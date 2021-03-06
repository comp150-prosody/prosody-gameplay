from sys import byteorder
from array import array
from struct import pack


import pyaudio
import wave
import sys
import scipy.io.wavfile

sys.path.append("./api")
import Vokaturi

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
RATE = 44100

def is_silent(snd_data):
    "Returns 'True' if below the 'silent' threshold"
    return max(snd_data) < THRESHOLD

def normalize(snd_data):
    "Average the volume out"
    MAXIMUM = 16384
    times = float(MAXIMUM)/max(abs(i) for i in snd_data)

    r = array('h')
    for i in snd_data:
        r.append(int(i*times))
    return r

def trim(snd_data):
    "Trim the blank spots at the start and end"
    def _trim(snd_data):
        snd_started = False
        r = array('h')

        for i in snd_data:
            if not snd_started and abs(i)>THRESHOLD:
                snd_started = True
                r.append(i)

            elif snd_started:
                r.append(i)
        return r

    # Trim to the left
    snd_data = _trim(snd_data)

    # Trim to the right
    snd_data.reverse()
    snd_data = _trim(snd_data)
    snd_data.reverse()
    return snd_data

def add_silence(snd_data, seconds):
    "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
    r = array('h', [0 for i in range(int(seconds*RATE))])
    r.extend(snd_data)
    r.extend([0 for i in range(int(seconds*RATE))])
    return r

def record():
    """
    Record a word or words from the microphone and
    return the data as an array of signed shorts.

    Normalizes the audio, trims silence from the
    start and end, and pads with 0.5 seconds of
    blank sound to make sure VLC et al can play
    it without getting chopped off.
    """
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=RATE,
        input=True, output=True,
        frames_per_buffer=CHUNK_SIZE)

    num_silent = 0
    snd_started = False

    r = array('h')

    while 1:
        # little endian, signed short
        snd_data = array('h', stream.read(CHUNK_SIZE))
        if byteorder == 'big':
            snd_data.byteswap()
        r.extend(snd_data)

        silent = is_silent(snd_data)

        if silent and snd_started:
            num_silent += 1
        elif not silent and not snd_started:
            snd_started = True

        if snd_started and num_silent > 30:
            break

    sample_width = p.get_sample_size(FORMAT)
    stream.stop_stream()
    stream.close()
    p.terminate()

    r = normalize(r)
    r = trim(r)
    r = add_silence(r, 0.5)
    return sample_width, r

def record_to_file(path):
    "Records from the microphone and outputs the resulting data to 'path'"
    sample_width, data = record()
    data = pack('<' + ('h'*len(data)), *data)

    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(RATE)
    wf.writeframes(data)
    wf.close()

def analyzeFile(filepath, lineNum):
    print("in analyzeFile 1")
    Vokaturi.load("./lib/Vokaturi_mac.so")

    (sample_rate, samples) = scipy.io.wavfile.read(filepath)

    print("in analyzeFile 2")
    buffer_length = len(samples)
    c_buffer = Vokaturi.SampleArrayC(buffer_length)
    if samples.ndim == 1:  # mono
            c_buffer[:] = samples[:] / 32768.0
    else:  # stereo
            c_buffer[:] = 0.5*(samples[:,0]+0.0+samples[:,1]) / 32768.0

    voice = Vokaturi.Voice (sample_rate, buffer_length)
    print("in analyzeFile 3")

    voice.fill(buffer_length, c_buffer)

    quality = Vokaturi.Quality()
    emotionProbabilities = Vokaturi.EmotionProbabilities()
    voice.extract(quality, emotionProbabilities)
    print("in analyzeFile 4")


    if quality.valid:
        emotions = [
                emotionProbabilities.happiness,
                emotionProbabilities.sadness,
                emotionProbabilities.anger,
                emotionProbabilities.fear,
                emotionProbabilities.neutrality]


        if max(emotions) == emotionProbabilities.happiness:
            maxEmotion = "Happy"
        elif max(emotions) == emotionProbabilities.sadness:
            maxEmotion = "Sad"
        elif max(emotions) == emotionProbabilities.anger:
            maxEmotion = "Angry"
        elif max(emotions) == emotionProbabilities.neutrality:
            maxEmotion = "Neut"
        else:
            maxEmotion = "Afraid"

        stats = ("Happy: %.3f\tSad: %.3f\tAngry %.3f\tFear %.3f\tNeut %.3f" % (emotions[0], emotions[1], emotions[2], emotions[3], emotions[4]))

        print("in analyzeFile 5")
        emotionFile = open("emotions", 'a')
        print("in analyzeFile 6")
        writeEmotions(emotionFile, maxEmotion + " " + stats, lineNum)
        print("in analyzeFile 7")
        emotionFile.close()
        print("in analyzeFile 8")


    else:
        print ("Not enough sonorancy to determine emotions")


def writeEmotions(emotionFile, emotion, lineNum):
    output = str(lineNum) + " " + emotion + "\n"
    emotionFile.write(output)


def run():
    lineNum = 0
    while 1:
        print("please speak into the microphone")
        record_to_file('demo.wav')
        analyzeFile('demo.wav', lineNum)
        print("file recorded")
        lineNum += 1


if __name__ == '__main__':
    run()


