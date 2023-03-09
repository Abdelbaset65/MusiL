import os
import shutil
import subprocess
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip


def remove_music(video_path, remove_original=False):
    
    dir_path = "/".join(video_path.split('/')[:-1])
    working_dir = dir_path + '/tmp'
    os.makedirs(working_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    video_name = video_path.split('/')[-1].split('.')[0]
    audio = video.audio
    audio_path = working_dir + '/audio.wav'
    audio.write_audiofile(audio_path)

    cp = subprocess.run(['spleeter', 'separate',
                         '-p', 'spleeter:2stems',
                         '-o', working_dir,
                         audio_path], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    print("\n\n", cp.returncode, cp.stdout.decode(
        'utf-8'), cp.stderr.decode('utf-8'), sep='\n\n')

    vocals_path = working_dir + '/audio/vocals.wav'
    try:    
        vocals = AudioFileClip(vocals_path)
        new_video = video.set_audio(vocals)
        new_video_path = dir_path + '/' + video_name + '_no_music.mp4'
        new_video.write_videofile(new_video_path)
    except Exception as e:
        print(e)
        
    shutil.rmtree(working_dir)
    if remove_original:
        os.remove(video_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', type=str, help='Path to the video')
    parser.add_argument('-r', '--remove_original', action='store_true', 
                        help='Remove original video')
    
    args = parser.parse_args()
    print(args)
    
    remove_music(args.video_path, args.remove_original)
    
    
if __name__ == '__main__':
    main()