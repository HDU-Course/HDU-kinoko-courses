from flask import Flask, render_template, request, redirect, url_for
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import requests

app = Flask(__name__)

PUBLIC_KEY_PATH = './keys/public_key.pem'


def encrypt_file(file_path):
    with open(file_path, 'rb') as file:
        file_data = file.read()

    with open(PUBLIC_KEY_PATH, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

    encrypted_data = public_key.encrypt(
        file_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return encrypted_data


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(file.filename)
            encrypted_data = encrypt_file(file.filename)
            response = requests.post(
                'http://localhost:4041/upload',
                data=encrypted_data,
                headers={'filename': file.filename}
            )
            return redirect(url_for('upload_file'))
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='localhost', port=4040)
