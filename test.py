from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_file_path, output_audio_file_path="output_audio.mp3"):

    video = VideoFileClip(video_file_path)
    audio = video.audio
    audio.write_audiofile(output_audio_file_path)

video_path = "input.mp4"

extract_audio_from_video(video_path)
