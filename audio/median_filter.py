import sys
import matplotlib.pyplot as plt
from scipy.io.wavfile import read
from scipy.signal import medfilt


def main(wav_file):
    raw_data = read(wav_file)
    filtered_data = medfilt(raw_data[1], 5)

    plot(raw_data, filtered_data)

def plot(raw_data, filtered_data):
    fig, axs = plt.subplots(1, 2) 

    axs[0].plot(raw_data[1][:200])
    axs[0].set_title('Raw data')

    axs[1].plot(filtered_data[:200])
    axs[1].set_title('Filtered data')

    plt.show()

if __name__ == '__main__':
    main(sys.argv[1])

