import wave
import struct
import math

def save_wav(filename, samples, sample_rate=44100):
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for sample in samples:
            wav_file.writeframes(struct.pack('h', int(sample * 32767.0)))

def generate_shoot():
    samples = []
    # Pitch sweep down
    for i in range(10000):
        t = i / 44100.0
        freq = 800 - (t * 4000)
        if freq < 100: freq = 100
        val = math.sin(2.0 * math.pi * freq * t)
        # envelope
        env = max(0, 1.0 - (i / 10000.0))
        samples.append(val * env * 0.5)
    save_wav('assets/sounds/shoot.wav', samples)

def generate_hit():
    samples = []
    for i in range(5000):
        t = i / 44100.0
        freq = 1200
        val = math.sin(2.0 * math.pi * freq * t)
        env = max(0, 1.0 - (i / 5000.0))
        samples.append(val * env * 0.5)
    save_wav('assets/sounds/hit.wav', samples)

def generate_miss():
    samples = []
    for i in range(8000):
        t = i / 44100.0
        freq = 150
        val = math.sin(2.0 * math.pi * freq * t)
        env = max(0, 1.0 - (i / 8000.0))
        samples.append(val * env * 0.5)
    save_wav('assets/sounds/miss.wav', samples)

def generate_powerup():
    samples = []
    notes = [400, 500, 600, 800]
    for note in notes:
        for i in range(5000):
            t = i / 44100.0
            val = math.sin(2.0 * math.pi * note * t)
            env = max(0, 1.0 - (i / 5000.0))
            samples.append(val * env * 0.5)
    save_wav('assets/sounds/powerup.wav', samples)

if __name__ == "__main__":
    generate_shoot()
    generate_hit()
    generate_miss()
    generate_powerup()
    print("Sounds generated!")
