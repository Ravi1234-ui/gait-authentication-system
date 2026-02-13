import numpy as np
from scipy.signal import butter, filtfilt

FS = 50  # sampling frequency
WINDOW_SIZE = 128
STEP = 64


def butter_lowpass(cutoff, order=3):
    nyq = 0.5 * FS
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low")
    return b, a


def lowpass_filter(signal, cutoff):
    b, a = butter_lowpass(cutoff)
    return filtfilt(b, a, signal)


def separate_gravity(acc):
    gravity = lowpass_filter(acc, cutoff=0.3)
    body = acc - gravity
    return body


def sliding_window(signal):
    windows = []
    for i in range(0, len(signal) - WINDOW_SIZE, STEP):
        windows.append(signal[i:i + WINDOW_SIZE])
    return np.array(windows)
