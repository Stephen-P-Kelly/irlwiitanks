import io
import logging
import socketserver
from http import server
from threading import Condition

from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# HTML page for the MJPEG streaming demo
PAGE = """\
<html>
<head>
  <meta charset="UTF-8">
  <title>Pi Cam Stream</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <style>
    html, body {
      margin: 0;
      padding: 0;
      background-color: black;
      width: 100%;
      height: 100%;
      overflow: hidden;
    }

    body {
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
    }

    #stream {
      width: 100vw;
      height: auto;
      max-height: 100vh;
      object-fit: contain;
      background: black;
    }

    #fullscreen-btn {
      position: absolute;
      bottom: 20px;
      right: 20px;
      z-index: 10;
      background-color: rgba(255, 255, 255, 0.2);
      color: white;
      border: 1px solid white;
      border-radius: 4px;
      padding: 8px 14px;
      font-size: 16px;
      cursor: pointer;
    }

    @media (orientation: landscape) {
      #stream {
        width: auto;
        height: 100vh;
      }
    }
  </style>
</head>
<body>
  <img id="stream" src="stream.mjpg" alt="Live Camera Stream">
  <button id="fullscreen-btn" onclick="toggleFullscreen()">Fullscreen</button>

  <script>
    function toggleFullscreen() {
      const el = document.documentElement;
      if (el.requestFullscreen) {
        el.requestFullscreen();
      } else if (el.webkitRequestFullscreen) { // Safari
        el.webkitRequestFullscreen();
      } else if (el.msRequestFullscreen) { // IE11
        el.msRequestFullscreen();
      }
    }

    // Optional: allow screen orientation to follow device
    if (screen.orientation && screen.orientation.unlock) {
      screen.orientation.unlock().catch(() => {}); // Not supported in all browsers
    }
  </script>
</body>
</html>
"""






# Class to handle streaming output
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

# Class to handle HTTP requests
class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            # Redirect root path to index.html
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Serve the HTML page
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            # Set up MJPEG streaming
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            # Handle 404 Not Found
            self.send_error(404)
            self.end_headers()

# Class to handle streaming server
class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

# Create Picamera2 instance and configure it
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}))
output = StreamingOutput()
picam2.start_recording(JpegEncoder(), FileOutput(output))

try:
    # Set up and start the streaming server
    address = ('', 8000)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    # Stop recording when the script is interrupted
    picam2.stop_recording()
