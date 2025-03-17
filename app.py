from flask import Flask, Response, render_template, request, jsonify, url_for
import os
import live_feed
import timelapse
import settings

if not os.path.exists('secrets.txt'):
    raise FileNotFoundError('secrets.txt not found. Please create this file and add a password hash.')

app = Flask(__name__)

# Initialise camera
live_feed.init_camera()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/live_feed')
def live_feed_route():
    # Use the gen_frames function from the live_feed module
    return Response(live_feed.gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/timelapse')
def timelapse_page():
    return render_template('timelapse.html')

@app.route('/timelapse_route', methods=['POST'])
def timelapse_route():
    data = request.get_json()
    selected_date = data.get('date')
    
    if not selected_date:
        return jsonify({'error': 'No date provided.'}), 400
    
    video_path = timelapse.retrieve_timelapse(selected_date)

    if video_path:
        video_url = url_for('static', filename=f'videos/{os.path.basename(video_path)}')
        return jsonify({'video_url': video_url})
    else:
        return jsonify({'error': 'Timelapse video not found.'}), 404

@app.route('/settings', methods=['GET', 'POST'])
def settings_route():
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if settings.verify_password(password):
            return render_template('settings.html')
        else:
            error = 'Invalid password.'
    return render_template('settings.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)