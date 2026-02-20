import inspect

import edge_tts
from flask import Flask, Response, jsonify, request, send_file
from flask_cors import CORS

OUTPUT_FILE = "/tmp/test.mp3"
DEFAULT_VOICE = "zh-CN-YunxiNeural"
COMMUNICATE_OPTION_KEYS = tuple(
    name
    for name in inspect.signature(edge_tts.Communicate.__init__).parameters
    if name not in {"self", "text", "connector"}
)
LIST_VOICE_OPTION_KEYS = tuple(
    name
    for name in inspect.signature(edge_tts.list_voices).parameters
    if name not in {"connector"}
)

app = Flask(__name__)
CORS(app, supports_credentials=True)


def stream_audio_chunks(communicate):
    for chunk in communicate.stream_sync():
        if chunk["type"] == "audio":
            yield chunk["data"]


def parse_json_payload():
    data = request.get_json(silent=True)
    if data is None:
        raise ValueError("Invalid or missing JSON body.")
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object.")
    return data


def parse_text(data):
    text = data.get("text")
    if not isinstance(text, str) or not text.strip():
        raise ValueError("`text` is required and must be a non-empty string.")
    return text


def build_communicate_kwargs(data):
    if "connector" in data:
        raise ValueError("`connector` is not supported via HTTP API.")

    kwargs = {key: data[key] for key in COMMUNICATE_OPTION_KEYS if key in data}
    if "voice" not in kwargs:
        kwargs["voice"] = DEFAULT_VOICE
    return kwargs


def make_response(code, message, data=None):
    response = {
        'code': code,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), code


@app.route('/tts', methods=['POST'])
def tts():
    try:
        data = parse_json_payload()
        text = parse_text(data)
        communicate_kwargs = build_communicate_kwargs(data)

        audio_fname = data.get("audio_fname") or data.get("file_name") or OUTPUT_FILE
        metadata_fname = data.get("metadata_fname") or data.get("metadata_file")

        communicate = edge_tts.Communicate(text, **communicate_kwargs)
        communicate.save_sync(audio_fname, metadata_fname=metadata_fname)

        return send_file(audio_fname, mimetype='audio/mpeg')
    except ValueError as e:
        return make_response(400, str(e))
    except Exception as e:
        return make_response(500, str(e))


@app.route('/tts/stream', methods=['POST'])
def stream_audio_route():
    try:
        data = parse_json_payload()
        text = parse_text(data)
        communicate_kwargs = build_communicate_kwargs(data)
        communicate = edge_tts.Communicate(text, **communicate_kwargs)

        return Response(stream_audio_chunks(communicate), content_type='audio/mpeg')
    except ValueError as e:
        return make_response(400, str(e))
    except Exception as e:
        return make_response(500, str(e))


@app.route('/voices', methods=['GET'])
async def voices():
    try:
        if "connector" in request.args:
            return make_response(400, "`connector` is not supported via HTTP API.")
        list_voices_kwargs = {
            key: request.args.get(key)
            for key in LIST_VOICE_OPTION_KEYS
            if key in request.args
        }
        voices = await edge_tts.list_voices(**list_voices_kwargs)
        return make_response(200, 'OK', voices)
    except Exception as e:
        return make_response(500, str(e))


if __name__ == "__main__":

    app.run()
