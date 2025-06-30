This project is primarily focused on deep learning, not broader AI techniques.

### What WSInfer Uses:
* **Deep Learning Models:** The project uses various convolutional neural network (CNN) architectures for patch-based classification on whole slide images (WSI) in pathology
* **Specific Architectures:**
    * **ResNet34** (most common - used for breast, lung, pancreas, prostate tumor detection)
    * **InceptionV4** (used for lymphocyte detection)
    * Models are trained on TCGA datasets (cancer genomics data)

### Technical Approach:
* **Patch-based classification:** Divides whole slide images into smaller patches and runs inference on each patch
* **PyTorch-based:** Built on PyTorch for deep learning inference
* **Pre-trained models:** Uses a model zoo system with models hosted on HuggingFace Hub
* **JIT compilation:** Optimizes models using PyTorch's just-in-time compilation

### Not Traditional AI:
The project doesn't appear to use:

* Rule-based expert systems
* Classical machine learning algorithms (SVM, random forests, etc.)
* Symbolic AI approaches
* Traditional computer vision techniques (beyond basic preprocessing)

### Classification:
This is specialized deep learning for medical imaging - specifically computational pathology. It's a domain-specific application of deep neural networks rather than a broader AI system with multiple reasoning approaches.

---

It's deep learning (which is a subset of AI), but not "AI" in the broader sense of incorporating multiple artificial intelligence techniques.

<br>
