import os
import threading
import pygame
import random
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from mutagen import File
from PIL import Image, ImageTk
from time import sleep

class MusicPlayer:
    def __init__(self, master):
        self.master = master
        self.master.title("Music Player")
        self.master.geometry("1000x640")
        self.master.minsize(1000, 640)
        self.playlist = []
        self.current_song_index = 0
        self.is_playing = False
        self.loop_mode = "No Loop"
        self.duration = 0
        pygame.mixer.init()
        self.setup_ui()

    def setup_ui(self):
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=0)
        self.master.columnconfigure(2, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.master.rowconfigure(1, weight=0)
        self.playlist_frame = ttk.Frame(self.master)
        self.playlist_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.playlist_box = tk.Listbox(self.playlist_frame, selectmode=tk.SINGLE, width=50)
        self.playlist_box.pack(padx=20, fill=tk.BOTH, expand=True)
        self.loop_mode_var = tk.StringVar(value="No Loop")
        self.loop_options = ["No Loop", "Single Loop", "Loop All"]
        self.loop_dropdown = ttk.Combobox(self.playlist_frame, textvariable=self.loop_mode_var, values=self.loop_options, state="readonly")
        self.loop_dropdown.pack(pady=5)
        self.current_time_label = tk.Label(self.playlist_frame, text="00:00:00")
        self.current_time_label.pack(side=tk.LEFT, padx=5)
        self.duration_label = tk.Label(self.playlist_frame, text="00:00:00")
        self.duration_label.pack(side=tk.RIGHT, padx=5)
        self.current_time_slider = tk.Scale(self.playlist_frame, from_=0, to=100, orient=tk.HORIZONTAL, state='disabled', length=400)
        self.current_time_slider.pack(pady=10, fill=tk.X)
        self.current_time_slider.bind("<Motion>", self.seek_song)
        self.control_frame = ttk.Frame(self.master)
        self.control_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        for i in range(8):
            self.control_frame.columnconfigure(i, weight=1)
        self.play_button = ttk.Button(self.control_frame, text="Play", command=self.play_song, width=15)
        self.play_button.grid(row=0, column=0, padx=5, pady=5)
        self.pause_button = ttk.Button(self.control_frame, text="Pause", command=self.pause_song, width=15)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)
        self.stop_button = ttk.Button(self.control_frame, text="Stop", command=self.stop_song, width=15)
        self.stop_button.grid(row=0, column=2, padx=5, pady=5)
        self.prev_button = ttk.Button(self.control_frame, text="Previous", command=self.previous_song, width=15)
        self.prev_button.grid(row=0, column=3, padx=5, pady=5)
        self.next_button = ttk.Button(self.control_frame, text="Next", command=self.next_song, width=15)
        self.next_button.grid(row=0, column=4, padx=5, pady=5)
        self.remove_button = ttk.Button(self.control_frame, text="Remove", command=self.remove_song, width=15)
        self.remove_button.grid(row=0, column=5, padx=5, pady=5)
        self.shuffle_button = ttk.Button(self.control_frame, text="Shuffle", command=self.shuffle_playlist, width=15)
        self.shuffle_button.grid(row=0, column=6, padx=5, pady=5)
        self.load_button = ttk.Button(self.control_frame, text="Load Songs", command=self.load_songs, width=15)
        self.load_button.grid(row=0, column=7, padx=5, pady=5)
        self.metadata_frame = ttk.Frame(self.master)
        self.metadata_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        self.artwork_label = ttk.Label(self.metadata_frame)
        self.artwork_label.pack(pady=10)
        self.metadata_text = tk.Text(self.metadata_frame, width=40, height=15, wrap=tk.WORD, state=tk.DISABLED)
        self.metadata_text.pack(pady=5)

    def load_songs(self):
        song_files = filedialog.askopenfilenames(title="Select Music Files", filetypes=[("All Music Files", "*.mp3;*.wav;*.ogg;*.flac")])
        if song_files:
            self.playlist.extend(song_files)
            for song in song_files:
                self.playlist_box.insert(tk.END, os.path.basename(song))

    def play_song(self):
        if not self.playlist:
            messagebox.showwarning("Warning", "No songs in the playlist.")
            return
        selected_song = self.playlist_box.curselection()
        if not selected_song:
            messagebox.showwarning("Warning", "Select a song to play.")
            return
        if self.is_playing:
            return
        self.current_song_index = selected_song[0]
        self.song_to_play = self.playlist[self.current_song_index]
        self.loop_mode = self.loop_mode_var.get().lower().replace(" ", "_")
        self.display_metadata(self.song_to_play)
        self.play_selected_song()

    def play_selected_song(self):
        threading.Thread(target=self._play_song).start()

    def _play_song(self):
        pygame.mixer.music.load(self.song_to_play)  # Load the song
        self.duration = self.get_song_duration()  # Get song duration
        self.current_time_slider.config(to=self.duration, state='normal')  # Enable slider and set maximum value
        self.duration_label.config(text=self.format_time(self.duration))  # Set the duration label

        self.is_playing = True
        pygame.mixer.music.play()  # Play the song

        while pygame.mixer.music.get_busy():  # Wait until the song is done
            self.update_slider()  # Update slider position
            if not self.is_playing:
                pygame.mixer.music.stop()  # Stop playing if the state is not playing
                return
            sleep(1)  # Sleep for a second to control the update rate

        self.is_playing = False
        self.current_time_slider.config(state='disabled')  # Disable slider after playback
        self.next_song()

    def update_slider(self):
        current_position = pygame.mixer.music.get_pos() / 1000  # Get current position in seconds
        self.current_time_slider.set(current_position)  # Update slider
        self.current_time_label.config(text=self.format_time(current_position))  # Update current time label

    def seek_song(self, event):
        if self.is_playing:
            pygame.mixer.music.pause()
            seek_time = self.current_time_slider.get()
            pygame.mixer.music.set_pos(seek_time)
            pygame.mixer.music.unpause()

    def format_time(self, seconds):
        hours = int(seconds // 3600)
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def get_song_duration(self):
        audio = File(self.song_to_play)
        return audio.info.length if audio.info.length else 0

    def pause_song(self):
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def stop_song(self):
        self.is_playing = False
        pygame.mixer.music.stop()

    def previous_song(self):
        if self.current_song_index > 0:
            self.current_song_index -= 1
        else:
            self.current_song_index = len(self.playlist) - 1
        self.stop_song()
        self.play_song()

    def next_song(self):
        if self.loop_mode == "Single Loop":
            self.stop_song()
            self.play_song()
            return
        if self.current_song_index < len(self.playlist) - 1:
            self.current_song_index += 1
        else:
            self.current_song_index = 0
        self.stop_song()
        self.play_song()

    def shuffle_playlist(self):
        random.shuffle(self.playlist)
        self.playlist_box.delete(0, tk.END)
        for song in self.playlist:
            self.playlist_box.insert(tk.END, os.path.basename(song))

    def remove_song(self):
        selected_song = self.playlist_box.curselection()
        if selected_song:
            song_index = selected_song[0]
            del self.playlist[song_index]
            self.playlist_box.delete(song_index)

    def display_metadata(self, song_path):
        self.metadata_text.config(state=tk.NORMAL)
        self.metadata_text.delete(1.0, tk.END)
        audio = File(song_path)
        name = audio.tags.get('TIT2').text[0] if audio.tags and 'TIT2' in audio.tags else "Unknown"
        artist = audio.tags.get('TPE1').text[0] if audio.tags and 'TPE1' in audio.tags else "Unknown"
        album = audio.tags.get('TALB').text[0] if audio.tags and 'TALB' in audio.tags else "Unknown"
        genre = audio.tags.get('TCON').text[0] if audio.tags and 'TCON' in audio.tags else "Unknown"
        sample_rate = audio.info.sample_rate if audio.info.sample_rate else "Unknown"
        duration = audio.info.length if audio.info.length else "Unknown"
        duration_str = f"{int(duration // 3600):02}:{int((duration % 3600) // 60):02}:{int(duration % 60):02}" if audio.info.length else "Unknown"
        self.metadata_text.insert(tk.END, f"Name: {name}\n")
        self.metadata_text.insert(tk.END, f"Artist: {artist}\n")
        self.metadata_text.insert(tk.END, f"Album: {album}\n")
        self.metadata_text.insert(tk.END, f"Genre: {genre}\n")
        self.metadata_text.insert(tk.END, f"Sample rate: {sample_rate}\n")
        self.metadata_text.insert(tk.END, f"Duration: {duration_str}\n")
        self.metadata_text.config(state=tk.DISABLED)
        artwork_data = None
        if audio.tags and 'APIC:' in audio.tags:
            if isinstance(audio.tags['APIC:'], list):
                artwork_data = audio.tags['APIC:'][0].data
            else:
                artwork_data = audio.tags['APIC:'].data
        if artwork_data:
            from io import BytesIO
            image = Image.open(BytesIO(artwork_data))
            image.thumbnail((150, 150))
            photo = ImageTk.PhotoImage(image)
            self.artwork_label.config(image=photo)
            self.artwork_label.image = photo
        else:
            self.artwork_label.config(image='')

if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
