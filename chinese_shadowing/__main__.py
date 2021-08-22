import time
import numpy as np
import pandas as pd
import tkinter as tk
from chinese_shadowing.config import path_csv
from chinese_shadowing.config import path_data
from chinese_shadowing.play_audio import get_mp3_audio
from chinese_shadowing.record_audio import Recorder
from chinese_shadowing.utilities import define_option_menu
from chinese_shadowing.play_audio import PlayAudioThread


if __name__ == '__main__':
    master = tk.Tk()

    df = pd.read_csv(path_csv, index_col=0)
    hsk_to_indexes = {i: df.index[df['hsk'] == i].tolist() for i in range(1, 7)}

    chinese_sentence_box = tk.Label(master, text=df['simplified'][0])  # todo toggle simplified/traditional
    chinese_sentence_box.config(font=("Segoe UI", 20))  # todo add buttons
    chinese_sentence_box.pack()

    pinyin_sentence_box = tk.Label(master, text=df['pinyin'][0])  # todo toggle visibility h
    pinyin_sentence_box.config(font=("Segoe UI", 20))  # todo add buttons
    pinyin_sentence_box.pack()

    meaning_sentence_box = tk.Label(master, text=df['meaning'][0])
    meaning_sentence_box.config(font=("Segoe UI", 20))
    meaning_sentence_box.pack()

    hsk_option = ['HSK1', 'HSK2', 'HSK3', 'HSK4', 'HSK5', 'HSK6']
    from_hsk_box = tk.Label(master, text='From')
    from_hsk_box.config(font=("Segoe UI", 15))
    from_hsk_box.pack()
    from_hsk_menu, from_hsk_variable = define_option_menu(master=master, option_list=hsk_option, default_index=0)
    to_hsk_box = tk.Label(master, text='From')
    to_hsk_box.config(font=("Segoe UI", 15))
    to_hsk_box.pack()
    to_hsk_menu, to_hsk_variable = define_option_menu(master=master, option_list=hsk_option, default_index=5)  # futur constraint the options

    sentence_index = tk.IntVar(master)
    sentence_index.set(0)

    # New sentence
    def change_sentence(event=None):
        low = int(from_hsk_variable.get()[-1])
        high = int(to_hsk_variable.get()[-1])

        indexes = sum((hsk_to_indexes[i] for i in range(low, high + 1)), [])
        sentence_index.set(np.random.choice(indexes))

        chinese_sentence_box['text'] = df['simplified'][sentence_index.get()]
        pinyin_sentence_box['text'] = df['pinyin'][sentence_index.get()]
        meaning_sentence_box['text'] = df['meaning'][sentence_index.get()]
    master.bind("<KeyPress-h>", change_sentence)

    # Record
    recorder = Recorder()
    master.bind("<KeyPress-k>", recorder.start)
    master.bind("<KeyRelease-k>", recorder.stop)

    # Play recording
    def play_recording(event=None):
        print(f'{time.time()} play recording')
        if recorder.result is not None:
            audio, frame_rate, channels = recorder.result
            thread = PlayAudioThread(audio, frame_rate, channels)
            thread.start()
    master.bind("<KeyPress-l>", play_recording)

    # Play file
    def play_file(event=None):
        print(f'{time.time()} play file')
        path_mp3 = (path_data / str(sentence_index.get())).with_suffix('.mp3')
        audio, frame_rate, channels = get_mp3_audio(path_mp3)
        thread = PlayAudioThread(audio, frame_rate, channels)
        thread.start()
    master.bind("<KeyPress-j>", play_file)

    keyboard_shortcuts_box = tk.Label(master, text="H => Change sentence \n J => Listen file \n K => Record \n L => Listen recording")
    keyboard_shortcuts_box.config(font=("Segoe UI", 15))
    keyboard_shortcuts_box.pack()

    master.mainloop()  # todo add buttons

