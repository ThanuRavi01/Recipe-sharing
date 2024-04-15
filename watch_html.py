import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

HTML_DIR = 'templates'
PYTHON_DIR = 'Projectfiles'

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.html'):
            html_file = os.path.basename(event.src_path)
            python_file = os.path.splitext(html_file)[0] + '.py'
            if python_file in os.listdir(PYTHON_DIR):
                print(f"Detected change in {html_file}, running {python_file}")
                stop_flask_server()
                start_flask_server(python_file)

def stop_flask_server():
    subprocess.run(['pkill', '-f', 'python app.py'])

def start_flask_server(python_file):
    subprocess.Popen(['python', os.path.join(PYTHON_DIR, python_file)])

if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=HTML_DIR, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

