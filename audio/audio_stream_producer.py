import sys
import signal
import threading
import pyaudio
from six.moves import queue
import logging
import contextlib
import wave

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

logger = logging.getLogger('AudioStreamProducer')
handler = logging.StreamHandler()
formatter = logging.Formatter(
     '%(asctime)s %(levelname)-4s %(threadName)s %(name)s %(message)s'
     )
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO) 

def open_audio_stream(audio_interface):
    return audio_interface.open(
        format=pyaudio.paInt16,
        channels=1, rate=RATE,
            input=True, frames_per_buffer=CHUNK,
    )

class AudioStreamProducer(threading.Thread):
    def __init__(self):
        super(AudioStreamProducer, self).__init__()
        self.buff = queue.Queue()
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = open_audio_stream(self.audio_interface)
        self.shouldRun = True
        self.shouldPause = False
        self.buckupFrames = []

    def run(self):
        logger.info('Run')
        try:
            while self.shouldRun:
                a = self.audio_stream.read(CHUNK)
                if not self.shouldPause: # Skip if PAUSEd
                    if not a is None and len(a) > 0:
                        self.buff.put(a)
        except (Exception) as e:
            print(e)
        finally:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            self.audio_interface.terminate()
            logger.info('Terminated')

    @contextlib.contextmanager
    def audio_data_generator(self):
        yield self.get_audio_data()

    def get_audio_data(self):
        while self.shouldRun:
            # if not self.shouldPause: # Skip if PAUSEd
            chunk = self.buff.get()
            if not chunk:
                break

            self.buckupFrames.append(chunk)

            yield chunk

    def pause(self):
        if not self.shouldRun:
            logger.warning('Pause failed (Already terminated)')
            return

        if self.shouldPause:
            return # Already paused

        logger.info('Pausing...')
        self.shouldPause = True

    def resume(self):
        if not self.shouldRun:
            logger.warning('Resume failed (Already terminated)')
            return

        if not self.shouldPause:
            return # Already resumed

        logger.info('Resuming...')
        self.shouldPause = False

    def shutdown(self, signal=None, frame=None):
        logger.info('Shutting down...')
        self.save_to_wav()
        self.shouldRun = False

    def save_to_wav(self):
        waveFile = wave.open('sample.wav', 'wb')
        waveFile.setnchannels(1)
        waveFile.setsampwidth(self.audio_interface.get_sample_size(pyaudio.paInt16))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(self.buckupFrames))
        waveFile.close()


if __name__ == "__main__":

    # audio stream acquisition test
    ap = AudioStreamProducer()
    ap.setDaemon(True)
    ap.start()

    signal.signal(signal.SIGINT, ap.shutdown)

    d = ap.get_audio_data()
    for i in d:
        logger.info('audio: %s' % i)

    # from time import sleep
    # sleep(2)
    # a.resume()

    # sleep(2)
    # a.shutdown()
    print('Main finished')
