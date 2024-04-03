import asyncio
from fastapi import FastAPI, BackgroundTasks
from starlette.responses import StreamingResponse, Response
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import subprocess
import uvicorn
import threading
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time

app = FastAPI()

# 添加跨域中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，也可以指定特定的来源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有HTTP请求头
)

frame_folder = r"D:\ym_jobwoek_example\ER-NeRF\trial_vrh_torso\results"
audio_folder = r"D:\ym_jobwoek_example\ER-NeRF\trial_vrh_torso\results\ngp_ep0023_ts_slices"
m3u8_file = os.path.join(frame_folder, "output.m3u8")

# 配置静态文件目录
app.mount("/static", StaticFiles(directory=frame_folder), name="static")

class FrameHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filename = os.path.basename(event.src_path)
        if filename.startswith("ngp_ep0023_"):
            asyncio.create_task(send_new_frame_to_clients("New frame data"))  # Use create_task to run coroutine in background
            generate_m3u8_file()  # Generate m3u8 file when new frame is created
            
async def send_new_frame_to_clients(frame_data):
    # Logic to send new frame to connected clients
    print("New frame data:", frame_data)  # Placeholder for actual logic
    # You may need to implement the logic to send the new frame to clients here

def generate_hls_segments():
    segment_duration = 1 / 25  # Duration of each segment in seconds
    segment_index = 0

    while True:
        segment_file = os.path.join(frame_folder, f"segment_{segment_index:04d}.ts")
        if not os.path.exists(segment_file):
            break
        with open(segment_file, "rb") as f:
            yield f.read()
        segment_index += 1

async def send_m3u8_file():
    while True:
        generate_m3u8_file()
        await asyncio.sleep(1)  # Check every 1 second for updates

def generate_m3u8_file():
    segment_files = sorted(filter(lambda x: x.startswith("segment_"), os.listdir(frame_folder)))
    with open(m3u8_file, "w") as f:
        f.write("#EXTM3U\n")
        f.write("#EXT-X-VERSION:3\n")
        f.write("#EXT-X-TARGETDURATION:10\n")  # 调整为片段持续时间的最大值
        f.write("#EXT-X-MEDIA-SEQUENCE:0\n")
        f.write("#EXT-X-PLAYLIST-TYPE:EVENT\n")
        for segment_file in segment_files:
            f.write(f"#EXTINF:10.000000,\n")  # 调整为每个片段的预期持续时间
            f.write(f"/static/{segment_file}\n")


def run_ffmpeg_periodically_thread():
    while True:
        run_ffmpeg()
        time.sleep(5)  # Run every 5 seconds

def run_ffmpeg_periodically():
    while True:
        run_ffmpeg()
        time.sleep(5)  # Run every 5 seconds
        
def run_ffmpeg():
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",  # Overwrite existing files
        "-framerate", "25",  # Set framerate to 25 FPS for video
        "-stream_loop", "-1",  # Loop the video indefinitely
        "-i", os.path.join(frame_folder, "ngp_ep0023_%04d_rgb.png"),
        "-i", os.path.join(audio_folder, "output_audio.wav"),
        "-c:v", "libx264",
        "-r", "25",  # Set output video framerate
        "-output_ts_offset", "5",  # Output ts offset
        "-c:a", "aac",
        "-shortest",  # End encoding when the shortest input ends
        "-hls_time", "1",  # Set segment duration to 5 seconds
        "-hls_list_size", "0",  # Infinite playlist
        "-hls_segment_type", "mpegts",  # Set HLS segment type to mpegts
        "-hls_flags", "delete_segments",  # Delete segment files when they are no longer needed
        "-hls_segment_filename", os.path.join(frame_folder, "segment_%04d.ts"),
        os.path.join(frame_folder, "output.m3u8")
    ]
    subprocess.run(ffmpeg_cmd)
    generate_m3u8_file()

@app.get("/")
async def get_video_feed(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_m3u8_file)
    return StreamingResponse(
        generate_hls_segments(),
        media_type="video/MP2T"
    )


@app.get("/hls.m3u8")
async def get_m3u8_file():
    if os.path.exists(m3u8_file):
        with open(m3u8_file, "r") as f:
            m3u8_content = f.read()
            # run_ffmpeg()
        return Response(content=m3u8_content, media_type="application/vnd.apple.mpegurl")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(FrameHandler(), frame_folder, recursive=True)
    observer.start()

    ffmpeg_thread = threading.Thread(target=run_ffmpeg)
    ffmpeg_thread.start()
    
    ffmpeg1_thread = threading.Thread(target=run_ffmpeg_periodically)
    ffmpeg1_thread.start()

    uvicorn.run(app, host="192.168.31.199", port=7000)
