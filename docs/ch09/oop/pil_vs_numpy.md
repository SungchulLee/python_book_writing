# PIL vs NumPy Images

!!! tip "Mental Model"
    PIL gives you a high-level Image object with methods like `resize` and `crop`; NumPy gives you a raw `(H, W, C)` array you can manipulate with indexing and math. Convert between them freely with `np.array(img)` and `Image.fromarray(arr)`. Use PIL for I/O and standard transformations, NumPy for custom pixel-level computation.

    The key insight: **images are arrays.** A color image is a 3D array
    `(height, width, channels)` of uint8 values. Once you see this, every NumPy
    technique — slicing, broadcasting, ufuncs, linear algebra — applies directly
    to image data. PIL handles the file format layer; NumPy handles the math.

## Image Representation

### 1. PIL Image Object

```python
from PIL import Image

img = Image.open('photo.jpg')
print(type(img))  # <class 'PIL.Image.Image'>
print(img.size)   # (width, height)
print(img.mode)   # 'RGB', 'RGBA', 'L', etc.
```

### 2. NumPy Array

```python
import numpy as np

arr = np.array(img)
print(type(arr))  # <class 'numpy.ndarray'>
print(arr.shape)  # (height, width, channels)
print(arr.dtype)  # uint8
```

### 3. Key Difference

PIL: Format-aware object
NumPy: Raw pixel data

## When to Use Each

### 1. Use PIL For

```python
# I/O operations
img = Image.open('input.jpg')
img.save('output.png')

# Format conversion
img_rgb = img.convert('RGB')

# Resizing
img_small = img.resize((100, 100))

# Rotation
img_rot = img.rotate(45)
```

### 2. Use NumPy For

```python
# Pixel arithmetic
arr = np.array(img)
bright = np.clip(arr * 1.5, 0, 255).astype(np.uint8)

# Filtering
kernel = np.ones((5, 5)) / 25
filtered = convolve2d(arr[:,:,0], kernel)

# Batch processing
batch = np.array([arr1, arr2, arr3])  # (3, H, W, C)
```

### 3. Workflow

```python
# Load with PIL
img = Image.open('photo.jpg')

# Convert to NumPy for processing
arr = np.array(img)
processed = arr * 0.8  # Darken

# Convert back to PIL for saving
result = Image.fromarray(processed.astype(np.uint8))
result.save('output.jpg')
```

## Deep Learning

### 1. PyTorch Format

```python
import torch

# PIL → NumPy → PyTorch
img = Image.open('photo.jpg')
arr = np.array(img) / 255.0  # Normalize
tensor = torch.from_numpy(arr).permute(2, 0, 1)  # (C, H, W)
```

### 2. Preprocessing

```python
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),  # PIL → Tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

tensor = transform(img)
```

### 3. Batch Loading

```python
# DataLoader expects PIL or Tensor
from torch.utils.data import Dataset

class ImageDataset(Dataset):
    def __init__(self, image_paths):
        self.paths = image_paths
    
    def __getitem__(self, idx):
        img = Image.open(self.paths[idx])
        return transform(img)  # Returns Tensor
```

---

## Exercises

**Exercise 1.** Write a short code example that demonstrates the main concept covered on this page. Include comments explaining each step.

??? success "Solution to Exercise 1"
    Refer to the code examples in the page content above. A complete solution would recreate the key pattern with clear comments explaining the NumPy operations involved.

---

**Exercise 2.** Predict the output of a code snippet that uses the features described on this page. Explain why the output is what it is.

??? success "Solution to Exercise 2"
    The output depends on how NumPy handles the specific operation. Key factors include array shapes, dtypes, and broadcasting rules. Trace through the computation step by step.

---

**Exercise 3.** Write a practical function that applies the concepts from this page to solve a real data processing task. Test it with sample data.

??? success "Solution to Exercise 3"
    ```python
    import numpy as np

    # Example: apply the page's concept to process sample data
    data = np.random.default_rng(42).random((5, 3))
    # Apply the relevant operation
    result = data  # replace with actual operation
    print(result)
    ```

---

**Exercise 4.** Identify a common mistake when using the features described on this page. Write code that demonstrates the mistake and then show the corrected version.

??? success "Solution to Exercise 4"
    A common mistake is misunderstanding array shapes or dtypes. Always check `.shape` and `.dtype` when debugging unexpected results.
