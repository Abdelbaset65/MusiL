from moviepy.editor import AudioFileClip, VideoFileClip, concatenate_videoclips
import subprocess
import os
import shutil
import sys

def split_video(video_path):
    video = VideoFileClip(video_path)
    dir_path = "/".join(video_path.split('/')[:-1])
    video_name = video_path.split('/')[-1].split('.')[0]
    subclips_path = dir_path + '/' + video_name + '_subclips'
    os.makedirs(subclips_path, exist_ok=True)

    clip_start = 0
    subclip_duration = 300

    while clip_start < video.duration:
        clip_end = min(clip_start + subclip_duration, video.duration)
        subclip = video.subclip(clip_start, clip_end)
        subclip_path = subclips_path + '/' + video_name + \
            f'_{clip_start//60}_{clip_end//60}.mp4'
        subclip.write_videofile(subclip_path)
        clip_start += subclip_duration
        
    return subclips_path

def remove_music_from_video(video_path, remove_original=False):
    
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
                    audio_path], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE)
    
    print(cp.stdout.decode('utf-8'))
    print(cp.stderr.decode('utf-8'))
    print(cp.returncode)
    
    vocals_path = working_dir + '/audio/vocals.wav'
    vocals = AudioFileClip(vocals_path)
    new_video = video.set_audio(vocals)
    new_video_path = dir_path + '/' + video_name + '_vocals.mp4'
    new_video.write_videofile(new_video_path)
    shutil.rmtree(working_dir)
    if remove_original:
        os.remove(video_path)
    return new_video_path
    
    
def main():
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = input('Enter the path to the video: ')
    
    video = VideoFileClip(video_path)
    if video.duration <= 300:
        remove_music_from_video(video_path)
    else:
        subclips_path = split_video(video_path)
        # subclips_path = '/mnt/e/Movies/Atlantis2_subclips'
        # loop through subclips and remove music from each
        # then concatenate the subclips and save to a new video
        # then remove the subclips directory
        subclips = os.listdir(subclips_path)
        for i in range(len(subclips)):
            subclips[i] = remove_music_from_video(subclips_path + '/' + subclips[i],
                                                remove_original=True)
        subclips = [VideoFileClip(subclip) for subclip in subclips]
        new_video = concatenate_videoclips(subclips)
        new_video_path = subclips_path.split('.')[0] + '_no_music.mp4'
        new_video.write_videofile(new_video_path)
        shutil.rmtree(subclips_path)
        
        
if __name__ == '__main__':
    main()
    