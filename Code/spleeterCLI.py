from moviepy.editor import AudioFileClip, VideoFileClip
# from multiprocessing import Process, Semaphore
import subprocess
import os
import shutil

def remove_music_from_video(video_path):
    dir_path = "/".join(video_path.split('/')[:-1])
    working_dir = dir_path + '/tmp'
    os.makedirs(working_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    audio = video.audio
    audio_path = working_dir + '/audio.wav'
    audio.write_audiofile(audio_path)

    
    subprocess.run(['spleeter', 'separate',
                    '-p', 'spleeter:2stems', '-o', working_dir, audio_path])
    
    vocals_path = working_dir + '/audio/vocals.wav'
    vocals = AudioFileClip(vocals_path)
    new_video = video.set_audio(vocals)
    # save the new video in the same folder as the original video and delete the tmp folder
    new_video_path = dir_path + '/' + video_path.split('/')[-1].split('.')[0] + '_vocals.mp4'
    new_video.write_videofile(new_video_path)
    shutil.rmtree(working_dir)
    

if __name__ == '__main__':
    video_path = input('Enter the path to the video: ')
    remove_music_from_video(video_path)
    