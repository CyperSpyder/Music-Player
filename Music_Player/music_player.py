import sys
from tkinter import *
from tkinter import filedialog
from audioplayer import AudioPlayer
from mutagen.mp3 import MP3
import os
import json
import time
import threading

class music_player():
    def convert(self,seconds):
        self.seconds=seconds
        seconds=self.seconds
        hours = seconds // 3600
        seconds %= 3600
        mins = seconds // 60
        seconds %= 60
        return hours, mins, seconds
  
    def up_json(self):
        f = open("ctrl/ctrl.json", "r")
        update = json.load(f)
        f.close()
        update["m_ctrl"] = "none"
        f = open("ctrl/ctrl.json", "w")
        json.dump(update, f)
        f.close()
    
    def __init__(self):
        f = open("ctrl/ctrl.json", "r")
        ctrldata = json.load(f)
        f.close()
        path_dir=ctrldata['m_path']

        try:
          songs=os.listdir(path_dir)
        except Exception as e:
          try:
            path_dir = filedialog.askdirectory(title="Select Songs Folder")
            f = open("ctrl/ctrl.json", "r")
            update = json.load(f)
            f.close()
            update["m_path"] = path_dir
            f = open("ctrl/ctrl.json", "w")
            json.dump(update, f)
            f.close()
            songs=os.listdir(path_dir)
          except Exception as e:
            exit()
        i=0
        l=0
        total=len(songs)
        while i<=total:      
            song=MP3(os.path.join(path_dir,songs[i]))
            audio_info = song.info    
            length_in_secs = int(audio_info.length)
            hours, mins, seconds = self.convert(length_in_secs)
            self.loaddata(hours, mins, seconds)
            try:
                player = AudioPlayer(os.path.join(path_dir,songs[i]))
                player.play()
            except Exception as e:
                exit()
            
        # controls
            while True:
              f = open("ctrl/ctrl.json", "r")
              update = json.load(f)
              f.close()
              update["Song"] = songs[i]
              f = open("ctrl/ctrl.json", "w")
              json.dump(update, f)
              f.close()
              time.sleep(0.5)
              f = open("ctrl/ctrl.json", "r")
              ctrldata = json.load(f)
              f.close()
              value=ctrldata['m_ctrl']  
              if value == "pause song":
                  player.pause()
                  f = open("ctrl/ctrl.json", "r")
                  update = json.load(f)
                  f.close()
                  update["m_pause"] = True
                  pause=update["m_pause"]
                  f = open("ctrl/ctrl.json", "w")
                  json.dump(update, f)
                  f.close()
                  while pause is True:
                    f = open("ctrl/ctrl.json", "r")
                    update = json.load(f)
                    f.close()
                    pause=update["m_pause"]
                    resume=update["m_ctrl"]
                    if resume == "resume song":
                      player.resume() 
                      update["m_pause"],update["m_ctrl"] = False,"none"
                      pause=update["m_pause"]
                      f = open("ctrl/ctrl.json", "w")
                      json.dump(update, f)
                      f.close()
                    time.sleep(1)
                  self.up_json()
              elif value == "stop song":
                  player.stop()
                  l=0
                  self.up_json()
              elif value == "resume song":
                  player.resume() 
                  f = open("ctrl/ctrl.json", "r")
                  update = json.load(f)
                  f.close()
                  update["m_pause"] = False
                  f = open("ctrl/ctrl.json", "w")
                  json.dump(update, f)
                  f.close()
                  self.up_json()
              elif value == "play song":
                  player.play()
                  self.up_json()
              elif value == "next song":
                  try:
                    if i<=total:
                      i+=1
                      song=MP3(os.path.join(path_dir,songs[i]))
                      audio_info = song.info    
                      length_in_secs = int(audio_info.length)
                      player = AudioPlayer(os.path.join(path_dir,songs[i]))
                      player.play()
                      l=0
                    self.up_json()
                  except Exception as e:
                    i-=1
                    self.up_json()
              elif value == "previous song":
                  try:
                    i-=1
                    song=MP3(os.path.join(path_dir,songs[i]))
                    audio_info = song.info    
                    length_in_secs = int(audio_info.length)
                    player = AudioPlayer(os.path.join(path_dir,songs[i]))
                    player.play()
                    l=0
                    self.up_json()
                  except Exception as e:
                    i+=1
                    self.up_json()
              elif value == "close":
                  player.close()
                  self.up_json()
                  exit()
              time.sleep(1)
              if l == length_in_secs: 
                f = open("ctrl/ctrl.json", "r")
                update = json.load(f)
                f.close()
                try:
                  player.close()
                  if i<total:
                    i+=1
                    player = AudioPlayer(os.path.join(path_dir,songs[i]))
                    player.play()
                  else:
                      exit()
                  break 
                except Exception as e:
                  player.close()
                  exit()
              l+=1
            
class PlayerMonitor():
  player=Tk()
  player['bg']='#001010'

 # Get current song name   
  def current_song(self):
    f = open("ctrl/ctrl.json", "r")
    ctrldata = json.load(f)
    f.close()
    Current_song=ctrldata['Song']
    _Song=Current_song[0:20]
    return _Song

 # Play  
  def _play(self):
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "play song"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()

 # stop    
  def _stop(self):
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "stop song"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()

 # Pause
  def _pause(self):
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "pause song"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close() 

 # Ressume
  def _resume(self):
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "resume song"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()

 # next
  def _next(self):
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "next song"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()

 # Previous
  def _previous(self):
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "previous song"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()
  
 # Display current song name 
  def m_player_monitor(self):
    player=self.player
    _Song=self.current_song()
    Song_Title_txt=Label(
      player, 
      text=" "+ _Song,
      bg='#001010', 
      fg='#FFF', 
      font=("Arial 9")
      )
    Song_Title_txt.place(x=30, y=25)
    player.after(1000,self.m_player_monitor)

 # Close Player
  def _close(self):
    player=self.player
    threading.Thread(target=player.destroy).start()
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "close"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()
    time.sleep(0.5)
    f = open("ctrl/ctrl.json", "r")
    update = json.load(f)
    f.close()
    update["m_ctrl"] = "none"
    f = open("ctrl/ctrl.json", "w")
    json.dump(update, f)
    f.close()
    os.system('killall -q -15 python3')

  def __init__(self):

 # App open place
    player=self.player
    w = player.winfo_reqwidth()
    h = player.winfo_reqheight()
    ws =player.winfo_screenwidth()
    hs =player.winfo_screenheight()
    x = (ws/1.005) - (w)
    y = (hs/1.365) - (h)
    player.geometry('+%d+%d' % (x, y))

  # Window Size and Transparancy
    player.attributes('-type', 'normal')
    player.geometry("200x50")
    player.attributes('-alpha',0.93)

  # TitleBar
    player.overrideredirect(True)
    title_bar = Frame(
    player, 
    bg='#001010', 
    relief='raised', 
    bd=0,highlightthickness=0
    )
    title_bar.pack(expand=0, fill=X)

  # CloseButton
    close_button = Button(
      title_bar, 
      text='x ', 
      command= self._close,bg="#001010",
      padx=3,pady=0,
      activebackground='#001010',
      activeforeground='#FF2300',
      bd=0,font="bold",
      fg='white',
      highlightthickness=0,
      )
    close_button.pack(side=RIGHT)

  # Workplace
    window = Canvas(
      player, 
      bg='#001010',
      highlightthickness=0
      )
    window.pack(expand=1, fill=BOTH)

 # icons
    StopImg= PhotoImage(file='control_icons/stop.png')
    StopImg=StopImg.subsample(50, 50)
    PauseImg=PhotoImage(file='control_icons/pause.png')
    PauseImg=PauseImg.subsample(50, 50)
    NextImg=PhotoImage(file='control_icons/next.png')
    NextImg=NextImg.subsample(50, 50)
    PlayImg=PhotoImage(file='control_icons/play.png')
    PlayImg=PlayImg.subsample(50, 50)
    PreviousImg=PhotoImage(file='control_icons/previous.png')
    PreviousImg=PreviousImg.subsample(50, 50)
    StopPlay=PhotoImage(file='control_icons/stopPlay.png')
    StopPlay=StopPlay.subsample(50, 50)

 # ctrl_Buttons
    Stop_button = Button(
          window, 
          image=StopImg,
          command=self._stop,
          bg="#001010",
          padx=3,pady=0,
          activebackground='#001010',
          activeforeground='#FF2300',
          bd=0,font="bold",
          fg='white',
          highlightthickness=1,
          )
    Stop_button.place(x=10, y=0)
    
    Play_button = Button(
          window, 
          image=PlayImg, 
          command=self._play,
          bg="#001010",
          padx=3,pady=0,
          activebackground='#001010',
          activeforeground='#FF2300',
          bd=0,font="bold",
          fg='white',
          highlightthickness=1,
          )
    Play_button.place(x=10, y=14)

    Previous_button = Button(
          window, 
          image=PreviousImg, 
          command=self._previous,
          bg="#001010",
          padx=3,pady=0,
          activebackground='#001010',
          activeforeground='#FF2300',
          bd=0,font="bold",
          fg='white',
          highlightthickness=1,
          )
    Previous_button.place(x=140, y=7)

    Pause_button = Button(
          window, 
          image=PauseImg, 
          command=self._pause,
          bg="#001010",
          padx=3,pady=0,
          activebackground='#001010',
          activeforeground='#FF2300',
          bd=0,font="bold",
          fg='white',
          highlightthickness=1,
          )
    Pause_button.place(x=157, y=14)
    
    Play_button = Button(
          window, 
          image=PlayImg, 
          command=self._resume,
          bg="#001010",
          padx=3,pady=0,
          activebackground='#001010',
          activeforeground='#FF2300',
          bd=0,font="bold",
          fg='white',
          highlightthickness=1,
          )
    Play_button.place(x=157, y=0)

    Next_button = Button(
          window, 
          image=NextImg, 
          command=self._next,bg="#001010",
          padx=3,pady=0,
          activebackground='#001010',
          activeforeground='#FF2300',
          bd=0,font="bold",
          fg='white',
          highlightthickness=1,
          )
    Next_button.place(x=174, y=7)
 
 # Window setup

    # Title
    Title_txt=Label(
      player, 
      text="Music Player",
      bg='#001010', 
      fg='#FFF', 
      font=("Arial 10")
      )
    Title_txt.place(x=70, y=1)

    threading.Thread(target=self.m_player_monitor, args=[]).start()
    threading.Thread(target=music_player).start()
  # First Trigger
    player.mainloop()

PlayerMonitor()
