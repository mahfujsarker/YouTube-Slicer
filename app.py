from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_resolutions(url):
    ydl_opts = {'format': 'bestvideo+bestaudio/best', 'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        resolutions = [f"{format['format_id']} - {format['height']}p" for format in info['formats'] if 'height' in format]
        return resolutions

@app.route('/')
def index():
    return '''
    <h2>YouTube Video Downloader</h2>
    <form action="/download" method="post">
        <label for="url">YouTube URL:</label>
        <input type="text" id="url" name="url" required>
        <button type="submit">Download Video</button>
    </form>
    '''

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    resolutions = get_resolutions(url)
    return jsonify(resolutions)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
