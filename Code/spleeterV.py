from moviepy.editor import *
from spleeter.separator import Separator

def separate_music(video_path, save_path):
    separator = Separator('spleeter:2stems')
    segment_length = float(60)  # seconds
    save_path = save_path + '\\spleeter_output'
    
    original_video = VideoFileClip(video_path)
    duration = original_video.duration
    clip_start = 0
    clips = []
    
    while clip_start < duration:
        clip_end = min(clip_start + segment_length, duration)
        subclip = original_video.subclip(clip_start, clip_end)
        subclip_audio = subclip.audio
        separated_audio = separator.separate(subclip_audio.to_soundarray())
        vocals = separated_audio['vocals']
        new_subclip = subclip.set_audio(vocals)
        clips.append(new_subclip)
        clip_start += segment_length
        
    new_video = concatenate_videoclips(clips)
    new_video_path = save_path + '\\' + video_path.split('\\')[-1].split('.')[0] + '_vocals.mp4'
    new_video.write_videofile(new_video_path)
    
if __name__ == '__main__':
    separate_music('F:\\Spleeter\\test_video.mp4', 'F:\\Spleeter')