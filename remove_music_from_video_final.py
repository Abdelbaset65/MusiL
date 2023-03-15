# %% [markdown]
# # Remove Music from Video

# %% [markdown]
# ## Installing Dependencies

# %%
# %pip install moviepy==1.0.3
# %pip install spleeter==2.3.2
# %pip install scipy==1.5.4

# %% [markdown]
# ## Import Libraries

# %%
import os
import shutil
import subprocess
import argparse
# import librosa
# import noisereduce as nr
import numpy as np
# from pydub import AudioSegment
# from pydub.silence import split_on_silence
from scipy.signal import savgol_filter
from scipy.io import wavfile
from moviepy.editor import VideoFileClip, AudioFileClip

# %% [markdown]
# ## Define Functions

# %% [markdown]
# ### Split Video into Subclips

# %%
def split_video(video_path, subclip_duration=300, remove_original=False):
    video = VideoFileClip(video_path)
    dir_path = "/".join(video_path.split('/')[:-1])
    video_name = video_path.split('/')[-1].split('.')[0]
    subclips_dir = dir_path + '/' + video_name + '_subclips'
    os.makedirs(subclips_dir, exist_ok=True)

    subclip_duration = subclip_duration
    clip_start = 0
    i = 1
    
    while clip_start < video.duration:
        clip_end = min(clip_start + subclip_duration, video.duration)
        subclip = video.subclip(clip_start, clip_end)
        subclip_path = subclips_dir + '/' + video_name + \
            f'_{i}.mp4'
        subclip.write_videofile(subclip_path)
        clip_start += subclip_duration
        i += 1

    if remove_original:
        os.remove(video_path)
        
    return subclips_dir



# %% [markdown]
# ### Enhance Vocals

# %%
def enhance_vocals(vocals):

    # Load audio file
    rate, data = wavfile.read(vocals)

    # Apply Savitzky-Golay filter to each channel
    filtered_data = np.zeros_like(data)
    for i in range(data.shape[1]):
        filtered_data[:, i] = savgol_filter(
            data[:, i], window_length=31, polyorder=2)

    # Save filtered audio
    # Save the gated audio to a new file
    
    video_name = vocals.split('/')[-1].split('.')[0]
    new_vocals = "/".join(vocals.split('/')[:-1]) + '/' + video_name + \
                                            '_vocals_enhanced.wav'
    wavfile.write(new_vocals, rate, filtered_data)        

    return new_vocals

# def enhance_vocals2(vocals):

#     # Load audio file
#     sound = AudioSegment.from_wav(vocals)

#     # Split audio file on silence
#     chunks = split_on_silence(sound, min_silence_len=1000, silence_thresh=-16)

#     # Concatenate interleaving portions to create noise clip
#     noise_clip = AudioSegment.empty()
#     for i in range(1, len(chunks), 2):
#         noise_clip += chunks[i]

#     # Convert noise clip to numpy array for use with noisereduce
#     noise_clip_array = np.array(noise_clip.get_array_of_samples())

#     # Load audio file using librosa
#     y, sr = librosa.load("your_audio_file.wav")

#     # Perform noise reduction using noisereduce
#     reduced_noise = nr.reduce_noise(audio_clip=y, noise_clip=noise_clip_array)

#     # Save the result to a new file using librosa
#     video_name = vocals.split('/')[-1].split('.')[0]
#     new_vocals = "/".join(vocals.split('/')[:-1]) + '/' + video_name + \
#         '_vocals_enhanced.wav'
#     librosa.output.write_wav(new_vocals, reduced_noise, sr)
    
#     return new_vocals

# %% [markdown]
# ### Remove Music from Video

# %%
def remove_music(video_path, remove_original=False):

    dir_path = "/".join(video_path.split('/')[:-1])
    working_dir = dir_path + '/tmp'
    os.makedirs(working_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    video_name = video_path.split('/')[-1].split('.')[0]
    audio = video.audio
    audio_path = working_dir + '/audio.wav'
    audio.write_audiofile(audio_path)
    vocals_path = working_dir + '/audio/vocals.wav'

    result = subprocess.run(['spleeter', 'separate',
                             '-p', 'spleeter:2stems',
                             '-o', working_dir,
                             audio_path], 
                            stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    if result.returncode == 0:
        print(f'Music removed from {video_name}')

    else:
        print(f'Could not remove music from {video_name}\n\
                returncode = {result.returncode}\n\
                {result.stderr.decode("utf-8")}')
        return
    enhanced_vocals_path = enhance_vocals(vocals_path)
    # enhanced_vocals_path = enhance_vocals2(vocals_path)
    # enhanced_vocals_path = dolby_enhance(
    #     input_file=vocals_path, 
    #     output_file=working_dir + '/audio/vocals_enhanced.wav', 
    #     api_key='b68DHDp-JvYoqPhKp9AjgA==')
    vocals = AudioFileClip(enhanced_vocals_path)
    new_video = video.set_audio(vocals)
    # output_dir = dir_path + '/No_Music'
    # os.makedirs(output_dir, exist_ok=True)
    # new_video_path = output_dir + '/' + video_name + '_no_music.mp4'
    new_video_path = dir_path + '/' + video_name + '_no_music.mp4'
    new_video.write_videofile(new_video_path)

    shutil.rmtree(working_dir)
    if remove_original:
        os.remove(video_path)
        
    return new_video_path

# %% [markdown]
# ## Test

# %%
def main():
    
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', type=str, help='Path to the video')
    parser.add_argument('-r', '--remove_original', action='store_true', default=False,
                        help='Remove original video')
    parser.add_argument('-s', '--subclip_duration', type=int, default=300,
                        help='Duration of subclips in seconds')
                        
    
    args = parser.parse_args()
    video_path = args.video_path
    remove_original = args.remove_original
    subclip_duration = args.subclip_duration
    
    video_name = video_path.split('/')[-1].split('.')[0]
    base_dir = '/'.join(video_path.split('/')[:-1])
    
    # Split video into subclips if longer than subclip_duration
    video = VideoFileClip(video_path)
    if video.duration > subclip_duration:
        
        subclips_dir = split_video(video_path=video_path,
                                   subclip_duration=subclip_duration, 
                                   remove_original=remove_original)
        # subclips_dir = '/mnt/e/Anime/Vinland_Saga/VS_S2_E10_subclips'
        subclips = []
        
        # Remove music from each subclip
        for f in os.listdir(subclips_dir):
            if f.endswith('.mp4'):
                new_video_path = remove_music(video_path=subclips_dir + '/' + f, 
                                              remove_original=remove_original)
                subclips.append(new_video_path)
        
        # Concatenate subclips
        for i in range(len(subclips)):
            subclips[i] = f'file {subclips[i]}'
            
        subclips_list = '\n'.join(subclips)
        with open(f'{subclips_dir}/subclips.txt', 'w') as f:
            f.writelines(subclips_list)

        cmd = f'ffmpeg -f concat -safe 0 -i {subclips_dir}/subclips.txt -c copy \
                                            {base_dir}/{video_name}_no_music.mp4'
        result = subprocess.run(cmd, shell=True, stderr=subprocess.PIPE,)
        
        if result.returncode == '0':
            print('Concatenated')
        else:
            print(f'Command failed with return code {result.returncode}\n\
                {result.stderr.decode("utf-8")}')
            
        if remove_original:
            shutil.rmtree(subclips_dir)   

        print(f'New video saved at {base_dir}/{video_name}_no_music.mp4')     
        
    else:
        new_video_path = remove_music(video_path)
        print(f'New video saved at {new_video_path}')

if __name__ == '__main__':
    main()

