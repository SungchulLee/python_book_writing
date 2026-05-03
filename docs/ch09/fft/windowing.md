# Window Functions and Spectral Leakage

!!! tip "Mental Model"
    The FFT assumes your signal repeats forever. When the signal's start and end don't match, the discontinuity smears energy across all frequencies -- this is spectral leakage. A window function tapers the signal to zero at both ends, removing the discontinuity and concentrating each frequency peak where it belongs.

## The Spectral Leakage Problem

The DFT (and FFT) assumes the input signal is **periodic**—it treats your signal as if it repeats infinitely. This works well when your signal truly is periodic or when you capture an integer number of cycles.

But what happens when your signal is not periodic, or you capture a non-integer number of cycles?

### Visualizing the Problem

Consider a simple sine wave at 10 Hz sampled for 0.95 seconds (not an integer number of periods):

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Signal: 10 Hz sine, sampled for 0.95 seconds (not integer periods)
fs = 1000
duration = 0.95
t = np.arange(0, duration, 1/fs)
x = np.sin(2 * np.pi * 10 * t)

# Compute FFT
X = np.fft.fft(x)
freqs = np.fft.fftfreq(len(x), 1/fs)

# Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

# Time domain
ax = axes[0, 0]
ax.plot(t, x, 'b-', linewidth=0.5)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude')
ax.set_title('Input Signal: 10 Hz Sine (0.95 sec)')
ax.grid(True, alpha=0.3)

# Discontinuity at wraparound
ax = axes[0, 1]
t_wrap = np.array([t[-1], 0])
x_wrap = np.array([x[-1], x[0]])
ax.plot(t, x, 'b-', linewidth=0.5, label='Signal')
ax.plot(t_wrap, x_wrap, 'r--', linewidth=2, label='Discontinuity')
ax.set_xlabel('Time [s]')
ax.set_ylabel('Amplitude')
ax.set_title('DFT Assumes Periodicity → Discontinuity at Edge')
ax.legend()
ax.grid(True, alpha=0.3)

# FFT magnitude (linear scale)
ax = axes[1, 0]
mask = freqs > 0
ax.stem(freqs[mask][:100], np.abs(X[mask])[:100], basefmt=' ')
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude')
ax.set_title('FFT Magnitude (Linear) - Spectral Leakage')
ax.grid(True, alpha=0.3)
ax.set_xlim([0, 50])

# FFT magnitude (dB scale)
ax = axes[1, 1]
X_db = 20 * np.log10(np.abs(X[mask]) + 1e-10)
ax.semilogy(freqs[mask][:100], np.abs(X[mask][:100]) + 1e-10)
ax.set_xlabel('Frequency [Hz]')
ax.set_ylabel('Magnitude (dB)')
ax.set_title('FFT Magnitude (Log) - Leakage Visible')
ax.grid(True, alpha=0.3, which='both')
ax.set_xlim([0, 50])

plt.tight_layout()
plt.show()

# Quantify leakage
peak_idx = np.argmax(np.abs(X[1:len(X)//2])) + 1
peak_freq = freqs[peak_idx]
peak_mag = np.abs(X[peak_idx])
noise_mag = np.mean(np.abs(X[1:len(X)//2]))
leakage_ratio = peak_mag / noise_mag

print(f"Peak frequency: {peak_freq:.1f} Hz (expected 10 Hz)")
print(f"Peak magnitude: {peak_mag:.1f}")
print(f"Mean noise floor: {noise_mag:.3f}")
print(f"Leakage ratio: {leakage_ratio:.1f}:1")
```

**What's happening:**
- The signal doesn't repeat seamlessly at the boundary
- The discontinuity introduces high-frequency components ("spectral leakage")
- Energy "leaks" from the signal's true frequency bin into neighboring bins
- The FFT shows power spread across many frequencies, not just at 10 Hz

## Rectangular Window vs. Smooth Windows

### The Rectangular Window

By default, the DFT uses an implicit **rectangular window** (just multiply by 1, then 0):

$$w_{\text{rect}}[n] = \begin{cases} 1 & 0 \le n < N \\ 0 & \text{otherwise} \end{cases}$$

This window has abrupt edges, creating the discontinuity problem above.

### Smooth Windows Reduce Leakage

A **smooth window** tapers signal values to zero at the edges, eliminating the discontinuity:

```python
def visualize_windows(N=512):
    """Compare different window functions."""
    n = np.arange(N)

    windows = {
        'Rectangular': np.ones(N),
        'Hann': np.hanning(N),
        'Hamming': np.hamming(N),
        'Blackman': np.blackman(N),
        'Kaiser (β=5)': np.kaiser(N, beta=5),
        'Kaiser (β=10)': np.kaiser(N, beta=10),
    }

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()

    for idx, (name, w) in enumerate(windows.items()):
        ax = axes[idx]
        ax.plot(n, w, 'b-', linewidth=1.5)
        ax.fill_between(n, 0, w, alpha=0.3)
        ax.set_title(name)
        ax.set_ylabel('Amplitude')
        ax.set_xlim([0, N])
        ax.set_ylim([0, 1.1])
        ax.grid(True, alpha=0.3)

    plt.suptitle('Comparison of Window Functions (N=512)')
    plt.tight_layout()
    plt.show()

visualize_windows()
```

**Key observations:**
- Rectangular: Edges are sharp (1 → 0 instantly)
- Hann, Hamming, Blackman: Edges taper smoothly (0 → 1 → 0)
- Kaiser: Tunable edge sharpness via β parameter

## Common Window Functions

### Hann (Hanning) Window

$$w[n] = 0.5 \left(1 - \cos\left(\frac{2\pi n}{N-1}\right)\right), \quad 0 \le n < N$$

**Characteristics:**
- General-purpose window, widely used
- Good balance of main lobe width and sidelobe attenuation
- Sidelobe level: ~-32 dB

```python
w_hann = np.hanning(512)
print(f"Hann window min: {w_hann.min():.4f}, max: {w_hann.max():.4f}")
```

### Hamming Window

$$w[n] = 0.54 - 0.46 \cos\left(\frac{2\pi n}{N-1}\right), \quad 0 \le n < N$$

**Characteristics:**
- Slightly flatter peak than Hann
- Sidelobe level: ~-43 dB (better than Hann)
- Does not quite reach zero at edges (residual window effect)

```python
w_hamming = np.hamming(512)
print(f"Hamming window min: {w_hamming.min():.4f}, max: {w_hamming.max():.4f}")
```

### Blackman Window

$$w[n] = 0.42 - 0.5 \cos\left(\frac{2\pi n}{N-1}\right) + 0.08 \cos\left(\frac{4\pi n}{N-1}\right)$$

**Characteristics:**
- Very low sidelobe level: ~-58 dB
- Wider main lobe (reduced frequency resolution)
- Use when sidelobe reduction is critical (e.g., radar)

```python
w_blackman = np.blackman(512)
print(f"Blackman window min: {w_blackman.min():.6f}, max: {w_blackman.max():.6f}")
```

### Kaiser Window (Tunable)

$$w[n] = \frac{I_0\left(\beta\sqrt{1-(2n/N-1)^2}\right)}{I_0(\beta)}$$

where $I_0$ is the modified Bessel function of the first kind.

**The β parameter tunes the trade-off:**
- $\beta = 0$: Rectangular window
- $\beta = 5$: Similar to Hamming
- $\beta = 10$: Better sidelobe suppression (~-60 dB)
- $\beta = 100$: Extremely sharp edges, high sidelobe suppression (~-120 dB)

```python
# Visualize Kaiser window for different beta values
fig, axes = plt.subplots(1, 4, figsize=(14, 4))

betas = [0, 5, 10, 100]
for idx, beta in enumerate(betas):
    w = np.kaiser(512, beta)
    ax = axes[idx]
    ax.plot(w, 'b-')
    ax.fill_between(np.arange(512), 0, w, alpha=0.3)
    ax.set_title(f'Kaiser (β={beta})')
    ax.set_ylim([0, 1.1])
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Practical example: design Kaiser window for target sidelobe
def design_kaiser_window(N, target_atten_dB, width):
    """Design Kaiser window for target sidelobe attenuation."""
    if target_atten_dB < 21:
        beta = 0
    elif target_atten_dB < 50:
        beta = 0.5842 * (target_atten_dB - 21)**0.4 + 0.07886 * (target_atten_dB - 21)
    else:
        beta = 0.1102 * (target_atten_dB - 8.7)

    return np.kaiser(N, beta)

# Design for -80 dB sidelobe
w = design_kaiser_window(512, 80, width=100)
print(f"Kaiser window for -80 dB: β ≈ {0.1102 * (80 - 8.7):.1f}")
```

!!! note "Kaiser Window Design"
    The β parameter has design rules:
    - $\beta = 0.1102(A - 8.7)$ for $A > 50$ dB
    - $\beta = 0.5842(A - 21)^{0.4} + 0.07886(A - 21)$ for $21 < A < 50$ dB

    where A is the desired sidelobe attenuation in dB.

## When to Use Which Window

!!! tip "Quick Reference"
    | Scenario | Window | Why |
    |----------|--------|-----|
    | General-purpose / default | **Hann** | Best balance of resolution and leakage suppression |
    | Audio and speech processing | **Hann** or **Hamming** | Standard in librosa, scipy defaults |
    | Detecting weak signals near strong ones | **Kaiser** (high $\beta$) or **Blackman** | Low sidelobes reveal hidden peaks |
    | Maximum frequency resolution | **Rectangular** | Narrowest main lobe (only if integer periods) |
    | Radar / sonar | **Blackman** or **Kaiser** | Very low sidelobe floor required |
    | Unsure / experimenting | **Hann** first, then compare **Kaiser** ($\beta = 10$) | Covers most trade-off space |

## Trade-offs: Sidelobe Reduction vs. Main Lobe Width

Every window function involves a trade-off:

| Window | Sidelobe Level | Main Lobe Width | Use Case |
|--------|----------------|-----------------|----------|
| Rectangular | -13 dB | Narrowest | Frequency estimation (integer cycles) |
| Hann | -32 dB | 4 bins | General-purpose |
| Hamming | -43 dB | 4 bins | Better sidelobe suppression |
| Blackman | -58 dB | 6 bins | Radar, very low noise tolerance |
| Kaiser (β=10) | -60 dB | 5 bins | Tunable trade-off |

**Interpretation:**
- **Main lobe width**: Narrower = better frequency resolution
- **Sidelobe level**: Lower = better dynamic range, weaker signals visible

**Example:**
- If two signals are close in frequency, a wider main lobe (Blackman) will merge them
- If a weak signal hides behind a strong signal's sidelobes, you need lower sidelobes

```python
def compare_window_spectra(N=512):
    """Compare window functions in frequency domain."""
    windows = {
        'Rectangular': np.ones(N),
        'Hann': np.hanning(N),
        'Hamming': np.hamming(N),
        'Blackman': np.blackman(N),
        'Kaiser (β=10)': np.kaiser(N, 10),
    }

    fig, ax = plt.subplots(figsize=(12, 6))

    for name, w in windows.items():
        # Compute frequency response
        W = np.fft.fft(w, 2048)
        W_db = 20 * np.log10(np.abs(W) / np.max(np.abs(W)) + 1e-10)

        freqs = np.fft.fftfreq(len(W), 1/N)
        ax.plot(freqs[:1024], W_db[:1024], label=name, linewidth=2)

    ax.set_xlim([-20, 20])
    ax.set_ylim([-100, 5])
    ax.set_xlabel('Normalized Frequency (bins)')
    ax.set_ylabel('Magnitude (dB)')
    ax.set_title('Window Functions in Frequency Domain')
    ax.legend(loc='lower left')
    ax.grid(True, alpha=0.3, which='both')
    plt.tight_layout()
    plt.show()

compare_window_spectra()
```

## Using NumPy Window Functions

```python
import numpy as np

# Create windows of length N
N = 512

# Hann window
w_hann = np.hanning(N)
w_hann = np.hann(N)  # alternative name (NumPy 1.20+)

# Hamming window
w_hamming = np.hamming(N)

# Blackman window
w_blackman = np.blackman(N)

# Kaiser window with beta parameter
w_kaiser = np.kaiser(N, beta=10)

# bartlett, blackmanharris, nuttall, etc.
w_bartlett = np.bartlett(N)
```

!!! tip "Window Selection Guidelines"
    1. **Default choice**: Hann window (good balance)
    2. **Weak signal detection**: Kaiser or Blackman (lower sidelobes)
    3. **High frequency resolution needed**: Rectangular or Kaiser with low β
    4. **Audio/speech processing**: Hann or Hamming
    5. **Radar/Sonar**: Blackman or Kaiser
    6. **Experimental**: Start with Hann, compare with Hamming and Kaiser(β=10)

## Practical Example: Cleaning Up FFT with Windowing

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Create a signal with two close frequencies: 100 Hz and 105 Hz
fs = 1000
duration = 1
t = np.arange(0, duration, 1/fs)

# Signal: weak 100 Hz + strong 105 Hz
x = 0.5 * np.sin(2*np.pi*100*t) + np.sin(2*np.pi*105*t)

# Add noise
np.random.seed(42)
x += 0.05 * np.random.randn(len(x))

# Compute FFTs with different windows
windows = {
    'Rectangular': np.ones(len(x)),
    'Hann': np.hanning(len(x)),
    'Hamming': np.hamming(len(x)),
    'Blackman': np.blackman(len(x)),
}

fig, axes = plt.subplots(2, 2, figsize=(14, 8))
axes = axes.flatten()

for idx, (name, w) in enumerate(windows.items()):
    # Apply window
    x_windowed = x * w

    # Compute FFT
    X = np.fft.fft(x_windowed)
    freqs = np.fft.fftfreq(len(x), 1/fs)

    # Plot magnitude in dB
    ax = axes[idx]
    mask = (freqs > 0) & (freqs < 200)
    X_db = 20 * np.log10(np.abs(X) + 1e-10)

    ax.plot(freqs[mask], X_db[mask], 'b-', linewidth=1)
    ax.axvline(100, color='g', linestyle='--', label='100 Hz (weak)')
    ax.axvline(105, color='r', linestyle='--', label='105 Hz (strong)')
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Magnitude [dB]')
    ax.set_title(f'{name} Window')
    ax.set_ylim([-80, 0])
    ax.set_xlim([80, 130])
    ax.legend()
    ax.grid(True, alpha=0.3, which='both')

plt.suptitle('Effect of Window on FFT Resolution')
plt.tight_layout()
plt.show()

# Quantify performance
print("Window Performance Comparison:")
print(f"{'Window':<15} {'100 Hz Peak':<15} {'105 Hz Peak':<15} {'Separation':<15}")
print("-" * 60)

for name, w in windows.items():
    x_windowed = x * w
    X = np.fft.fft(x_windowed)
    freqs = np.fft.fftfreq(len(x), 1/fs)

    # Find peaks
    X_db = 20 * np.log10(np.abs(X) + 1e-10)
    peak_100_idx = np.argmin(np.abs(freqs - 100))
    peak_105_idx = np.argmin(np.abs(freqs - 105))

    peak_100 = X_db[peak_100_idx]
    peak_105 = X_db[peak_105_idx]
    sep = peak_105 - peak_100

    print(f"{name:<15} {peak_100:>10.1f} dB  {peak_105:>10.1f} dB  {sep:>10.1f} dB")
```

## Summary

- **Spectral leakage** occurs when signals aren't periodic over the window
- **Rectangular window** (default) has sharp edges but high sidelobes
- **Smooth windows** (Hann, Hamming, Blackman, Kaiser) taper edges, reducing leakage
- **Kaiser window** with tunable β provides maximum flexibility
- **Trade-off**: Sidelobe suppression vs. main lobe width (dynamic range vs. resolution)
- **Standard choice**: Hann window for most applications

**Next steps:**
1. Read **Spectrogram and STFT** to see windows in action on time-varying signals
2. Explore **2D FFT** for image processing where windowing is less critical
3. Study window design theory for specialized applications

---

## Exercises

**Exercise 1.**
Create a 10 Hz sine wave sampled at 1000 Hz for exactly 1.0 seconds (integer number of periods) and for 0.95 seconds (non-integer). Compute the FFT of each and compare the peak magnitudes and the noise floor. Quantify how much spectral leakage is reduced when the signal has an integer number of periods.

??? success "Solution to Exercise 1"

        import numpy as np

        fs = 1000
        # Integer periods
        t1 = np.arange(0, 1.0, 1/fs)
        x1 = np.sin(2*np.pi*10*t1)
        X1 = np.fft.rfft(x1)
        freqs1 = np.fft.rfftfreq(len(x1), 1/fs)

        # Non-integer periods
        t2 = np.arange(0, 0.95, 1/fs)
        x2 = np.sin(2*np.pi*10*t2)
        X2 = np.fft.rfft(x2)
        freqs2 = np.fft.rfftfreq(len(x2), 1/fs)

        mag1 = np.abs(X1)
        mag2 = np.abs(X2)

        peak1 = mag1.max()
        floor1 = np.mean(mag1[mag1 < peak1 * 0.1])
        peak2 = mag2.max()
        floor2 = np.mean(mag2[mag2 < peak2 * 0.1])

        print(f"Integer periods - Peak: {peak1:.1f}, Floor: {floor1:.4f}, Ratio: {peak1/floor1:.0f}")
        print(f"Non-integer     - Peak: {peak2:.1f}, Floor: {floor2:.4f}, Ratio: {peak2/floor2:.0f}")

---

**Exercise 2.**
Apply three different windows (rectangular, Hann, and Blackman) to a 50 Hz sine wave of duration 0.93 seconds sampled at 1000 Hz. For each windowed FFT, compute the sidelobe level relative to the main peak in dB. Verify that Blackman has the lowest sidelobes.

??? success "Solution to Exercise 2"

        import numpy as np

        fs = 1000
        t = np.arange(0, 0.93, 1/fs)
        x = np.sin(2*np.pi*50*t)

        for name, w in [('Rectangular', np.ones(len(t))),
                         ('Hann', np.hanning(len(t))),
                         ('Blackman', np.blackman(len(t)))]:
            X = np.fft.rfft(x * w)
            mag_db = 20 * np.log10(np.abs(X) + 1e-10)
            peak_db = mag_db.max()
            sidelobe_db = np.sort(mag_db)[-2]  # second highest
            print(f"{name:12s}: peak={peak_db:.1f} dB, sidelobe={sidelobe_db:.1f} dB, "
                  f"difference={peak_db - sidelobe_db:.1f} dB")

---

**Exercise 3.**
Design a Kaiser window with target sidelobe attenuation of 60 dB using the design formula. Apply it to a signal containing two sine waves at 100 Hz (amplitude 1.0) and 103 Hz (amplitude 0.01) sampled at 1000 Hz for 1 second. Show that the weak 103 Hz signal is visible in the windowed FFT but not in the rectangular-windowed FFT.

??? success "Solution to Exercise 3"

        import numpy as np

        fs = 1000
        t = np.arange(0, 1.0, 1/fs)
        x = 1.0 * np.sin(2*np.pi*100*t) + 0.01 * np.sin(2*np.pi*103*t)

        # Kaiser design for 60 dB
        beta = 0.1102 * (60 - 8.7)  # ~5.65
        w_kaiser = np.kaiser(len(t), beta)

        # Rectangular
        X_rect = np.fft.rfft(x)
        freqs = np.fft.rfftfreq(len(t), 1/fs)
        mag_rect_db = 20 * np.log10(np.abs(X_rect) + 1e-10)

        # Kaiser
        X_kaiser = np.fft.rfft(x * w_kaiser)
        mag_kaiser_db = 20 * np.log10(np.abs(X_kaiser) + 1e-10)

        idx_103 = np.argmin(np.abs(freqs - 103))
        peak_100_rect = mag_rect_db[np.argmin(np.abs(freqs - 100))]
        val_103_rect = mag_rect_db[idx_103]
        val_103_kaiser = mag_kaiser_db[idx_103]

        print(f"Rectangular at 103 Hz: {val_103_rect:.1f} dB (relative peak: {peak_100_rect - val_103_rect:.1f} dB)")
        print(f"Kaiser at 103 Hz:      {val_103_kaiser:.1f} dB")
