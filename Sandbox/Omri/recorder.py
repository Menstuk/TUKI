import pyaudio
import wave
import pathlib
import threading as th
import time

keep_going = True

def key_capture_thread():
    global keep_going
    input()
    keep_going = False

def record(output_path: pathlib.Path):

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []

    print('Press ENTER to stop recording')
    th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
    dots = 0
    while keep_going:
        data = stream.read(1024)
        frames.append(data)
        print('\rRecording' + dots * '.', end='')
        dots += 1
        if dots == 4:
            dots = 0
    print("\r")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    filename = "check2.m4a"
    full_path = output_path / filename
    sound_file = wave.open(full_path.as_posix(), "wb")
    sound_file.setnchannels(1)
    sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    sound_file.setframerate(44100)
    sound_file.writeframes(b''.join(frames))
    sound_file.close()

    return full_path

if __name__ == '__main__':
    file = record(pathlib.Path("E:/project_tests"))
    print(file)