from flask import Flask, render_template, request, redirect, url_for
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import requests

app = Flask(__name__)

# 公钥文件路径
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


def decrypt_data(encrypted_data, private_key):
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_data


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save(file.filename)
            encrypted_data = encrypt_file(file.filename)
            headers = {'filename': file.filename}
            response = requests.post('http://localhost:4041/upload', data=encrypted_data, headers=headers)
            return redirect(url_for('upload_file'))
    return render_template('index.html')


@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    if filename:
        response = requests.get('http://localhost:4041/download?filename=' + filename)
        encrypted_data = response.content

        with open('./downloads/' + filename, 'wb') as file:
            file.write(encrypted_data)

        with open('./keys/private_key.pem', 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        decrypted_data = decrypt_data(encrypted_data, private_key)

        with open('./downloads/decrypted_' + filename, 'wb') as file:
            file.write(decrypted_data)

    return redirect(url_for('upload_file'))


if __name__ == '__main__':
    app.run(host='localhost', port=4040)
