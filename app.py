from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yt_dlp

app = FastAPI()

# Allow frontend access from anywhere (can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "YT-DLP API is working!"}

@app.get("/download")
def download_audio(url: str = Query(..., description="YouTube video URL")):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True,
        'extract_flat': False,
        'forceurl': True,
        'skip_download': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
        title = info.get('title', 'Unknown Title')

    return {
        "title": title,
        "audio_url": audio_url
    }
    
from fastapi.responses import JSONResponse

@app.get("/extract")
async def extract(url: str = Query(...)):
    try:
        ydl_opts = {
            'quiet': True,
            'skip_download': True,
            'forcejson': True,
            'simulate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        return JSONResponse(content=info)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
