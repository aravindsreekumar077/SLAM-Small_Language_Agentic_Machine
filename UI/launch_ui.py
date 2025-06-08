import subprocess
import webbrowser
import time
import socket

#This file starts the streamlit app

def wait_for_port(port, host="localhost", timeout=5):
    start_time = time.time()
    while True:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.2)

# Start Streamlit server
process = subprocess.Popen(
    ["streamlit", "run", "main_ui.py", "--server.headless", "true"],
    shell = True
)

# Wait until port 8501 is open
if wait_for_port(8501):
    webbrowser.open("http://localhost:8501")
else:
    print("Streamlit server didn't start in time!")
