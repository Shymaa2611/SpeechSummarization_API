from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi.templating import Jinja2Templates
from fastapi import Request
from ssummarization import Speech2TextSummarization,Speech2Text,TextSummarization
from summary_format import OutputFormat
from videosummarization import VideoSummarization

app = FastAPI()
templates = Jinja2Templates(directory="templates")
       
@app.post('/speech2text/')
async def speech_text(Audio_file: UploadFile = File(...)):
    file_bytes = await Audio_file.read()
    file_io = BytesIO(file_bytes)
    s2t=Speech2Text()
    text=s2t.speech2text(file_io)
    return text


#@app.get('/textsummarization/')
def text_summarization(text:str):
    t2s=TextSummarization()
    summary=t2s.text2summarize(text)
    return summary

@app.get('/videosummarization/')
async def video_summarization(video_url:str):
    v2s=VideoSummarization()
    summary=v2s.Video_summarization(video_url)
    return summary

@app.post('/speechsummarization/')
async def speech_summarization(Audio_file: UploadFile = File(...)):
    file_bytes = await Audio_file.read()
    file_io = BytesIO(file_bytes)
    s2s=Speech2TextSummarization()
    summary=s2s.speech2textsummarization(file_io)
    return summary

@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def upload_audio(file: UploadFile = File(...), file_type: str = Form(...), format: str = Form(...)):
    file_bytes = await file.read()
    file_io = BytesIO(file_bytes)
    if file_type == 'audio':
        s2ts = Speech2TextSummarization()
        summary = s2ts.speech2textsummarization(file_io)
        #summary="hello how are you"
    elif file_type == 'video':
        v2s = VideoSummarization()
        summary = v2s.Video_summarization(file_io)
        #summary="hello how are you"
    else:
        return {"error": "Unsupported file type"}
    output_format = OutputFormat()
    if format == 'pdf':
        pdf_io = BytesIO()
        output_format.pdf(summary, pdf_io)
        pdf_io.seek(0)
        return StreamingResponse(pdf_io, media_type='application/pdf', headers={"Content-Disposition": "attachment; filename=summary.pdf"})
    elif format == 'word':
        doc_io = BytesIO()
        output_format.word(summary, doc_io)
        doc_io.seek(0)
        return StreamingResponse(doc_io, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document', headers={"Content-Disposition": "attachment; filename=summary.docx"})
    elif format == 'text':
        text_io = BytesIO()
        output_format.text(summary, text_io)
        text_io.seek(0)
        return StreamingResponse(text_io, media_type='text/plain', headers={"Content-Disposition": "attachment; filename=summary.txt"})
    elif format == 'pptx':
        ppt_io = BytesIO()
        output_format.powerpoint(summary, ppt_io)
        ppt_io.seek(0)
        return StreamingResponse(ppt_io, media_type='application/vnd.openxmlformats-officedocument.presentationml.presentation', headers={"Content-Disposition": "attachment; filename=summary.pptx"})
    else:
        return {"error": "Unsupported format"}


if __name__=="main":
    text="""Artificial Intelligence (AI) has rapidly evolved from a futuristic concept into a transformative force reshaping a multitude of industries. This technology, characterized by its ability to perform tasks that typically require human intelligence, such as learning, reasoning, and problem-solving, has far-reaching implications across sectors including healthcare, finance, transportation, and more.
   In healthcare, AI has revolutionized diagnostics and patient care. Machine learning algorithms analyze vast amounts of medical data to identify patterns and predict outcomes with remarkable accuracy. For example, AI-powered imaging tools can detect early signs of diseases like cancer and diabetic retinopathy from medical scans. Additionally, AI-driven predictive analytics help in personalizing treatment plans and optimizing hospital operations, ultimately enhancing patient outcomes and reducing costs.
"""
    print(text_summarization(text))

