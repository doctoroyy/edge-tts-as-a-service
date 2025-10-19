import asyncio
import edge_tts
from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS

OUTPUT_FILE = "/tmp/test.mp3"
app = Flask(__name__)
CORS(app, supports_credentials=True)


async def stream_audio(text, voice, rate=None, volume=None, pitch=None) -> None: # type: ignore
    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
    for chunk in communicate.stream_sync():
        if chunk["type"] == "audio":
            yield chunk["data"] # type: ignore


def audio_generator(text, voice, rate=None, volume=None, pitch=None):
    loop = asyncio.new_event_loop()
    coroutine = stream_audio(text, voice, rate, volume, pitch)
    while True:
        try:
            chunk = loop.run_until_complete(coroutine.__anext__()) # type: ignore
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
def tts():
    data = request.get_json()
    text = data['text']
    # voice not required
    voice = data.get('voice', 'zh-CN-YunxiNeural')
    file_name = data.get('file_name', OUTPUT_FILE)
    # Optional parameters for speech customization
    rate = data.get('rate')  # e.g., "+50%", "-50%"
    volume = data.get('volume')  # e.g., "+50%", "-50%"
    pitch = data.get('pitch')  # e.g., "+50Hz", "-50Hz"

    communicate = edge_tts.Communicate(text, voice, rate=rate, volume=volume, pitch=pitch)
    communicate.save_sync(file_name)
    return send_file(file_name, mimetype='audio/mpeg')


@app.route('/tts/stream', methods=['POST'])
async def stream_audio_route():
    data = request.get_json()
    text = data['text']
    voice = data.get('voice', 'zh-CN-YunxiNeural')
    # Optional parameters for speech customization
    rate = data.get('rate')  # e.g., "+50%", "-50%"
    volume = data.get('volume')  # e.g., "+50%", "-50%"
    pitch = data.get('pitch')  # e.g., "+50Hz", "-50Hz"

    return Response((audio_generator(text, voice, rate, volume, pitch)), content_type='application/octet-stream')


@app.route('/voices', methods=['GET'])
async def voices():
    try:
        voices = await edge_tts.list_voices()
        return make_response(200, 'OK', voices)
    except Exception as e:
        return make_response(500, str(e))


if __name__ == "__main__":

    app.run()
