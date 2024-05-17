import numpy as np
import librosa

# Lista de frequências das notas para cada oitava
notas_freqs = [
    ('C0', 16.352), ('C#0/Db0', 17.324), ('D0', 18.354), ('D#0/Eb0', 19.445), ('E0', 20.602), ('F0', 21.827), ('F#0/Gb0',
                                                                                                               23.125), ('G0', 24.500), ('G#0/Ab0', 25.957), ('A0', 27.500), ('A#0/Bb0', 29.136), ('B0', 30.868),
    ('C1', 32.703), ('C#1/Db1', 34.648), ('D1', 36.708), ('D#1/Eb1', 38.891), ('E1', 41.203), ('F1', 43.654), ('F#1/Gb1',
                                                                                                               46.249), ('G1', 48.999), ('G#1/Ab1', 51.913), ('A1', 55.000), ('A#1/Bb1', 58.270), ('B1', 61.735),
    ('C2', 65.406), ('C#2/Db2', 69.296), ('D2', 73.416), ('D#2/Eb2', 77.782), ('E2', 82.407), ('F2', 87.307), ('F#2/Gb2',
                                                                                                               92.499), ('G2', 97.999), ('G#2/Ab2', 103.826), ('A2', 110.000), ('A#2/Bb2', 116.541), ('B2', 123.471),
    ('C3', 130.813), ('C#3/Db3', 138.591), ('D3', 146.832), ('D#3/Eb3', 155.563), ('E3', 164.814), ('F3', 174.614), ('F#3/Gb3',
                                                                                                                     184.997), ('G3', 195.998), ('G#3/Ab3', 207.652), ('A3', 220.000), ('A#3/Bb3', 233.082), ('B3', 246.942),
    ('C4', 261.626), ('C#4/Db4', 277.183), ('D4', 293.665), ('D#4/Eb4', 311.127), ('E4', 329.628), ('F4', 349.228), ('F#4/Gb4',
                                                                                                                     369.994), ('G4', 391.995), ('G#4/Ab4', 415.305), ('A4', 440.000), ('A#4/Bb4', 466.164), ('B4', 493.883),
    ('C5', 523.251), ('C#5/Db5', 554.365), ('D5', 587.330), ('D#5/Eb5', 622.254), ('E5', 659.255), ('F5', 698.456), ('F#5/Gb5',
                                                                                                                     739.989), ('G5', 783.991), ('G#5/Ab5', 830.609), ('A5', 880.000), ('A#5/Bb5', 932.328), ('B5', 987.767),
    ('C6', 1046.502), ('C#6/Db6', 1108.731), ('D6', 1174.659), ('D#6/Eb6', 1244.508), ('E6', 1318.510), ('F6', 1396.913), ('F#6/Gb6',
                                                                                                                           1479.978), ('G6', 1567.982), ('G#6/Ab6', 1661.219), ('A6', 1760.000), ('A#6/Bb6', 1864.655), ('B6', 1975.533),
    ('C7', 2093.005), ('C#7/Db7', 2217.461), ('D7', 2349.318), ('D#7/Eb7', 2489.016), ('E7', 2637.020), ('F7', 2793.826), ('F#7/Gb7',
                                                                                                                           2959.955), ('G7', 3135.964), ('G#7/Ab7', 3322.438), ('A7', 3520.000), ('A#7/Bb7', 3729.310), ('B7', 3951.066),
    ('C8', 4186.009), ('C#8/Db8', 4434.922), ('D8', 4698.636), ('D#8/Eb8', 4978.032), ('E8', 5274.041), ('F8', 5587.652), ('F#8/Gb8',
                                                                                                                           5919.910), ('G8', 6271.928), ('G#8/Ab8', 6644.875), ('A8', 7040.000), ('A#8/Bb8', 7458.620), ('B8', 7902.133),
    ('C9', 8372.018), ('C#9/Db9', 8869.844), ('D9', 9397.272), ('D#9/Eb9', 9956.064), ('E9', 10548.082), ('F9', 11175.304), ('F#9/Gb9',
                                                                                                                             11839.820), ('G9', 12543.856), ('G#9/Ab9', 13289.750), ('A9', 14080.000), ('A#9/Bb9', 14917.240), ('B9', 15804.266),
    ('C10', 16744.036), ('C#10/Db10', 17739.688), ('D10', 18794.545), ('D#10/Eb10', 19912.128), ('E10', 21096.164), ('F10', 22350.609), ('F#10/Gb10',
                                                                                                                                         23679.640), ('G10', 25087.712), ('G#10/Ab10', 26579.500), ('A10', 28160.000), ('A#10/Bb10', 29834.480), ('B10', 31608.532),
]


def nota_musical(frequencia):
    nota_mais_proxima = min(
        notas_freqs, key=lambda nota: abs(frequencia - nota[1]))
    return nota_mais_proxima[0]


def print_audio_frequencies(audio_path):
    # Carregar o arquivo de áudio
    y, sr = librosa.load(audio_path, sr=None)

    # Define os parâmetros para a STFT com uma janela de amostragem maior
    n_fft = 2**14  # Aumentando o tamanho da janela de amostragem
    hop_length = 2**12  # Ajustando o hop length para 1 segundo

    # Processa o áudio em segmentos de 1 segundo
    for i in range(0, len(y), sr):
        segmento = y[i:i + sr]

        # Calcula a STFT do segmento de áudio
        D = np.abs(librosa.stft(segmento, n_fft=n_fft, hop_length=hop_length))

        # Frequências correspondentes aos bins da FFT
        freqs = librosa.fft_frequencies(sr=sr, n_fft=n_fft)

        # Calcula os tempos correspondentes às colunas da STFT
        times = librosa.frames_to_time(
            np.arange(D.shape[1]), sr=sr, hop_length=hop_length)
        #t = zip(times)
        # Encontrar a frequência dominante no segmento
        if D.shape[1] > 0:
            mag = np.mean(D, axis=1)
            dominant_freq = freqs[np.argmax(mag)]
            print(
                f"Tempo: {i/sr:.2f}s, Frequência dominante: {dominant_freq:.2f}Hz, Nota: {nota_musical(dominant_freq)}")


# Caminho para o arquivo de áudio
audio_path = 'afinacao-padrao-do-violao.wav'
print_audio_frequencies(audio_path)
