from picamera2 import Picamera2
import cv2, time, io

camera = None

def init_camera():
    """
    Initialise and configure the Raspberry Pi camera.
    
    This:
    1. Creates a new Picamera2 instance
    2. Sets up the preview config with a resolution of 640x480
    3. Aligns the configuration (ensures hardware compatibility)
    4. Configures the camera with the preview configuration
    5. Starts the camera
    
    This function should be called before the gen_frames function.
    """
    global camera
    camera = Picamera2()
    camera.preview_configuration.main.size = (1280, 720)
    camera.preview_configuration.main.format = 'RGB888'
    camera.preview_configuration.align()
    camera.configure('preview')
    camera.start()
    
def gen_frames():
    """
    Generator function that continuously yields frames for streaming on the website.
    
    This:
    1. Captures an image from the camera
    2. Converts the image to .JPEG format
    3. Yields the image with proper HTTP headers
    
    Yields:
        bytes: Frame data in multipart/x-mixed-replace format for HTTP streaming
        
    Raises:
        RuntimeError: If the camera has not been initialised
    """
    global camera
    if camera is None:
        raise RuntimeError('Camera not initialised. Call init_camera() first.')
    
    while True:
        im = camera.capture_array()
        
        _, buffer = cv2.imencode('.jpg', im)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
        time.sleep(0.05)