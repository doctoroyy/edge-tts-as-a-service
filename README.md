# Edge-TTS HTTP Service

This is a simple HTTP service that uses the Edge-TTS library to generate text-to-speech audio files.

## Installation

1. Clone this repository
2. Install the required dependencies using `pip install -r requirements.txt`
3. Run the server using `python main.py`

## Usage

### POST /tts

Generates an audio file from the provided text and voice, and returns it as a response.

#### Request Body

```json
{
  "text": "Hello, world!",
  "voice": "en-US-GuyNeural",
  "file_name": "output.mp3"
}
```

- `text` (required): The text to be converted to speech.
- `voice` (optional): The name of the voice to use for the conversion. Defaults to "zh-CN-YunxiNeural".
- `file_name` (optional): The name of the output file. Defaults to "test.mp3".

#### Response

The generated audio file will be returned as a response with the content type "audio/mpeg".

### POST /tts/stream

Streams the generated audio file as a response.

#### Request Body

```json
{
  "text": "Hello, world!",
  "voice": "en-US-GuyNeural"
}
```

- `text` (required): The text to be converted to speech.
- `voice` (optional): The name of the voice to use for the conversion. Defaults to "zh-CN-YunxiNeural".

#### Response

The generated audio file will be streamed as a response with the content type "application/octet-stream".
