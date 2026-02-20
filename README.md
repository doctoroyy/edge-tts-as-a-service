# Edge-TTS HTTP Service

A simple HTTP service that provides Text-to-Speech functionality using Microsoft Edge's TTS engine, supporting multiple languages and voices through RESTful APIs.

[English](README.md) | [中文](README_zh.md)

## Features

- 🌍 Multiple languages and voices support
- 🚀 Both streaming and non-streaming audio output
- 🔧 Simple REST API interface
- 🐳 Docker support
- ⚡ Low latency response

## Quick Start

### Option 1: Run Directly

1. Clone the repository:
```bash
git clone https://github.com/doctoroyy/edge-tts-as-a-service
cd edge-tts-as-a-service
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the service:
```bash
python main.py
```

The service will be available at `http://localhost:5000`

### Option 2: Docker Deployment

1. Build the image:
```bash
docker build -t edge-tts-as-a-service .
```

2. Run the container:
```bash
docker run -d -p 5000:5000 edge-tts-as-a-service
```

## API Documentation

### 1. List Available Voices

Retrieve all supported voice options.

```
GET /voices
```

Query parameters:

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `proxy` | string | No | None | Proxy URL passed to `edge_tts.list_voices(proxy=...)` |

Response example:
```json
{
    "code": 200,
    "message": "OK",
    "data": [
        {
            "Name": "en-US-GuyNeural",
            "ShortName": "en-US-GuyNeural",
            "Gender": "Male",
            "Locale": "en-US"
        },
        // ... more voices
    ]
}
```

### 2. Text-to-Speech (Download)

Convert text to speech and download the audio file.

```
POST /tts
```

Request body:
```json
{
    "text": "Hello, World!",
    "voice": "en-US-GuyNeural",    // Optional, defaults to "zh-CN-YunxiNeural"
    "rate": "+20%",
    "volume": "+0%",
    "pitch": "+0Hz",
    "proxy": "http://127.0.0.1:7890",
    "connect_timeout": 10,
    "receive_timeout": 60,
    "audio_fname": "hello.mp3",
    "metadata_fname": "hello.vtt"
}
```

Supported request parameters:

| Parameter | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `text` | string | Yes | - | Input text |
| `voice` | string | No | `zh-CN-YunxiNeural` | Voice name |
| `rate` | string | No | `+0%` | Speaking rate |
| `volume` | string | No | `+0%` | Volume gain |
| `pitch` | string | No | `+0Hz` | Pitch |
| `proxy` | string/null | No | `None` | Proxy URL |
| `connect_timeout` | number/null | No | `10` | Connection timeout (seconds) |
| `receive_timeout` | number/null | No | `60` | Receive timeout (seconds) |
| `audio_fname` | string | No | `/tmp/test.mp3` | Output audio file path |
| `metadata_fname` | string/null | No | `None` | Metadata output path (`edge-tts` subtitles/metadata) |

Compatibility aliases:
- `file_name` is still supported as an alias of `audio_fname`.
- `metadata_file` is still supported as an alias of `metadata_fname`.

Response:
- Content-Type: audio/mpeg
- Returns audio file stream

### 3. Text-to-Speech (Streaming)

Convert text to speech with streaming output, suitable for real-time playback.

```
POST /tts/stream
```

Request body:
```json
{
    "text": "Hello, World!",
    "voice": "en-US-GuyNeural",
    "rate": "+20%",
    "volume": "+0%",
    "pitch": "+0Hz",
    "proxy": "http://127.0.0.1:7890",
    "connect_timeout": 10,
    "receive_timeout": 60
}
```

Response:
- Content-Type: audio/mpeg
- Returns audio stream

Note:
- `connector` is a Python object and is not accepted through HTTP JSON.

## Usage Examples

### Python Example

```python
import requests

# Get available voices
response = requests.get('http://localhost:5000/voices')
voices = response.json()['data']

# Text-to-Speech (Download)
data = {
    "text": "Hello, World!",
    "voice": "en-US-GuyNeural",
    "rate": "+10%",
    "volume": "+0%",
    "pitch": "+0Hz",
    "audio_fname": "output.mp3",
    "metadata_fname": "output.vtt"
}
response = requests.post('http://localhost:5000/tts', json=data)
with open('output.mp3', 'wb') as f:
    f.write(response.content)

# Text-to-Speech (Streaming)
response = requests.post('http://localhost:5000/tts/stream', json=data, stream=True)
with open('stream_output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

### curl Example

```bash
# Get available voices
curl http://localhost:5000/voices

# Text-to-Speech (Download)
curl -X POST http://localhost:5000/tts \
    -H "Content-Type: application/json" \
    -d '{"text":"Hello, World!", "voice":"en-US-GuyNeural", "rate":"+10%", "pitch":"+2Hz"}' \
    --output output.mp3

# Text-to-Speech (Streaming)
curl -X POST http://localhost:5000/tts/stream \
    -H "Content-Type: application/json" \
    -d '{"text":"Hello, World!", "voice":"en-US-GuyNeural", "rate":"+10%"}' \
    --output stream_output.mp3
```

## Frontend Project

### 🚨 React Frontend Companion Project 🚨

**Looking for a ready-to-use frontend interface?**

🔗 **Quick Link**: [react-audio-stream-demo](https://github.com/doctoroyy/react-audio-stream-demo)

This React demo provides a fully functional frontend for seamless TTS interaction, making it easy to demonstrate and integrate the Edge-TTS service with a user-friendly interface.

## FAQ

1. **Q: How do I choose the right voice?**  
   A: Use the `/voices` endpoint to get a list of all available voices. Choose based on the Locale and Gender attributes.

2. **Q: What languages are supported?**  
   A: Multiple languages including English, Chinese, Japanese, etc. Check the `/voices` endpoint for a complete list.

3. **Q: What is the audio file format?**  
   A: The service generates MP3 audio files.

## Notes

- Docker deployment is recommended for production environments
- The service has a text length limit; consider splitting long texts
- Default port is 5000, configurable through environment variables

## Contributing

Issues and Pull Requests are welcome. Before submitting a PR, please:

1. Ensure your code follows the project style
2. Add necessary tests
3. Update relevant documentation

## License

[MIT License](LICENSE)
