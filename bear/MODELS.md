### WSInfer works with a model zoo system where:

1. Models are downloaded from HuggingFace Hub when you run inference
2. Models are cached locally in `~/.cache/huggingface/` after first download
3. The repository contains the code framework but not the actual model weights

### This repository contains:

* Source code for the WSInfer framework
* Documentation 
* Tests
* Scripts for development
* Configuration files

No pre-trained model files.

### The models are distributed separately through:

1. WSInfer Model Zoo - Available models hosted on HuggingFace Hub
2. Models are downloaded automatically when you first use them
3. Models are cached locally in `~/.cache/huggingface/` after download

### To get the models, you would need to:

1. Install WSInfer (either from PyPI or by installing this repository in development mode)
2. Use the models - they download automatically when referenced

### For example, some available models mentioned in the code include:

* breast-tumor-resnet34.tcga-brca
* lung-tumor-resnet34.tcga-luad 
* pancancer-lymphocytes-inceptionv4.tcga
* pancreas-tumor-resnet34.tcga-paad
* prostate-tumor-resnet34.tcga-prad

If you want to install WSInfer from this repository and then access the models, you could run:

```sh
pip install -e .
wsinfer-zoo ls  # This will show available models
```

<br>
