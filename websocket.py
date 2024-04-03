from fastapi import FastAPI, File, Response
from fastapi.responses import StreamingResponse
import os

app = FastAPI()
path=r"D:\ym_jobwoek_example\ER-NeRF\trial_vrh_torso\results"
@app.get("/m3u8/{file_path:path}")
async def get_m3u8(file_path: str):
    file_full_path = f"{path}/{file_path}"
    if os.path.exists(file_full_path):
        with open(file_full_path, "rb") as f:
            contents = f.read()
        return Response(content=contents, media_type="application/x-mpegURL")
    else:
        return {"error": "File not found"}

@app.get("/ts/{file_path:path}")
async def get_ts(file_path: str):
    file_full_path = f"{D:\ym_jobwoek_example\ER-NeRF\trial_vrh_torso\results}/{file_path}"
    if os.path.exists(file_full_path):
        return StreamingResponse(open(file_full_path, "rb"), media_type="video/MP2T")
    else:
        return {"error": "File not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.31.199", port=7000)
