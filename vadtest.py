
SAMPLING_RATE = 16000

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import torch
import os


import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import sounddevice as sd
import numpy as np

def show_vad(wav, start_time, end_time):
    ## 画出幅值图
    plt.plot(np.arange(len(wav))/SAMPLING_RATE, wav)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform')

    plt.axvline(x=start_time/1000, color='r', linestyle='--')
    plt.axvline(x=end_time/1000, color='r', linestyle='--')

    axplay = plt.axes([0.6, 0.0, 0.1, 0.06])
    bplay = Button(axplay, 'Play')
    def play(event):
        sd.play(wav, SAMPLING_RATE)
    bplay.on_clicked(play)

    axvplay = plt.axes([0.71, 0.0, 0.1, 0.06])
    vbplay = Button(axvplay, 'VAD')
    def vplay(event):
        sd.play(wav[int(start_time/1000*16000):int(end_time/1000*16000)], SAMPLING_RATE)
    vbplay.on_clicked(vplay)
    
    axstop = plt.axes([0.82, 0.0, 0.1, 0.06])
    bstop = Button(axstop, 'Stop')
    def stop(event):
        sd.stop()
    bstop.on_clicked(stop)

    plt.show()

def silero_vad(model, filepath, threshold_score, threshold_start_count, threshold_end_count, win_size=512, logger=True):
    wav = read_audio(filepath, sampling_rate=SAMPLING_RATE)
    speech_probs = []
    start_count = 0
    end_count = 0
    started = False
    if logger: print(f"file: {filepath}")
    for i in range(0, len(wav), win_size):
        if len(wav) < i+win_size:
            break
        chunk = wav[i: i+win_size]
        speech_prob = model(chunk, SAMPLING_RATE).item()
        speech_probs.append(speech_prob)

        if not started:
            if(speech_prob >= threshold_score):
                start_count += 1
                end_count = 0
            else:
                start_count = 0
            if(start_count >= threshold_start_count): 
                start_time = (i-8*win_size)/16000 * 1000;
                if logger: print(f'  start: {start_time}ms')
                started = True
        else:
            if(speech_prob < threshold_score):
                end_count += 1
            else:
                end_count = 0
            if(end_count >= threshold_end_count): 
                end_time = i/16000 * 1000
                if logger: print(f'  end: {end_time}ms')
                break
    model.reset_states()
    return wav, start_time, end_time


  
wav_dir = "./samples"
output_dir = "./"
SHOW_UI = False

torch.set_num_threads(1)
model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=True,
                              onnx=False)
(get_speech_timestamps,
 save_audio,
 read_audio,
 VADIterator,
 collect_chunks) = utils

with open(os.path.join(output_dir, "result.csv"), "w+") as f:
    f.write('filename,vad_start,vad_end\n')
    for root, dirs, files in os.walk(wav_dir):
        for filename in files:
            if not filename.endswith("wav"): continue

            wav, start_time, end_time = silero_vad(model, os.path.join(root, filename), 0.8, 4, 8)

            f.write(f'{filename},{start_time},{end_time}\n')

            if SHOW_UI: 
                show_vad(wav, start_time, end_time)
                


