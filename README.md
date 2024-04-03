# 项目文档

## 项目名称：ym

---

## 2. 项目介绍

ym_jobwoek_example 是一个工作期间开发部署的项目，旨在利用多种技术和算法实现对数据的处理和推理。该项目的主要特点包括改良了 ErNeRF 的生成方法，使用预加载模型，将 FFmpeg 作为单独进程，并实现了多线程处理。以下是项目的详细介绍和规范。上传工作流程以及部分python代码。

---

## 3. 项目结构

```
\ym_jobwoek_example
|-- 3D-Human-Face-Reconstruction-with-3DMM-face-model-from-RGB-image-main
|-- aduio_data
|-- cub-2.1.0
|-- ER-NeRF
|-- ER-NERF所需模型
|-- face-alignment
|-- metahuman-stream
|-- OpenFace_2.2.0_win_x64
|-- wav2lip
|-- wav2lip288*288
|-- ym_python_exmple
```

---

## 4. 技术栈

本项目所使用的技术栈包括：

- Python
- FastAPI
- WebSocket
- FFmpeg
- HTTP
- TCP
- 其他相关技术

---

## 5. 使用算法

本项目使用了以下算法：

- 3DMM（3维人脸重建算法）集成
- NERF（神经辐射传输算法）训练数据集深度学习
- OpenFace AUV（自动标注关键点）收集图像进行推理生成 CSV 坐标数据集
- DeepSpeech 对音频进行特征提取和推理

---

## 6. 主要项目 - ER-NeRF

ER-NeRF 项目是本项目的核心部分，主要实现了对数据的推理和处理。具体操作方式如下：

- 使用 `tts.py` 进行操作。
- 启用命令为 `python tts.py data/01/ --workspace trial_vrh_torso/ -O`。
- 使用 data 目录中的数据进行数据推理。
- `trial_vrh_torso` 是包含身体的模型。
- 启用之后可部署在本地，也可以使用命令启用 FastAPI 服务，端口为 8000。

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.31.199", port=8000)
```

---

## 7. 测试请求

使用 `request.py` 进行测试请求。

```python
python request.py
```

---

## 8. 推拉流服务

使用 `stream_video.py` 启用推拉流服务。可以使用 VLC 进行拉流，端口为 7000。在 Python 中内置 IP 对应自己的 IP 地址即可，已做了跨域请求。

拉流 m3u8 文件对应 `/hls.m3u8`，都为 GET 请求。

---

## 9. Apache 许可证说明

本项目采用 Apache 许可证 2.0，允许用户自由使用、修改和分发项目的源代码和衍生作品，同时还保留了原作者的著作权。

### Apache 许可证概述

Apache 许可证是一种自由软件许可证，它为用户提供了广泛的权利，包括使用、修改和分发软件的源代码和衍生作品。该许可证还包括了对于源代码的修改和分发需要包含原始版权声明和许可证条款的要求。

### 主要特点

- 允许私有修改和商业发布
- 允许修改后的代码被闭源化
- 需要包含原始版权声明和许可证条款
- 不提供任何担保或保证

### 适用性

Apache 许可证通常适用于开源软件项目，特别是那些希望吸引商业和开源用户的项目。由于其灵活性和广泛的适用性，许多开源项目选择采用 Apache 许可证。

### 注意事项

使用本项目的源代码或衍生作品时，请务必遵守 Apache 许可证的条款和条件，并且在使用、修改和分发时包含原始版权声明和许可证条款。

## 10. 结束语

以上为本项目的规范文档，包括项目介绍、结构、技术栈、算法、主要项目以及测试等方面的说明。希望本文档能够为项目的开发和维护提供参考和指导。包括了 Apache 许可证的说明。
