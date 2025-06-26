#!/usr/bin/env python3
"""
Monitor system resources during WSInfer execution.

Usage:
    python monitor_resources.py --command "wsinfer run --wsi-dir slides/ --results-dir results/ --model breast-tumor-resnet34.tcga-brca"
"""

import argparse
import subprocess
import threading
import time
import json
import psutil
import sys
from pathlib import Path
from typing import Dict, List, Any

try:
    import GPUtil
    GPU_AVAILABLE = True
except ImportError:
    GPU_AVAILABLE = False


class ResourceMonitor:
    def __init__(self, interval: float = 1.0):
        self.interval = interval
        self.monitoring = False
        self.data = []
        
    def start_monitoring(self):
        """Start monitoring system resources."""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """Stop monitoring and return collected data."""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join()
        return self.data
        
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            timestamp = time.time()
            
            # CPU and Memory
            cpu_percent = psutil.cpu_percent(interval=None)
            memory = psutil.virtual_memory()
            
            data_point = {
                "timestamp": timestamp,
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_used_gb": memory.used / (1024**3),
                "memory_available_gb": memory.available / (1024**3),
            }
            
            # GPU monitoring if available
            if GPU_AVAILABLE:
                try:
                    gpus = GPUtil.getGPUs()
                    gpu_data = []
                    for gpu in gpus:
                        gpu_data.append({
                            "id": gpu.id,
                            "name": gpu.name,
                            "memory_used_mb": gpu.memoryUsed,
                            "memory_total_mb": gpu.memoryTotal,
                            "memory_percent": gpu.memoryUtil * 100,
                            "gpu_percent": gpu.load * 100,
                            "temperature": gpu.temperature,
                        })
                    data_point["gpus"] = gpu_data
                except Exception as e:
                    data_point["gpu_error"] = str(e)
            
            self.data.append(data_point)
            time.sleep(self.interval)


def run_with_monitoring(command: List[str], monitor_interval: float = 1.0) -> Dict[str, Any]:
    """Run a command while monitoring system resources."""
    
    print(f"Starting monitoring for command: {' '.join(command)}")
    
    # Start resource monitoring
    monitor = ResourceMonitor(interval=monitor_interval)
    monitor.start_monitoring()
    
    start_time = time.time()
    
    try:
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        end_time = time.time()
        
        success = result.returncode == 0
        
    except Exception as e:
        end_time = time.time()
        success = False
        result = type('obj', (object,), {
            'returncode': -1,
            'stdout': '',
            'stderr': str(e)
        })
    
    # Stop monitoring
    resource_data = monitor.stop_monitoring()
    
    execution_time = end_time - start_time
    
    # Analyze resource usage
    if resource_data:
        cpu_usage = [d["cpu_percent"] for d in resource_data]
        memory_usage = [d["memory_used_gb"] for d in resource_data]
        
        analysis = {
            "max_cpu_percent": max(cpu_usage),
            "avg_cpu_percent": sum(cpu_usage) / len(cpu_usage),
            "max_memory_gb": max(memory_usage),
            "avg_memory_gb": sum(memory_usage) / len(memory_usage),
        }
        
        if GPU_AVAILABLE and any("gpus" in d for d in resource_data):
            gpu_memory_usage = []
            gpu_utilization = []
            
            for data_point in resource_data:
                if "gpus" in data_point:
                    for gpu in data_point["gpus"]:
                        gpu_memory_usage.append(gpu["memory_used_mb"])
                        gpu_utilization.append(gpu["gpu_percent"])
            
            if gpu_memory_usage:
                analysis.update({
                    "max_gpu_memory_mb": max(gpu_memory_usage),
                    "avg_gpu_memory_mb": sum(gpu_memory_usage) / len(gpu_memory_usage),
                    "max_gpu_utilization": max(gpu_utilization),
                    "avg_gpu_utilization": sum(gpu_utilization) / len(gpu_utilization),
                })
    else:
        analysis = {}
    
    return {
        "success": success,
        "execution_time": execution_time,
        "return_code": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "resource_analysis": analysis,
        "resource_timeline": resource_data,
    }


def main():
    parser = argparse.ArgumentParser(description="Monitor resources during WSInfer execution")
    parser.add_argument("--command", required=True, help="Command to run and monitor")
    parser.add_argument("--output", default="resource_monitor.json", help="Output file")
    parser.add_argument("--interval", type=float, default=1.0, help="Monitoring interval in seconds")
    
    args = parser.parse_args()
    
    # Parse command
    command = args.command.split()
    
    print(f"Monitoring command: {args.command}")
    if GPU_AVAILABLE:
        print("GPU monitoring enabled")
    else:
        print("GPU monitoring not available (install GPUtil for GPU monitoring)")
    
    # Run with monitoring
    results = run_with_monitoring(command, args.interval)
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print(f"\n📊 Monitoring Results:")
    print(f"Success: {results['success']}")
    print(f"Execution time: {results['execution_time']:.2f} seconds")
    
    if results['resource_analysis']:
        analysis = results['resource_analysis']
        print(f"Max CPU: {analysis.get('max_cpu_percent', 'N/A'):.1f}%")
        print(f"Max Memory: {analysis.get('max_memory_gb', 'N/A'):.2f} GB")
        
        if 'max_gpu_memory_mb' in analysis:
            print(f"Max GPU Memory: {analysis['max_gpu_memory_mb']:.0f} MB")
            print(f"Max GPU Utilization: {analysis['max_gpu_utilization']:.1f}%")
    
    print(f"Full results saved to: {args.output}")


if __name__ == "__main__":
    main()
