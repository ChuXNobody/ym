## 项目介绍

该项目是在工作期间开发和部署的，使用了多种技术和算法，包括改进了 ER-NeRF 的生成，预加载模型，以及利用 ffmpeg 作为单独进程，多线程处理等。下面将对项目进行详细解析。由于过多文件，仅上传工作流程以及部分python代码

### 项目结构

```
\ym_jobwoek_example
    --3D-Human-Face-Reconstruction-with-3DMM-face-model-from-RGB-image-main
    --aduio_data
    --cub-2.1.0
    --ER-NeRF
    --ER-NERF所需模型
    --face-alignment
    --metahuman-stream
    --OpenFace_2.2.0_win_x64
    --wav2lip
    --wav2lip288*288
    --ym_python_exmple
```

### 技术栈

- Python
- FastAPI
- WebSocket
- FFmpeg
- HTTP
- TCP

### 使用算法

- 3DMM（3维人脸重建算法集成）
- NeRF（用于训练数据集的深度学习模型）
- OpenFace（用于收集图像进行推理生成 csv. 坐标数据集）
- DeepSpeech（对音频进行特征提取和推理）

### 主要项目：ER-NeRF

ER-NeRF 项目主要使用了以下已编写好的脚本：

- **tts.py**: 用于启用数据进行推理。命令为 `python tts.py data/01/ --workspace trial_vrh_torso/ -O`，其中 `data/01/` 是要使用的数据，`trial_vrh_torso` 是包含身体模型的工作空间。

### FastAPI 挂载服务

可以使用 FastAPI 框架将 ER-NeRF 作为一个 接口 服务挂载：

```python
from fastapi import FastAPI
from uvicorn import run

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to ER-NeRF API!"}

@app.post("/run_er_nerf")
async def run_er_nerf(data_path: str, workspace: str):
    return {"message": "ER-NeRF is running with data from " + data_path}

if __name__ == "__main__":
    run(app, host="192.168.31.199", port=8000)
```

可以使用 `uvicorn` 启动 FastAPI 服务器：

```
uvicorn app:app --host 192.168.31.199 --port 8000
```

这样就可以挂载 `http://192.168.31.199:8000` 
