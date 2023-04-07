import asyncio
import edge_tts
from flask import Flask, request, send_file

OUTPUT_FILE = "test.mp3"


async def _main(text, voice) -> None:
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(OUTPUT_FILE)


def main(text, voice) -> None:
    asyncio.get_event_loop().run_until_complete(_main(text, voice))


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route('/tts', methods=['POST'])
    async def tts():
        text = request.form['text']
        voice = request.form['voice']
        await _main(text, voice)
        return send_file(OUTPUT_FILE, mimetype='audio/mpeg')

    app.run()
