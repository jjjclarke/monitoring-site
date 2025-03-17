from flask import Flask, Response, render_template
import live_feed

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)