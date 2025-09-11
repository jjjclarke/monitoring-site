from flask import Flask, Response, render_template, request, jsonify, url_for, session
import os
import timelapse
import settings
import logger

# Setup logger
logger = logger.setup_logging(__name__)

# Check if the camera is available
camera_unavailable = False
try:
    import live_feed
    live_feed.init_camera() # Start the camera
    logger.info('Camera initialised successfully.')
except ModuleNotFoundError:
    camera_unavailable = True
    logger.warning('Camera is unavailable. Live feed will be disabled.')

if not os.path.exists('key.txt'):
    logger.error('Secret key not found. Please refer to the GitHub page for instructions on setting up a secret key.')
    raise FileNotFoundError('key.txt not found. Please create this file and add a secret key.')

if not os.path.exists('secrets.txt'):
    logger.error('Password file not found. Please refer to the GitHub page for instructions on setting up the admin password.')
    raise FileNotFoundError('secrets.txt not found. Please create this file and add a password hash.')

app = Flask(__name__)
app.secret_key = settings.get_secret_key()
logger.info('Application running...')

@app.route('/')
def index():
    logger.info('Request received for index page.')
    return render_template('index.html', camera_unavailable=camera_unavailable)

@app.route('/live_feed')
def live_feed_route():
    logger.info('Request received for live feed.')
    if camera_unavailable:
        return render_template('index.html', camera_unavailable=True)
    else:
        # Use the gen_frames function from the live_feed module
        return Response(live_feed.gen_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/timelapse')
def timelapse_page():
    logger.info('Request received for timelapse page.')
    return render_template('timelapse.html')

@app.route('/timelapse_route', methods=['POST'])
def timelapse_route():
    data = request.get_json()
    selected_date = data.get('date')
    
    if not selected_date:
        logger.warning('No date provided for timelapse.')
        return jsonify({'error': 'No date provided.'}), 400
    
    video_path = timelapse.retrieve_timelapse(selected_date)

    if video_path:
        video_url = url_for('static', filename=f'videos/{os.path.basename(video_path)}')
        logger.info(f'Timelapse found and returned: {video_path}')
        return jsonify({'video_url': video_url})
    else:
        logger.warning(f'Timelapse not found for date {selected_date}')
        return jsonify({'error': 'Timelapse video not found.'}), 404

@app.route('/settings', methods=['GET', 'POST'])
def settings_route():
    logger.info('Request received for settings page.')
    error = None
    if request.method == 'POST':
        password = request.form['password']
        if settings.verify_password(password):
            session['authenticated'] = True
            logger.info('A user has successfully logged into the admin portal.')
        else:
            error = 'Invalid password.'
            logger.warning('An invalid password was entered.')
    return render_template('settings.html', error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)