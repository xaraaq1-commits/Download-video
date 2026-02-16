from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def get_video_info(url):
    ydl_opts = {
        'format': 'best', # Cari kualitas terbaik
        'quiet': True,
        'no_warnings': True,
        # Kita tidak mau download ke server, cuma mau ambil Info URL nya saja
        'simulate': True, 
        'forceurl': True, 
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ekstrak informasi video
            info = ydl.extract_info(url, download=False)
            
            # Ambil data yang diperlukan
            return {
                'status': 'success',
                'title': info.get('title', 'Video tanpa judul'),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': info.get('url', ''), # Ini link direct videonya
                'platform': info.get('extractor_key', 'Unknown'),
                'duration': info.get('duration_string', 'N/A')
            }
    except Exception as e:
        return {'status': 'error', 'message': str(e)}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'status': 'error', 'message': 'URL tidak boleh kosong!'})

    # Proses mendapatkan info video
    result = get_video_info(url)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

