import sys
from scipy.signal import medfilt
import numpy as np
import matplotlib.pyplot as plt


def main():
    t = np.arange(0, 200, 0.1)
    raw_data = np.sin(t) + (np.random.randn(2000)*0.2)
    filtered_data = medfilt(raw_data, 9)

    plot(raw_data, filtered_data)

def plot(raw_data, filtered_data, range=200):
    _, axs = plt.subplots(2, 1) 

    axs[0].plot(np.arange(range), raw_data[:range], 'C0')
    axs[0].set_title('Raw data')

    axs[1].plot(np.arange(range), filtered_data[:range], 'C1')
    axs[1].set_title('Filtered data')

    plt.show()

if __name__ == '__main__':
    main()

