import asyncio
import edge_tts
from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS

OUTPUT_FILE = "test.mp3"
app = Flask(__name__)
CORS(app, supports_credentials=True)


async def stream_audio(text, voice) -> None:
    communicate = edge_tts.Communicate(text, voice)
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            yield chunk["data"]


def audio_generator(text, voice):
    loop = asyncio.new_event_loop()
    coroutine = stream_audio(text, voice)
    while True:
        try:
            chunk = loop.run_until_complete(coroutine.__anext__())
            yield chunk
        except StopAsyncIteration:
            break


def make_response(code, message, data=None):
    response = {
        'code': code,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return jsonify(response)


@app.route('/tts', methods=['POST'])
async def tts():
    data = request.get_json()
    text = data['text']
    # voice not required
    voice = data.get('voice', 'zh-CN-YunxiNeural')
    file_name = data.get('file_name', OUTPUT_FILE)

    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file_name)
    return send_file(file_name, mimetype='audio/mpeg')


@app.route('/tts/stream', methods=['POST'])
async def stream_audio_route():
    data = request.get_json()
    text = data['text']
    voice = data.get('voice', 'zh-CN-YunxiNeural')

    return Response((audio_generator(text, voice)), content_type='application/octet-stream')


@app.route('/voices', methods=['GET'])
async def voices():
    try:
        voices = await edge_tts.list_voices()
        return make_response(200, 'OK', voices)
    except Exception as e:
        return make_response(500, str(e))


if __name__ == "__main__":

    app.run()
