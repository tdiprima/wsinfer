WSInfer is designed to work with directories of whole slide images rather than individual images. However, you can run it on a single image by placing that image in a directory.

Here's how to run WSInfer on one image:

### Basic approach:

1. Create a directory containing only your single whole slide image:

   ```sh
   mkdir slides
   cp your_image.svs slides/
   ```

2. Run WSInfer pointing to that directory:

   ```sh
   wsinfer run \
     --wsi-dir slides/ \
     --results-dir results/ \
     --model breast-tumor-resnet34.tcga-brca
   ```

### Key points:

* The `--wsi-dir` parameter expects a directory, not a single file
* The directory should contain only whole slide images (no other files)
* You need to specify a model from the WSInfer zoo (use wsinfer-zoo ls to see available models)
* Results will be saved to the specified results directory

### Example with common options:

```sh
wsinfer run \
  --wsi-dir slides/ \
  --results-dir results/ \
  --model breast-tumor-resnet34.tcga-brca \
  --batch-size 32 \
  --num-workers 4
```

### To see all available models:

```sh
wsinfer-zoo ls
```

### To get help on additional options:

```sh
wsinfer run --help
```

The tool will process your single image and create outputs including patch-level predictions in CSV and GeoJSON formats, tissue masks, and metadata about the run.

```sh
export WSINFER_FORCE_CPU=1
export CUDA_VISIBLE_DEVICES=0

time wsinfer run \
  --wsi-dir slides/ \
  --results-dir results/ \
  --model breast-tumor-resnet34.tcga-brca \
  --batch-size 16 \
  --num-workers 4
```

<br>
