from moviepy.editor import *
from multiprocessing import Process, Semaphore
# from spleeter.separator import Separator
# from spleeter.audio.adapter import AudioAdapter
import subprocess
import customtkinter as ctk
# import sys

##################################################### Spleeter #######################################################
def split_video(video_path, save_path):
    
    # separator = Separator('spleeter:2stems')
    # audio_loader = AudioAdapter.default()
    
    # sample_rate = 44100
    # waveform, _ = audio_loader.load('/path/to/audio/file', sample_rate=sample_rate)

    # # Perform the separation :
    # prediction = separator.separate(waveform)
    
    # segment_length = float(60)  # seconds
    # original_video = VideoFileClip("original.mp4")
    
    # Replace with the path to your video file
    # video_path = 'F:\\Spleeter\\test_video.mp4'
    save_path = save_path + '\\spleeter_output'
    # Extract audio from video
    video = VideoFileClip(video_path)
    # duration = video.duration
    # clip_start = 0
    # num = 0
    # clips = []
    # pool_sema = Semaphore(3)

    # while clip_start < duration:
    #     # pool_sema.acquire()
    #     clip_end = min(clip_start + segment_length, duration)
    #     subclip = original_video.subclip(clip_start, clip_end)
    #     clips.append(subclip)
    #     # num += 1
    #     # filename = "output_%04d.mp4" % num
    #     # print("Writing", filename)
    #     # Process(target=subclip.write_videofile,
    #     #         args=(filename,),
    #     #         kwargs={}).start()
    #     clip_start += segment_length

    # pool_sema.acquire()
    
    audio = video.audio
    audio_path = save_path + '\\audio.wav'
    audio.write_audiofile(audio_path)

    # Use spleeter to separate vocals and accompaniment
    subprocess.run(['spleeter', 'separate', audio_path,
                    '-p', 'spleeter:2stems', '-o', save_path])

    # Replace audio in video with separated vocal track
    vocals_path = save_path + '\\vocals.wav'
    vocals = AudioFileClip(vocals_path)
    new_video = video.set_audio(vocals)
    new_video_path = save_path + '\\' + video_path.split('\\')[-1].split('.')[0] + '_vocals.mp4'
    # Write new video file
    new_video.write_videofile(new_video_path)


video_path = 'E:\\Movies\\Hotel.Transylvania.4.Transformania.2022.1080p.WEB-DL.mp4'
save_path = 'E:\\Movies'

split_video(video_path, save_path)

##################################################### CustomTKInter #######################################################

# ctk.set_appearance_mode('dark')
# ctk.set_default_color_theme('dark-blue')

# root = ctk.CTk()
# root.geometry('500x350')

# frame = ctk.CTkFrame(master=root)
# frame.pack(pady=20, padx=60, fill='both', expand=True)
# label = ctk.CTkLabel(master=frame, text='Select a video file')
# label.pack(pady=10, padx=10)
# video_path = ctk.CTkEntry(master=frame, placeholder_text='Video Path')
# save_path = ctk.CTkEntry(master=frame, placeholder_text='Save Path')
# video_path.pack(pady=10, padx=100)
# save_path.pack(pady=10, padx=100)
# split_video_button = ctk.CTkButton(master=frame, text='Split Video', command=lambda: split_video(video_path.get(), save_path.get()))
# split_video_button.pack(pady=10, padx=10)
# root.mainloop()
