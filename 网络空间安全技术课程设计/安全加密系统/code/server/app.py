from flask import Flask, request, render_template, send_from_directory
from cryptography.hazmat.primitives import serialization, padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import os

app = Flask(__name__)

PRIVATE_KEY_PATH = './keys/private_key.pem'
UPLOADS_DIRECTORY = './uploads'


def decrypt_data(encrypted_data):
    with open(PRIVATE_KEY_PATH, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data


@app.route('/', methods=['GET'])
def index():
    file_list = os.listdir(UPLOADS_DIRECTORY)
    return render_template('index.html', files=file_list)


@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(UPLOADS_DIRECTORY, filename)


@app.route('/upload', methods=['POST'])
def upload_file():
    encrypted_data = request.data
    filename = request.headers.get('filename')
    decrypted_data = decrypt_data(encrypted_data)
    print(f"Encrypted content of file '{filename}':")
    print(decrypted_data.decode())
    with open(os.path.join(UPLOADS_DIRECTORY, filename), 'wb') as file:
        file.write(decrypted_data)
    return 'File uploaded successfully'


if __name__ == '__main__':
    app.run(host='localhost', port=4041)
