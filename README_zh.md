# Edge-TTS HTTP 服务

一个基于 Microsoft Edge TTS 引擎的 HTTP 服务，通过 RESTful API 提供文字转语音功能，支持多语言和多种声音。

[English](README.md) | [中文](README_zh.md)

## 特性

- 🌍 支持多种语言和声音
- 🚀 支持流式和非流式音频输出
- 🔧 简单的 REST API 接口
- 🐳 支持 Docker 部署
- ⚡ 低延迟响应

## 快速开始

### 方式一：直接运行

1. 克隆仓库：
```bash
git clone https://github.com/doctoroyy/edge-tts-as-a-service
cd edge-tts-as-a-service
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 启动服务：
```bash
python main.py
```

服务将在 `http://localhost:5000` 启动

### 方式二：Docker 部署

1. 构建镜像：
```bash
docker build -t edge-tts-as-a-service .
```

2. 运行容器：
```bash
docker run -d -p 5000:5000 edge-tts-as-a-service
```

## API 文档

### 1. 获取可用声音列表

获取所有支持的声音选项。

```
GET /voices
```

响应示例：
```json
{
    "code": 200,
    "message": "OK",
    "data": [
        {
            "Name": "zh-CN-YunxiNeural",
            "ShortName": "zh-CN-YunxiNeural",
            "Gender": "Male",
            "Locale": "zh-CN"
        },
        // ... 更多声音选项
    ]
}
```

### 2. 文本转语音（下载）

将文本转换为语音文件并下载。

```
POST /tts
```

请求体：
```json
{
    "text": "你好，世界！",
    "voice": "zh-CN-YunxiNeural",  // 可选，默认为 "zh-CN-YunxiNeural"
    "file_name": "hello.mp3"       // 可选，默认为 "test.mp3"
}
```

响应：
- Content-Type: audio/mpeg
- 返回音频文件流

### 3. 文本转语音（流式）

将文本转换为语音并以流式方式返回，适合实时播放场景。

```
POST /tts/stream
```

请求体：
```json
{
    "text": "你好，世界！",
    "voice": "zh-CN-YunxiNeural"  // 可选，默认为 "zh-CN-YunxiNeural"
}
```

响应：
- Content-Type: application/octet-stream
- 返回音频数据流

## 使用示例

### Python 示例

```python
import requests

# 获取可用声音列表
response = requests.get('http://localhost:5000/voices')
voices = response.json()['data']

# 文本转语音（下载）
data = {
    "text": "你好，世界！",
    "voice": "zh-CN-YunxiNeural",
    "file_name": "output.mp3"
}
response = requests.post('http://localhost:5000/tts', json=data)
with open('output.mp3', 'wb') as f:
    f.write(response.content)

# 文本转语音（流式）
response = requests.post('http://localhost:5000/tts/stream', json=data, stream=True)
with open('stream_output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### curl 示例

```bash
# 获取可用声音列表
curl http://localhost:5000/voices

# 文本转语音（下载）
curl -X POST http://localhost:5000/tts \
    -H "Content-Type: application/json" \
    -d '{"text":"你好，世界！", "voice":"zh-CN-YunxiNeural"}' \
    --output output.mp3

# 文本转语音（流式）
curl -X POST http://localhost:5000/tts/stream \
    -H "Content-Type: application/json" \
    -d '{"text":"你好，世界！", "voice":"zh-CN-YunxiNeural"}' \
    --output stream_output.mp3
```

## 常见问题

1. **Q: 如何选择合适的声音？**  
   A: 通过 `/voices` 接口获取所有可用的声音列表，根据 Locale（地区）和 Gender（性别）选择合适的声音。

2. **Q: 支持哪些语言？**  
   A: 支持多种语言，包括中文、英语、日语等。具体可通过 `/voices` 接口查看完整的支持语言列表。

3. **Q: 音频文件格式是什么？**  
   A: 服务生成的音频文件格式为 MP3。

## 注意事项

- 推荐在生产环境中使用 Docker 部署
- 服务对文本长度有限制，建议将长文本分段处理
- 默认端口为 5000，可通过环境变量配置

## 参与贡献

欢迎提交 Issue 和 Pull Request。在提交 PR 之前，请确保：

1. 代码符合项目规范
2. 添加必要的测试
3. 更新相关文档

## 许可证

[MIT License](LICENSE)