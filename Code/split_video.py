from moviepy.editor import VideoFileClip
import os
import argparse

def split_video(video_path):
    video = VideoFileClip(video_path)
    dir_path = "/".join(video_path.split('/')[:-1])
    video_name = video_path.split('/')[-1].split('.')[0]
    working_dir = dir_path + '/' + video_name + '_subclips'
    os.makedirs(working_dir, exist_ok=True)

    clip_start = 0
    subclip_duration = 300

    while clip_start < video.duration:
        clip_end = min(clip_start + subclip_duration, video.duration)
        subclip = video.subclip(clip_start, clip_end)
        subclip_path = working_dir + '/' + video_name + \
            f'_{clip_start//60}_{clip_end//60}.mp4'
        subclip.write_videofile(subclip_path)
        clip_start += subclip_duration


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('video_path', type=str, help='Path to the video')
    args = parser.parse_args()
    split_video(args.video_path)


if __name__ == '__main__':
    main()
