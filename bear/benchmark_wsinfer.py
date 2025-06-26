#!/usr/bin/env python3
"""
Benchmark WSInfer performance across different configurations.

Usage:
    python benchmark_wsinfer.py --wsi-dir slides/ --output benchmark_results.json
"""

import argparse
import json
import time
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Any
import platform
import torch


def get_system_info() -> Dict[str, Any]:
    """Get system information for benchmarking context."""
    return {
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "mps_available": torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False,
    }


def run_benchmark(wsi_dir: Path, results_dir: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    """Run a single benchmark with given configuration."""
    
    # Clean results directory for this run
    run_results_dir = results_dir / f"run_{config['name']}"
    if run_results_dir.exists():
        import shutil
        shutil.rmtree(run_results_dir)
    
    # Build command
    cmd = [
        "wsinfer", "run",
        "--wsi-dir", str(wsi_dir),
        "--results-dir", str(run_results_dir),
        "--model", config["model"],
        "--batch-size", str(config["batch_size"]),
        "--num-workers", str(config["num_workers"]),
    ]
    
    if config.get("speedup", False):
        cmd.append("--speedup")
    else:
        cmd.append("--no-speedup")
    
    print(f"Running benchmark: {config['name']}")
    print(f"Command: {' '.join(cmd)}")
    
    start_time = time.perf_counter()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        
        return {
            "config": config,
            "execution_time_seconds": execution_time,
            "success": True,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
        
    except subprocess.CalledProcessError as e:
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        
        return {
            "config": config,
            "execution_time_seconds": execution_time,
            "success": False,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "return_code": e.returncode,
        }


def main():
    parser = argparse.ArgumentParser(description="Benchmark WSInfer performance")
    parser.add_argument("--wsi-dir", type=Path, required=True, help="Directory with WSI files")
    parser.add_argument("--output", type=Path, default="benchmark_results.json", help="Output JSON file")
    parser.add_argument("--models", nargs="+", default=["breast-tumor-resnet34.tcga-brca"], 
                       help="Models to benchmark")
    parser.add_argument("--batch-sizes", nargs="+", type=int, default=[16, 32, 64], 
                       help="Batch sizes to test")
    parser.add_argument("--num-workers", nargs="+", type=int, default=[0, 2, 4], 
                       help="Number of workers to test")
    args = parser.parse_args()
    
    if not args.wsi_dir.exists():
        print(f"Error: WSI directory {args.wsi_dir} does not exist")
        sys.exit(1)
    
    # Create temporary results directory
    results_base_dir = Path("benchmark_temp_results")
    results_base_dir.mkdir(exist_ok=True)
    
    # Generate benchmark configurations
    configs = []
    for model in args.models:
        for batch_size in args.batch_sizes:
            for num_workers in args.num_workers:
                for speedup in [False, True]:
                    config_name = f"{model}_bs{batch_size}_w{num_workers}_speedup{speedup}"
                    configs.append({
                        "name": config_name,
                        "model": model,
                        "batch_size": batch_size,
                        "num_workers": num_workers,
                        "speedup": speedup,
                    })
    
    print(f"Running {len(configs)} benchmark configurations...")
    
    benchmark_results = {
        "system_info": get_system_info(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "wsi_directory": str(args.wsi_dir),
        "results": []
    }
    
    for i, config in enumerate(configs, 1):
        print(f"\n--- Benchmark {i}/{len(configs)} ---")
        result = run_benchmark(args.wsi_dir, results_base_dir, config)
        benchmark_results["results"].append(result)
        
        if result["success"]:
            print(f"✅ Completed in {result['execution_time_seconds']:.2f} seconds")
        else:
            print(f"❌ Failed after {result['execution_time_seconds']:.2f} seconds")
    
    # Save results
    with open(args.output, 'w') as f:
        json.dump(benchmark_results, f, indent=2)
    
    print(f"\n📊 Benchmark results saved to {args.output}")
    
    # Print summary
    successful_runs = [r for r in benchmark_results["results"] if r["success"]]
    if successful_runs:
        fastest = min(successful_runs, key=lambda x: x["execution_time_seconds"])
        slowest = max(successful_runs, key=lambda x: x["execution_time_seconds"])
        
        print(f"\n📈 Performance Summary:")
        print(f"Successful runs: {len(successful_runs)}/{len(configs)}")
        print(f"Fastest: {fastest['config']['name']} ({fastest['execution_time_seconds']:.2f}s)")
        print(f"Slowest: {slowest['config']['name']} ({slowest['execution_time_seconds']:.2f}s)")
    
    # Cleanup
    import shutil
    shutil.rmtree(results_base_dir)


if __name__ == "__main__":
    main()
