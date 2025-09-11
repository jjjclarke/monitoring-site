# monitoring-site

## Setup

This project requires a Raspberry Pi with a Raspberry Pi Camera (or another suitable camera) connected. If you don't have a camera connected, the site should *in theory* still work, but I haven't been able to test it!

Before the site can run, you'll need to run the `setup.sh` script, which is used to generate the secret key (required for Flask) and semi-encrypted password for the settings page.

Once the script is completed (you should then have a `key.txt` and `secret.txt` file in your project directory), you'll need to create a virtual environment with Python, activate it, and install Flask:

```
python3 -m venv venv
source venv/bin/activate
pip install flask
deactivate
```

Getting the camera to work with this site can be... difficult, to say the least. This is the method that worked for me in the past:

Install OpenCV as a *system package* with `sudo apt-get install -y python3-opencv`, and then create a symbolic link:

```
cd venv/lib/python3*/site-packages/
ln -s /usr/lib/python3/dist-packages/cv2.* .
```

Once that's done, you can run the site:

```
cd ../../../..
python3 app.py
```