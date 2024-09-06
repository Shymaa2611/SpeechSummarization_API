from ssummarization import Speech2TextSummarization
from moviepy.editor import VideoFileClip


class Video2audio():
   
    def extract_audio_from_video(video_file_path, output_audio_file_path="output_audio.mp3"):   
       video = VideoFileClip(video_file_path)
       audio = video.audio
       audio.write_audiofile(output_audio_file_path)
       return output_audio_file_path
    
    def video2audio(self,video_url:str):
        audio_url=self.extract_audio_from_video(video_url)
        return audio_url

class VideoSummarization():
    def __init__(self):
        self.v2a=Video2audio()
        self.vs=Speech2TextSummarization()
    def Video_summarization(self,video_url:str):
       audio_url=self.v2a.video2audio(video_url)
       summary=self.vs.speech2textsummarization(audio_url)
       return summary

    
