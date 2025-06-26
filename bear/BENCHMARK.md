1. **Basic Timing with `time` command**

   The simplest approach is to use the Unix `time` command:

   ```sh
   # Install WSInfer first
   pip install -e .

   # Basic timing
   time wsinfer run \
     --wsi-dir slides/ \
     --results-dir results/ \
     --model breast-tumor-resnet34.tcga-brca \
     --batch-size 32 \
     --num-workers 4
   ```

2. **Create a benchmarking script**

### Here's a comprehensive benchmarking approach:

3. GPU Memory and Resource Monitoring

4. Benchmarking Steps After Installation

Here's your complete benchmarking workflow:

### Step 1: Install WSInfer

```sh
# From this repository
pip install -e .

# Or from PyPI
pip install wsinfer
```

### Step 2: Install monitoring dependencies

```sh
pip install psutil GPUtil  # GPUtil for GPU monitoring
```

### Step 3: Get test data

```sh
# Create a test slide directory
mkdir slides
# Download a sample slide (as mentioned in docs)
# Or use your own WSI files
```

### Step 4: Run basic benchmark

```sh
# Simple timing
time wsinfer run --wsi-dir slides/ --results-dir results/ --model breast-tumor-resnet34.tcga-brca

# Comprehensive benchmarking
python benchmark_wsinfer.py --wsi-dir slides/ --output benchmark_results.json

# Resource monitoring
python monitor_resources.py --command "wsinfer run --wsi-dir slides/ --results-dir results/ --model breast-tumor-resnet34.tcga-brca"
```

### Step 5: Key Performance Factors to Test

Based on code analysis, these are the key parameters that affect performance:

1. `--batch-size` &mdash; Higher = faster GPU utilization but more memory
2. `--num-workers` &mdash; More workers = faster data loading (up to CPU cores)
3. `--speedup` &mdash; JIT compilation (test shows this improves performance)
4. Models &mdash; Different models have different computational requirements
5. GPU vs CPU &mdash; Automatic detection but can force CPU with `WSINFER_FORCE_CPU=1`

<br>
