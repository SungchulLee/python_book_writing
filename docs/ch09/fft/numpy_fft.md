# NumPy FFT — Fourier Transforms

The `np.fft` module provides functions for computing the discrete Fourier transform (DFT) and its inverse. Fourier transforms decompose signals into their frequency components.

!!! tip "Mental Model"
    The FFT answers the question "which frequencies are present and how strong are they?" It converts a time-domain signal into a list of sine-wave amplitudes and phases. `np.fft.fft` goes forward (time to frequency), `np.fft.ifft` goes back, and the process is lossless -- no information is created or destroyed.

!!! note "The Unified FFT Pipeline"
    Every topic in this section fits into a single system:

    ```text
    Signal → FFT → Frequency Domain
                        │
                ┌───────┴───────┐
            Problems        Applications
            │                   │
        ┌───┴───┐         ┌────┼────┐
     Leakage  No time   Filter  FFT2  Convolution
        │     info         │     │       │
    Windowing  STFT    denoise  images  fast blur
    ```

    **Decision guide:**

    | Question | Tool |
    |----------|------|
    | Global frequency content? | `fft` / `rfft` |
    | Time-varying frequencies? | STFT / spectrogram |
    | Spectral leakage? | Apply a window function first |
    | 2D signal (image)? | `fft2` / `ifft2` |
    | Large-kernel convolution? | `fftconvolve` |

!!! tip "If You Only Remember Three Things"
    ```python
    fft_result = np.fft.rfft(signal)          # 1. Transform
    magnitudes = np.abs(fft_result)            # 2. Get amplitudes
    frequencies = np.fft.rfftfreq(n, 1/fs)     # 3. Get frequency axis
    ```
    This is the minimal path from a time-domain signal to "which frequencies are present."

```python
import numpy as np
```

---

## What is a Fourier Transform?

The Fourier transform converts a signal from the **time domain** to the **frequency domain**:

- **Time domain**: Signal as amplitude vs. time
- **Frequency domain**: Signal as amplitude vs. frequency

```
Time Domain          Fourier Transform       Frequency Domain
    │                      →                      │
 ───┼──▄█▄──           np.fft.fft()         ───┼─█─────
    │                                            │   █
    t                                            f
```

---

## Mathematical Foundations of the DFT

The Discrete Fourier Transform (DFT) converts a length-$N$ sequence $\{x_0, x_1, \ldots, x_{N-1}\}$ in the time domain to a length-$N$ sequence $\{y_0, y_1, \ldots, y_{N-1}\}$ in the frequency domain:

$$y_k = \sum_{n=0}^{N-1} e^{-i\frac{2\pi}{N}nk} x_n, \qquad k = 0, 1, \ldots, N-1$$

The inverse DFT recovers the original sequence:

$$x_n = \frac{1}{N} \sum_{k=0}^{N-1} e^{i\frac{2\pi}{N}nk} y_k, \qquad n = 0, 1, \ldots, N-1$$

### Matrix Form

The DFT can be expressed as a matrix-vector multiplication $\mathbf{y} = W \mathbf{x}$, where $W$ is the DFT matrix with entries $W_{kn} = e^{-i 2\pi kn / N}$. The inverse DFT is $\mathbf{x} = \frac{1}{N} W^* \mathbf{y}$, where $W^*$ is the conjugate of $W$.

### Manual DFT Implementation

Building the DFT from the matrix formula reinforces the linear algebra connection:

```python
import numpy as np
import matplotlib.pyplot as plt

N = 100
time = np.linspace(-2, 2, N)
x = np.zeros_like(time)
x[abs(time) < 1] = time[abs(time) < 1]  # Tent function

# Build the DFT matrix
n = np.arange(N).reshape((N, 1))
k = np.arange(N).reshape((1, N))
nk = n @ k  # (N, N) outer product
W = np.exp(-1j * (2 * np.pi / N) * nk)       # DFT matrix
W_inv = np.exp(1j * (2 * np.pi / N) * nk)    # Inverse DFT matrix

# Forward and inverse transforms
y = W @ x
x_recovered = (W_inv @ y) / N

fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(12, 3))
ax0.plot(x, '--ok', markersize=1, label='Original')
ax1.plot(np.real(y), '--ob', markersize=1, label='Real')
ax1.plot(np.imag(y), '--or', markersize=1, label='Imag')
ax2.plot(x, '--ok', markersize=1, label='Original')
ax2.plot(np.real(x_recovered), '--ob', markersize=1, label='Recovered Real')
for ax, title in zip((ax0, ax1, ax2), ('Time Domain', 'Frequency Domain', 'Time Domain')):
    ax.legend()
    ax.set_title(title)
plt.tight_layout()
plt.show()
```

The manual implementation confirms that `np.fft.fft()` and `np.fft.ifft()` are simply optimized algorithms (the Fast Fourier Transform) for computing this matrix-vector product in $O(N \log N)$ instead of $O(N^2)$.

---

## Basic FFT

### np.fft.fft() — 1D Transform

```python
# Simple signal: sum of two sine waves
t = np.linspace(0, 1, 1000)  # 1 second, 1000 samples
signal = np.sin(2 * np.pi * 5 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)

# Compute FFT
fft_result = np.fft.fft(signal)

# Result is complex: contains magnitude and phase
print(fft_result.dtype)  # complex128
print(len(fft_result))   # 1000 (same as input)
```

### Getting Frequencies

```python
# Sample rate
sample_rate = 1000  # Hz (samples per second)
n = len(signal)

# Get frequency bins
frequencies = np.fft.fftfreq(n, d=1/sample_rate)

# Magnitude spectrum
magnitude = np.abs(fft_result)

# Phase spectrum
phase = np.angle(fft_result)
```

### Positive Frequencies Only

FFT output is symmetric for real signals. Usually we only want positive frequencies:

```python
# Use only first half (positive frequencies)
n_half = n // 2
freq_positive = frequencies[:n_half]
magnitude_positive = magnitude[:n_half]

# Or use rfft for real input (more efficient)
fft_real = np.fft.rfft(signal)
freq_real = np.fft.rfftfreq(n, d=1/sample_rate)
```

---

## Inverse FFT

### np.fft.ifft() — Reconstruct Signal

```python
# Original signal
signal = np.sin(2 * np.pi * 5 * t)

# Forward FFT
fft_result = np.fft.fft(signal)

# Inverse FFT (reconstruct)
reconstructed = np.fft.ifft(fft_result)

# Should match original (within floating point precision)
print(np.allclose(signal, reconstructed.real))  # True
```

---

## 2D FFT (Images)

### np.fft.fft2() — 2D Transform

```python
# Create simple 2D pattern
image = np.zeros((100, 100))
image[40:60, 40:60] = 1  # White square

# 2D FFT
fft_2d = np.fft.fft2(image)

# Shift zero frequency to center (for visualization)
fft_shifted = np.fft.fftshift(fft_2d)

# Magnitude spectrum
magnitude_2d = np.abs(fft_shifted)
```

### Inverse 2D FFT

```python
# Reconstruct image
reconstructed = np.fft.ifft2(fft_2d)
print(np.allclose(image, reconstructed.real))  # True
```

---

## Common Operations

### fftshift / ifftshift

Shift zero-frequency component to center (useful for visualization):

```python
fft_result = np.fft.fft(signal)

# Shift: zero frequency to center
shifted = np.fft.fftshift(fft_result)

# Unshift: back to original layout
unshifted = np.fft.ifftshift(shifted)
```

### rfft / irfft (Real Input)

More efficient for real-valued signals:

```python
# Real signal → use rfft (half the output)
signal = np.random.randn(1000)

fft_complex = np.fft.fft(signal)     # Length: 1000
fft_real = np.fft.rfft(signal)       # Length: 501

# Inverse
reconstructed = np.fft.irfft(fft_real)
```

---

## Practical Examples

### Find Dominant Frequency

```python
# Signal with unknown frequency
sample_rate = 1000
t = np.linspace(0, 1, sample_rate)
signal = np.sin(2 * np.pi * 50 * t) + np.random.randn(sample_rate) * 0.5

# FFT
fft = np.fft.rfft(signal)
freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
magnitudes = np.abs(fft)

# Find peak frequency
peak_idx = np.argmax(magnitudes)
dominant_freq = freqs[peak_idx]
print(f"Dominant frequency: {dominant_freq} Hz")  # ~50 Hz
```

### Low-Pass Filter

```python
def low_pass_filter(signal, sample_rate, cutoff_freq):
    """Remove frequencies above cutoff."""
    fft = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
    
    # Zero out high frequencies
    fft[freqs > cutoff_freq] = 0
    
    # Reconstruct
    return np.fft.irfft(fft)

# Apply 100 Hz low-pass filter
filtered = low_pass_filter(signal, sample_rate=1000, cutoff_freq=100)
```

### Remove Specific Frequency (Notch Filter)

```python
def notch_filter(signal, sample_rate, remove_freq, bandwidth=2):
    """Remove specific frequency band."""
    fft = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1/sample_rate)
    
    # Zero out target frequency band
    mask = (freqs > remove_freq - bandwidth) & (freqs < remove_freq + bandwidth)
    fft[mask] = 0
    
    return np.fft.irfft(fft)

# Remove 60 Hz hum
clean_signal = notch_filter(signal, 1000, 60)
```

### Power Spectrum

```python
def power_spectrum(signal, sample_rate):
    """Compute power spectral density."""
    n = len(signal)
    fft = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(n, 1/sample_rate)
    
    # Power = |FFT|² / n
    power = np.abs(fft) ** 2 / n
    
    return freqs, power

freqs, power = power_spectrum(signal, 1000)
```

---

## FFT Functions Summary

| Function | Purpose |
|----------|---------|
| `fft(a)` | 1D FFT |
| `ifft(a)` | Inverse 1D FFT |
| `fft2(a)` | 2D FFT |
| `ifft2(a)` | Inverse 2D FFT |
| `fftn(a)` | N-dimensional FFT |
| `rfft(a)` | 1D FFT for real input |
| `irfft(a)` | Inverse of rfft |
| `fftfreq(n, d)` | Frequency bins for fft |
| `rfftfreq(n, d)` | Frequency bins for rfft |
| `fftshift(a)` | Shift zero-freq to center |
| `ifftshift(a)` | Inverse of fftshift |

---

## Performance Tips

```python
# FFT is fastest when length is power of 2
n = 1024  # 2^10 — fast
n = 1000  # not power of 2 — slower

# Pad to next power of 2
def next_power_of_2(x):
    return 1 << (x - 1).bit_length()

signal_padded = np.pad(signal, (0, next_power_of_2(len(signal)) - len(signal)))
```

---

## scipy.fft Module

The `scipy.fft` module provides the same FFT functions as `np.fft` but with additional features such as multithreading support via the `workers` parameter:

```python
import scipy.fft as fft

y = fft.fft(x)
x_recovered = fft.ifft(y)

# Parallel computation with multiple workers
y_parallel = fft.fft(x, workers=-1)  # Use all available CPU cores
```

For most use cases, `np.fft` and `scipy.fft` produce identical results. Use `scipy.fft` when you need the extra performance from multithreading or access to additional transform types.

---

## Key Takeaways

- FFT converts time domain → frequency domain
- `np.fft.fft()` for complex/general signals
- `np.fft.rfft()` for real signals (more efficient)
- `fftfreq()` / `rfftfreq()` get frequency bins
- `fftshift()` centers zero frequency (for visualization)
- Use `np.abs()` for magnitude, `np.angle()` for phase
- Power of 2 lengths are fastest
- Common applications: filtering, spectrum analysis, image processing

---

## Runnable Example: `dft_matrix_implementation.py`

```python
"""
Manual DFT Implementation Using Matrix Algebra
================================================
Level: Intermediate
Topics: Discrete Fourier Transform, matrix-vector multiplication,
        complex exponentials, frequency domain analysis

This module implements the DFT from first principles using the matrix
formulation, then verifies against scipy.fft for correctness.
"""

import numpy as np
import scipy.fft as fft
import matplotlib.pyplot as plt

# =============================================================================
# SECTION 1: Build the DFT Matrix
# =============================================================================

if __name__ == "__main__":
    """
    The DFT of a length-N sequence x is y = W @ x, where:

        W[k, n] = exp(-i * 2π * k * n / N)

    The inverse DFT is x = (1/N) * W* @ y, where W* is the conjugate.
    """


    def build_dft_matrix(N):
        """Build the N×N DFT matrix W and its conjugate W*."""
        n = np.arange(N).reshape((N, 1))
        k = np.arange(N).reshape((1, N))
        nk = n @ k  # (N, N) outer product of indices
        W = np.exp(-1j * (2 * np.pi / N) * nk)
        W_conj = np.exp(1j * (2 * np.pi / N) * nk)
        return W, W_conj


    def manual_fft(x, W):
        """Forward DFT: y = W @ x."""
        return W @ x


    def manual_ifft(y, W_conj, N):
        """Inverse DFT: x = (1/N) * W* @ y."""
        return (W_conj @ y) / N


    # =============================================================================
    # SECTION 2: Test Signal — Tent Function
    # =============================================================================

    N = 100
    time = np.linspace(-2, 2, N)
    x = np.zeros_like(time)
    x[abs(time) < 1] = time[abs(time) < 1]

    # =============================================================================
    # SECTION 3: Manual DFT vs scipy.fft
    # =============================================================================

    W, W_conj = build_dft_matrix(N)

    # Manual DFT
    y_manual = manual_fft(x, W)
    x_recovered_manual = manual_ifft(y_manual, W_conj, N)

    # scipy.fft for comparison
    y_scipy = fft.fft(x)
    x_recovered_scipy = fft.ifft(y_scipy)

    # Verify they match
    print("Manual vs scipy.fft agreement:")
    print(f"  Forward: {np.allclose(y_manual, y_scipy)}")
    print(f"  Inverse: {np.allclose(x_recovered_manual, x_recovered_scipy)}")
    print(f"  Roundtrip error: {np.max(np.abs(x - np.real(x_recovered_manual))):.2e}")

    # =============================================================================
    # SECTION 4: Visualization
    # =============================================================================

    fig, axes = plt.subplots(1, 3, figsize=(14, 4))

    # Time domain (original)
    axes[0].plot(x, '--ok', markersize=2, label='Original')
    axes[0].set_title('Time Domain')
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # Frequency domain
    axes[1].plot(np.real(y_manual), '--ob', markersize=1, label='Real')
    axes[1].plot(np.imag(y_manual), '--or', markersize=1, label='Imag')
    axes[1].set_title('Frequency Domain (Manual DFT)')
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    # Recovered signal
    axes[2].plot(x, '--ok', markersize=2, label='Original')
    axes[2].plot(np.real(x_recovered_manual), '--ob', markersize=1, label='Recovered')
    axes[2].set_title('Time Domain (Recovered)')
    axes[2].legend()
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # =============================================================================
    # SECTION 5: Performance Comparison
    # =============================================================================
    """
    The manual DFT using matrix multiplication is O(N²).
    The FFT algorithm (Cooley-Tukey) is O(N log N).
    For N = 100, this is 10000 vs ~664 — a ~15x difference.
    For N = 10000, it's 100,000,000 vs ~132,877 — a ~750x difference.
    """

    import time

    for N_test in [100, 1000]:
        W_test, _ = build_dft_matrix(N_test)
        x_test = np.random.randn(N_test)

        t0 = time.perf_counter()
        for _ in range(100):
            _ = W_test @ x_test
        t_manual = time.perf_counter() - t0

        t0 = time.perf_counter()
        for _ in range(100):
            _ = fft.fft(x_test)
        t_fft = time.perf_counter() - t0

        print(f"\nN={N_test}:")
        print(f"  Manual (matrix):  {t_manual:.4f} sec")
        print(f"  scipy.fft:        {t_fft:.4f} sec")
        print(f"  Speedup:          {t_manual / t_fft:.1f}x")
```

---

## Exercises

**Exercise 1.**
Create a signal composed of three sine waves at 5 Hz, 20 Hz, and 50 Hz with amplitudes 1.0, 0.5, and 0.3 respectively, sampled at 200 Hz for 2 seconds. Use `np.fft.rfft` and `np.fft.rfftfreq` to find the three peak frequencies and their magnitudes. Verify that the detected frequencies match the inputs.

??? success "Solution to Exercise 1"

        import numpy as np

        fs = 200
        t = np.arange(0, 2, 1/fs)
        signal = 1.0 * np.sin(2*np.pi*5*t) + 0.5 * np.sin(2*np.pi*20*t) + 0.3 * np.sin(2*np.pi*50*t)

        fft_result = np.fft.rfft(signal)
        freqs = np.fft.rfftfreq(len(signal), 1/fs)
        magnitudes = np.abs(fft_result)

        # Find top 3 peaks
        peak_indices = np.argsort(magnitudes)[-3:]
        for idx in sorted(peak_indices):
            print(f"Frequency: {freqs[idx]:.1f} Hz, Magnitude: {magnitudes[idx]:.1f}")

---

**Exercise 2.**
Write a band-pass filter function that keeps only frequencies between `low_freq` and `high_freq`. Test it on a signal that mixes a 5 Hz sine, a 50 Hz sine, and a 120 Hz sine (sampled at 500 Hz). Apply a 30--80 Hz band-pass and verify that only the 50 Hz component survives.

??? success "Solution to Exercise 2"

        import numpy as np

        def bandpass_filter(signal, fs, low_freq, high_freq):
            fft = np.fft.rfft(signal)
            freqs = np.fft.rfftfreq(len(signal), 1/fs)
            mask = (freqs >= low_freq) & (freqs <= high_freq)
            fft_filtered = fft * mask
            return np.fft.irfft(fft_filtered, n=len(signal))

        fs = 500
        t = np.arange(0, 2, 1/fs)
        signal = np.sin(2*np.pi*5*t) + np.sin(2*np.pi*50*t) + np.sin(2*np.pi*120*t)

        filtered = bandpass_filter(signal, fs, 30, 80)

        # Check: only 50 Hz should remain
        fft_out = np.fft.rfft(filtered)
        freqs_out = np.fft.rfftfreq(len(filtered), 1/fs)
        peak_idx = np.argmax(np.abs(fft_out))
        print(f"Dominant frequency after band-pass: {freqs_out[peak_idx]:.1f} Hz")

---

**Exercise 3.**
Demonstrate that the FFT is faster when the signal length is a power of 2. Time `np.fft.fft` on signals of length 1000 and length 1024 (each repeated 1000 times) and print the speedup factor.

??? success "Solution to Exercise 3"

        import numpy as np
        import time

        signal_1000 = np.random.randn(1000)
        signal_1024 = np.random.randn(1024)

        start = time.perf_counter()
        for _ in range(1000):
            np.fft.fft(signal_1000)
        t_1000 = time.perf_counter() - start

        start = time.perf_counter()
        for _ in range(1000):
            np.fft.fft(signal_1024)
        t_1024 = time.perf_counter() - start

        print(f"Length 1000: {t_1000:.4f} sec")
        print(f"Length 1024: {t_1024:.4f} sec")
        print(f"Speedup (power of 2): {t_1000 / t_1024:.2f}x")
