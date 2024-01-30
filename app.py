import os
import threading
import subprocess

from api.constants import Path

def run_script(script_name):
    subprocess.run(["python", script_name])
    
def run_chainlit():
    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        subprocess.Popen(["chainlit", "run", Path.CHATBOT_PROCESS_PATH.value , "--headless"])

if __name__ == '__main__':
    # Start the chatbot_process.py script in a separate thread
    #hreading.Thread(target=run_script, args=(Path.CHATBOT_PROCESS_PATH.value,)).start()
    
    run_chainlit()
    # Start the api_controller.py script in a separate thread
    threading.Thread(target=run_script, args=(Path.API_PROCESS_PATH.value,)).start()