# Short-Time Fourier Transform (STFT) and Spectrograms

!!! tip "Mental Model"
    The STFT slides a short window across a signal and computes an FFT for each position, producing a 2D map of frequency vs. time. The result -- a spectrogram -- tells you not just which frequencies are present, but when they appear. The window length controls the trade-off: shorter windows give better time resolution, longer windows give better frequency resolution.

## Understanding the Limitation of Standard FFT

When you apply a standard FFT to a long signal, you get frequency information but **lose all time information**. You cannot tell *when* specific frequencies occur in the signal. This limitation becomes critical when analyzing signals whose frequency content changes over time—like music, speech, or radar signals.

Consider a chirp signal that starts at 1000 Hz and sweeps to 5000 Hz over 2 seconds. A standard FFT of the entire signal would show frequencies between 1000–5000 Hz, but you'd have no idea how the frequency changed with time.

The **Short-Time Fourier Transform (STFT)** solves this problem by:
1. Dividing the signal into short, overlapping time windows
2. Applying a window function to each slice (to reduce spectral leakage)
3. Computing the FFT of each windowed slice
4. Stacking the results to create a time-frequency map called a **spectrogram**

## The STFT Concept

### Mathematical Definition

The STFT of a signal $x(n)$ is defined as:

$$X(m, k) = \sum_{n=0}^{N-1} w(n) \cdot x(n + m \cdot h) \cdot e^{-j2\pi kn/N}$$

where:
- $m$ is the time frame index
- $k$ is the frequency bin index
- $w(n)$ is a window function (Hann, Hamming, etc.)
- $h$ is the hop length (number of samples between successive windows)
- $N$ is the FFT size (window length)

The magnitude $|X(m, k)|$ represents the power at frequency bin $k$ during time frame $m$.

### Sliding Window Approach

The key idea is to:
1. **Extract overlapping segments** from the signal using a sliding window
2. **Apply a window function** to each segment (typically Hann or Hamming to reduce edge artifacts)
3. **Compute the FFT** of each windowed segment
4. **Arrange results** in a 2D array: rows = frequency bins, columns = time frames

**Overlap considerations:**
- 50% overlap is common (hop length = window length / 2)
- More overlap preserves temporal continuity but increases computation
- Less overlap (25% overlap) speeds up computation with minimal quality loss

## Using `scipy.signal.spectrogram()`

SciPy provides a high-level function to compute spectrograms efficiently:

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Generate a chirp signal: frequency sweeps from 100 to 250 Hz
duration = 3
fs = 1000  # sample rate
t = np.linspace(0, duration, int(fs * duration))
x = signal.chirp(t, f0=100, f1=250, t1=duration, method='linear')

# Compute spectrogram
f, t_spec, Sxx = signal.spectrogram(
    x,
    fs=fs,
    window='hann',        # window function
    nperseg=256,          # window length
    noverlap=128,         # overlap (256/2 = 50%)
    nfft=512              # FFT size (zero-padded)
)

# Sxx shape: (n_freqs, n_times)
print(f"Spectrogram shape: {Sxx.shape}")
print(f"Time frames: {len(t_spec)}")
print(f"Frequency bins: {len(f)}")

# Plot
plt.figure(figsize=(12, 6))
plt.pcolormesh(t_spec, f, 10 * np.log10(Sxx + 1e-10), shading='auto', cmap='viridis')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title('Spectrogram of Chirp Signal')
plt.colorbar(label='Power [dB]')
plt.show()
```

**Key parameters:**
- `nperseg`: Window length (number of samples per segment)
- `noverlap`: Number of overlapping samples between adjacent segments
- `window`: Type of window function ('hann', 'hamming', 'blackman', 'kaiser', etc.)
- `nfft`: FFT size (use zero-padding for better frequency resolution)

!!! tip "Parameter Selection"
    - **Longer windows** → better frequency resolution, worse time resolution
    - **Shorter windows** → better time resolution, worse frequency resolution
    - **Zero-padding** (`nfft > nperseg`) → smoother frequency display, doesn't improve actual resolution
    - **More overlap** → smoother transitions between frames

!!! note "The Time-Frequency Tradeoff"
    ```text
    Short window  →  precise time localization,  blurry frequency
    Long window   →  blurry time localization,   precise frequency
    ```
    This is not a limitation of the implementation — it is a fundamental property
    of Fourier analysis (related to the Heisenberg uncertainty principle). You
    cannot have perfect resolution in both domains simultaneously. The window
    length is your dial between the two extremes.

## Manual STFT Implementation

Understanding the mechanics of STFT helps you appreciate what SciPy does under the hood and allows custom implementations:

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def manual_stft(x, fs, nperseg=256, noverlap=128, window='hann', nfft=None):
    """
    Compute STFT manually using a sliding window approach.

    Parameters:
    -----------
    x : 1D array
        Input signal
    fs : float
        Sampling frequency
    nperseg : int
        Window length
    noverlap : int
        Number of overlapping samples
    window : str
        Window type ('hann', 'hamming', 'blackman', etc.)
    nfft : int or None
        FFT size (defaults to nperseg)

    Returns:
    --------
    f : 1D array
        Frequency array
    t_spec : 1D array
        Time array (frame centers)
    Sxx : 2D array (n_freqs, n_times)
        STFT magnitude
    """
    if nfft is None:
        nfft = nperseg

    # Create window function
    w = signal.get_window(window, nperseg)

    # Hop length
    hop = nperseg - noverlap

    # Number of frames
    n_frames = (len(x) - noverlap) // hop

    # Initialize STFT array
    Sxx = np.zeros((nfft // 2 + 1, n_frames), dtype=complex)

    # Sliding window loop
    for m in range(n_frames):
        # Extract segment
        start = m * hop
        end = start + nperseg
        segment = x[start:end]

        # Apply window
        windowed = segment * w

        # Zero-pad if nfft > nperseg
        if nfft > nperseg:
            windowed = np.pad(windowed, (0, nfft - nperseg), mode='constant')

        # Compute FFT
        X = np.fft.fft(windowed)[:nfft // 2 + 1]
        Sxx[:, m] = X

    # Compute frequency and time arrays
    f = np.fft.rfftfreq(nfft, 1 / fs)
    t_spec = np.arange(n_frames) * hop / fs + nperseg / (2 * fs)

    return f, t_spec, np.abs(Sxx)

# Test with chirp signal
duration = 3
fs = 1000
t = np.linspace(0, duration, int(fs * duration))
x = signal.chirp(t, f0=100, f1=250, t1=duration, method='linear')

# Compute manual STFT
f, t_spec, Sxx_manual = manual_stft(x, fs, nperseg=256, noverlap=128, nfft=512)

# Compare with SciPy
from scipy.signal import spectrogram as scipy_spectrogram
f_scipy, t_scipy, Sxx_scipy = scipy_spectrogram(
    x, fs=fs, window='hann', nperseg=256, noverlap=128, nfft=512
)

print(f"Manual STFT shape: {Sxx_manual.shape}")
print(f"SciPy STFT shape: {Sxx_scipy.shape}")
print(f"Results match: {np.allclose(Sxx_manual, Sxx_scipy)}")
```

!!! note "Window Function Impact — Connection to Windowing"
    The window function is critical for reducing **spectral leakage** at segment
    boundaries. Without windowing, the abrupt transitions at segment edges introduce
    artificial high-frequency components. Every STFT implicitly applies a window —
    choosing `window='hann'` vs `'blackman'` trades off frequency resolution against
    sidelobe suppression, exactly as described in the
    [Windowing](windowing.md) section. The window choice in STFT is not
    independent of the window length: together they determine both the time
    resolution and the spectral leakage characteristics of your spectrogram.

## Logarithmic Compression: Converting to Decibels

Raw spectrogram magnitudes have huge dynamic ranges (small values near zero, large peaks). Visualizing on a linear scale compresses small values into invisibility. The solution is **logarithmic compression** using the decibel scale:

$$S_{\text{dB}}(m, k) = 20 \log_{10}\left(\frac{|X(m, k)|}{\max(|X(m, k)|)}\right)$$

```python
# Convert magnitude spectrogram to dB
Sxx_db = 20 * np.log10(Sxx / np.max(Sxx) + 1e-10)

# Typical dynamic range: -80 dB to 0 dB
# You can clip to a smaller range for visualization
Sxx_db = np.clip(Sxx_db, -80, 0)

print(f"dB range: {Sxx_db.min():.1f} to {Sxx_db.max():.1f} dB")
```

**Why decibels matter:**
- Human hearing perceives loudness logarithmically
- dB scale reveals quiet but important signals masked by peaks
- Standard dynamic range: -80 dB to 0 dB (relative to max)
- You can adjust the floor for your application

```python
def power_to_db(S, ref=1.0, min_db=-80):
    """Convert power spectrogram to decibels."""
    S_db = 10 * np.log10(np.maximum(S, 1e-10) / ref**2)
    S_db = np.maximum(S_db, min_db)
    return S_db

# For magnitude (not power), use 20 * log10
def magnitude_to_db(S, ref=1.0, min_db=-80):
    """Convert magnitude spectrogram to decibels."""
    S_db = 20 * np.log10(np.maximum(S, 1e-10) / ref)
    S_db = np.maximum(S_db, min_db)
    return S_db
```

## Visualization: Two Approaches

### Using `imshow()` (Rectangular Pixels)

```python
plt.figure(figsize=(12, 6))
extent = [t_spec[0], t_spec[-1], f[0], f[-1]]
plt.imshow(Sxx_db, aspect='auto', origin='lower', extent=extent,
           cmap='viridis', interpolation='nearest')
plt.xlabel('Time [sec]')
plt.ylabel('Frequency [Hz]')
plt.title('Spectrogram (imshow)')
plt.colorbar(label='Power [dB]')
plt.show()
```

### Using `pcolormesh()` (Flexible Mesh)

```python
plt.figure(figsize=(12, 6))
plt.pcolormesh(t_spec, f, Sxx_db, shading='auto', cmap='viridis')
plt.xlabel('Time [sec]')
plt.ylabel('Frequency [Hz]')
plt.title('Spectrogram (pcolormesh)')
plt.colorbar(label='Power [dB]')
plt.show()
```

**Comparison:**
- `imshow()`: Assumes uniform grid, simpler syntax
- `pcolormesh()`: More flexible for non-uniform grids, handles irregular time spacing

!!! tip "Colormap Selection"
    - `viridis`: Perceptually uniform, colorblind-friendly
    - `magma`, `inferno`: High contrast, good for small dynamic ranges
    - `jet`: Avoid (perceptually non-linear), but familiar to some users
    - Custom colormaps: Use `matplotlib.colors.ListedColormap()`

## Practical Example: Analyzing a Chirp Signal

```python
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Generate chirp: frequency ramps from 200 Hz to 500 Hz over 5 seconds
duration = 5
fs = 2000
t = np.linspace(0, duration, int(fs * duration))
x = signal.chirp(t, f0=200, f1=500, t1=duration, method='linear')

# Add noise to make it realistic
np.random.seed(42)
x += 0.1 * np.random.randn(len(x))

# Compute spectrogram with different parameters
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# High time resolution (short windows)
f1, t1, Sxx1 = signal.spectrogram(x, fs=fs, nperseg=128, noverlap=64)
ax = axes[0, 0]
ax.pcolormesh(t1, f1, 20*np.log10(Sxx1+1e-10), shading='auto', cmap='viridis')
ax.set_title('High Time Resolution (nperseg=128)')
ax.set_ylabel('Frequency [Hz]')

# High frequency resolution (long windows)
f2, t2, Sxx2 = signal.spectrogram(x, fs=fs, nperseg=1024, noverlap=512)
ax = axes[0, 1]
ax.pcolormesh(t2, f2, 20*np.log10(Sxx2+1e-10), shading='auto', cmap='viridis')
ax.set_title('High Frequency Resolution (nperseg=1024)')
ax.set_ylabel('Frequency [Hz]')

# With zero-padding
f3, t3, Sxx3 = signal.spectrogram(x, fs=fs, nperseg=256, noverlap=128, nfft=1024)
ax = axes[1, 0]
ax.pcolormesh(t3, f3, 20*np.log10(Sxx3+1e-10), shading='auto', cmap='viridis')
ax.set_title('With Zero-Padding (nfft=1024)')
ax.set_ylabel('Frequency [Hz]')
ax.set_xlabel('Time [sec]')

# Different window function
f4, t4, Sxx4 = signal.spectrogram(x, fs=fs, nperseg=512, noverlap=256, window='blackman')
ax = axes[1, 1]
ax.pcolormesh(t4, f4, 20*np.log10(Sxx4+1e-10), shading='auto', cmap='viridis')
ax.set_title('With Blackman Window (nperseg=512)')
ax.set_ylabel('Frequency [Hz]')
ax.set_xlabel('Time [sec]')

plt.tight_layout()
plt.show()

# Print analysis
print(f"Theoretical frequency sweep: {200} Hz → {500} Hz")
print(f"Duration: {duration} seconds")
print(f"Expected slope: {(500-200)/duration:.1f} Hz/s")
```

**Expected output:** A clear diagonal line in the spectrogram rising from 200 Hz to 500 Hz, visualizing the frequency sweep.

## Advanced: Custom STFT with Different Windows Per Frame

For some applications, you might want to experiment with adaptive parameters:

```python
def adaptive_stft(x, fs, target_bw=10, min_win=128, max_win=2048):
    """
    STFT with adaptive window size based on target bandwidth.

    Lower frequencies need longer windows for better resolution.
    This is a simplified approach; see librosa for production code.
    """
    # Adaptive logic: use longer windows for better frequency resolution
    # In practice, use constant window size for consistency

    results = []
    hop = target_bw  # Hz → samples conversion

    for center_freq in np.arange(100, 500, target_bw):
        # For each frequency band, could theoretically use different window
        # In practice, constant window is more common
        pass

    return results

# For production audio/speech processing, use librosa:
# import librosa
# D = librosa.stft(x)
# S = np.abs(D)
# S_db = librosa.power_to_db(S)
```

## Summary

- **STFT** solves FFT's time-frequency trade-off by analyzing overlapping windows
- **Window size** trades time vs. frequency resolution; no universal optimal choice
- **`scipy.signal.spectrogram()`** handles all complexity with sensible defaults
- **Logarithmic compression** (dB scale) reveals details across dynamic ranges
- **Visualization** via `pcolormesh()` or `imshow()` clearly shows time-frequency structure

Next topic: **Windowing** explores how window functions reduce spectral leakage artifacts and why they matter for clean spectrograms.

---

## Exercises

**Exercise 1.**
Generate a signal that is a 200 Hz sine for the first 1.5 seconds and a 400 Hz sine for the remaining 1.5 seconds (sample rate 2000 Hz). Compute the spectrogram with `scipy.signal.spectrogram` using `nperseg=256` and `noverlap=128`. Verify that the spectrogram shows two distinct horizontal bands at 200 Hz and 400 Hz in their respective time intervals.

??? success "Solution to Exercise 1"

        import numpy as np
        from scipy import signal

        fs = 2000
        t = np.arange(0, 3, 1/fs)
        x = np.where(t < 1.5,
                      np.sin(2*np.pi*200*t),
                      np.sin(2*np.pi*400*t))

        f, t_spec, Sxx = signal.spectrogram(x, fs=fs, nperseg=256, noverlap=128)

        # Check that 200 Hz dominates in first half
        mid_time = len(t_spec) // 2
        peak_first = f[np.argmax(Sxx[:, mid_time // 2])]
        peak_second = f[np.argmax(Sxx[:, mid_time + mid_time // 2])]
        print(f"First half peak: {peak_first:.0f} Hz")   # ~200
        print(f"Second half peak: {peak_second:.0f} Hz") # ~400

---

**Exercise 2.**
Using the chirp signal from `scipy.signal.chirp` (100 Hz to 500 Hz over 3 seconds, sample rate 2000 Hz), compute two spectrograms: one with `nperseg=64` (high time resolution) and one with `nperseg=512` (high frequency resolution). Compare the two and explain which one more clearly shows the chirp's instantaneous frequency versus which one has a thinner frequency trace.

??? success "Solution to Exercise 2"

        import numpy as np
        from scipy import signal

        fs = 2000
        duration = 3
        t = np.linspace(0, duration, int(fs * duration))
        x = signal.chirp(t, f0=100, f1=500, t1=duration)

        f1, t1, Sxx1 = signal.spectrogram(x, fs=fs, nperseg=64, noverlap=32)
        f2, t2, Sxx2 = signal.spectrogram(x, fs=fs, nperseg=512, noverlap=256)

        print(f"Short window: {Sxx1.shape} (time frames={len(t1)}, freq bins={len(f1)})")
        print(f"Long window:  {Sxx2.shape} (time frames={len(t2)}, freq bins={len(f2)})")
        # Short window -> more time frames, fewer freq bins -> better time resolution
        # Long window -> fewer time frames, more freq bins -> thinner freq trace

---

**Exercise 3.**
Implement a manual STFT function that takes a signal, window length, hop length, and window type, and returns the magnitude spectrogram. Test it on a 500 Hz sine wave (sample rate 4000 Hz, duration 1 second) using a Hann window of length 256 and hop length 64. Verify that the peak frequency bin corresponds to 500 Hz.

??? success "Solution to Exercise 3"

        import numpy as np
        from scipy.signal import get_window

        def manual_stft(x, fs, nperseg, hop, window='hann'):
            w = get_window(window, nperseg)
            n_frames = (len(x) - nperseg) // hop + 1
            nfft = nperseg
            Sxx = np.zeros((nfft // 2 + 1, n_frames))
            for m in range(n_frames):
                start = m * hop
                segment = x[start:start + nperseg] * w
                X = np.fft.rfft(segment)
                Sxx[:, m] = np.abs(X)
            f = np.fft.rfftfreq(nfft, 1/fs)
            return f, Sxx

        fs = 4000
        t = np.arange(0, 1, 1/fs)
        x = np.sin(2*np.pi*500*t)

        f, Sxx = manual_stft(x, fs, nperseg=256, hop=64)
        peak_freq = f[np.argmax(Sxx.mean(axis=1))]
        print(f"Peak frequency: {peak_freq:.0f} Hz")  # 500
