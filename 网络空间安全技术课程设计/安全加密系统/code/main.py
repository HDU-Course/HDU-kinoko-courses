import subprocess

def start_client():
    subprocess.Popen(['python', './client/app.py'])

def start_server():
    subprocess.Popen(['python', './server/app.py'])

if __name__ == '__main__':
    start_server()
    start_client()
