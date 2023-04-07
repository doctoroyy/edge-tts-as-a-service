import asyncio
import edge_tts
from flask import Flask, Response, copy_current_request_context, request, send_file, stream_with_context

OUTPUT_FILE = "test.mp3"
app = Flask(__name__)


async def _main(text, voice, file_name) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_name)


def main(text, voice, file_name) -> None:
    asyncio.get_event_loop().run_until_complete(_main(text, voice, file_name))


async def stream_audio(text, voice) -> None:
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]
        elif chunk["type"] == "WordBoundary":
            print(f"WordBoundary: {chunk}")


def audio_generator(text, voice):
    loop = asyncio.new_event_loop()
    coroutine = stream_audio(text, voice)
    while True:
        try:
            chunk = loop.run_until_complete(coroutine.__anext__())
            yield chunk
        except StopAsyncIteration:
            break


@app.route('/tts', methods=['POST'])
async def tts():
    data = request.get_json()
    text = data['text']
    # voice not required
    voice = data.get('voice', 'zh-CN-YunxiNeural')
    file_name = data.get('file_name', OUTPUT_FILE)

    await _main(text, voice, file_name)
    return send_file(OUTPUT_FILE, mimetype='audio/mpeg')


@app.route('/tts/stream', methods=['POST'])
async def stream_audio_route():
    data = request.get_json()
    text = data['text']
    voice = data.get('voice', 'zh-CN-YunxiNeural')

    return Response((audio_generator(text, voice)), content_type='audio/mpeg')


if __name__ == "__main__":

    app.run()
