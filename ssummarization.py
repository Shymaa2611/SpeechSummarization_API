from pydub import AudioSegment
from transformers import pipeline
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
from io import BytesIO

import numpy as np
from pydub import AudioSegment
from io import BytesIO
from transformers import pipeline

class Speech2Text:
    def audio_segments(self, audio_file: BytesIO, segment_length_ms=15000):
        audio = AudioSegment.from_file(audio_file, format="mp3")  
        total_length_ms = len(audio)
        segments = []
        for i in range(0, total_length_ms, segment_length_ms):
            segment = audio[i:i + segment_length_ms]
            segments.append(segment)
            print(f'Segment {i // segment_length_ms + 1} processed')
        return segments

    def segment_to_numpy(self, segment: AudioSegment):
        samples = segment.get_array_of_samples()
        np_array = np.array(samples).astype(np.float32) / (2**15)  
        return np_array

    def load_model(self):
        pipe = pipeline("automatic-speech-recognition", model="checkpoint/whisperLarge_checkpoint")
        return pipe

    def speech2text(self, audio_file: BytesIO):
        pipe = self.load_model()
        segments = self.audio_segments(audio_file)
        full_text = ""
        for segment in segments:
            # Convert segment to numpy array
            audio_data_np = self.segment_to_numpy(segment)
            
            # Pass numpy array to the pipeline
            result = pipe(audio_data_np, return_timestamps=True) 
            full_text += result["text"]
        return full_text

class TextSummarization():
    def load_model(self):
       model = GPT2LMHeadModel.from_pretrained('checkpoint/summarize_checkpoint')
       tokenizer = GPT2Tokenizer.from_pretrained('checkpoint/summarize_checkpoint')
       #device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
       #model.to(device)
       return model,tokenizer
     
    def summarize_text(self,text, tokenizer, model, max_length=512, summary_length=200):
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

   def speech2textsummarization(self,audio_File:BytesIO):
       text=self.s2t.speech2text(audio_File)
       summarize=self.ts.text2summarize(text)
       return summarize
   
