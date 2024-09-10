from pydub import AudioSegment
from transformers import pipeline
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

import numpy as np
from pydub import AudioSegment
from transformers import pipeline
from io import BytesIO

class Speech2Text:
    def audio_segments(self, audio_url, segment_length_ms=15000):
       
        audio = AudioSegment.from_mp3(audio_url)
        total_length_ms = len(audio)
        segments = []
        for i in range(0, total_length_ms, segment_length_ms):
            segment = audio[i:i+segment_length_ms]
            segments.append(segment)
            print(f'Segment {i // segment_length_ms + 1} processed')
        return segments

    def load_model(self):
        # Load the ASR pipeline
        pipe = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3")
        return pipe

    def audiosegment_to_numpy(self, segment):
        samples = np.array(segment.get_array_of_samples())
        return samples.astype(np.float32)

    def speech2text(self, audio_url):
        pipe = self.load_model()
        segments = self.audio_segments(audio_url)
        full_text = ""
        for segment in segments:
            audio_data = self.audiosegment_to_numpy(segment)
            result = pipe(audio_data)
            full_text += result["text"]
        return full_text

class TextSummarization():
    def load_model(self):
       model = GPT2LMHeadModel.from_pretrained('checkpoint/summarize_checkpoint')
       tokenizer = GPT2Tokenizer.from_pretrained('checkpoint/summarize_checkpoint')
       #device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
       #model.to(device)
       return model,tokenizer
     
    def summarize_text(self,text, tokenizer, model, max_length=512, summary_length=150):
      inputs = tokenizer.encode(text, return_tensors='pt', max_length=max_length, truncation=True)
      with torch.no_grad():
        summary_ids = model.generate(inputs, max_length=summary_length, num_beams=4, early_stopping=True)
      summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
      return summary
       
    def text2summarize(self,full_text):
        model,tokenizer=self.load_model()
        summary=self.summarize_text(full_text,tokenizer,model)
        return summary

class Speech2TextSummarization():
   def __init__(self):
       self.s2t=Speech2Text()
       self.ts=TextSummarization()

   def speech2textsummarization(self,audio_url):
       text=self.s2t.speech2text(audio_url)
       summarize=self.ts.text2summarize(text)
       return summarize
   
