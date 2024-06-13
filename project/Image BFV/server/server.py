from flask import Flask, request, render_template
import numpy as np
from numpy.polynomial import polynomial as poly
from PIL import Image
import pickle
import os


def polymul(x, y, modulus, poly_mod):
    return np.int64(np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus))


def polyadd(x, y, modulus, poly_mod):
    return np.int64(np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus))


def encrypt(pk, size, q, t, poly_mod, pt):
    m = np.array([pt] + [0] * (size - 1), dtype=np.int64) % t
    delta = q // t
    scaled_m = delta * m
    e1 = np.int64(np.random.normal(0, 2, size=size))
    e2 = np.int64(np.random.normal(0, 2, size=size))
    u = np.random.randint(0, 2, size, dtype=np.int64)
    ct0 = polyadd(
        polyadd(polymul(pk[0], u, q, poly_mod), e1, q, poly_mod), scaled_m, q, poly_mod)
    ct1 = polyadd(polymul(pk[1], u, q, poly_mod), e2, q, poly_mod)
    return (ct0, ct1)


def add_cipher(ct1, ct2, q, poly_mod):
    new_ct0 = polyadd(ct1[0], ct2[0], q, poly_mod)
    new_ct1 = polyadd(ct1[1], ct2[1], q, poly_mod)
    return (new_ct0, new_ct1)


def read_image(file_path):
    with Image.open(file_path) as img:
        return np.array(img.convert("RGB"), dtype=np.int64)


def encrypt_image(pk, size, q, t, poly_mod, file_path):
    image_arr = read_image(file_path)
    ct_r, ct_g, ct_b = [], [], []
    for pt_r, pt_g, pt_b in zip(image_arr[:, :, 0].flatten(), image_arr[:, :, 1].flatten(), image_arr[:, :, 2].flatten()):
        ct_r.append(encrypt(pk, size, q, t, poly_mod, pt_r))
        ct_g.append(encrypt(pk, size, q, t, poly_mod, pt_g))
        ct_b.append(encrypt(pk, size, q, t, poly_mod, pt_b))
    return (ct_r, ct_g, ct_b)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt_route():
    files = request.files.getlist('files[]')
    n = 2**4  # polynomial modulus degree
    q = 2**15  # ciphertext modulus
    t = 2**8  # plaintext modulus
    poly_mod = np.array([1] + [0] * (n - 1) + [1])

    public_key_file = request.files['public_key']
    public_key_file_path = public_key_file.filename
    with open(public_key_file_path, 'rb') as f:
        pk = pickle.load(f)
    
    encrypted_images = []
    for file in files:
        file_path = os.path.join('images', file.filename)
        file.save(file_path)
        encrypted_images.append(encrypt_image(
            pk, n, q, t, poly_mod, file_path))

    combined_ct_r = [add_cipher(add_cipher(ct1, ct2, q, poly_mod), ct3, q, poly_mod)
                    for ct1, ct2, ct3 in zip(encrypted_images[0][0], encrypted_images[1][0], encrypted_images[2][0])]
    combined_ct_g = [add_cipher(add_cipher(ct1, ct2, q, poly_mod), ct3, q, poly_mod)
                    for ct1, ct2, ct3 in zip(encrypted_images[0][1], encrypted_images[1][1], encrypted_images[2][1])]
    combined_ct_b = [add_cipher(add_cipher(ct1, ct2, q, poly_mod), ct3, q, poly_mod)
                    for ct1, ct2, ct3 in zip(encrypted_images[0][2], encrypted_images[1][2], encrypted_images[2][2])]
    combined_ct = (combined_ct_r, combined_ct_g, combined_ct_b)

    with open('../client/cipher.pkl', 'wb') as f:
        pickle.dump(combined_ct, f)

    return 'Encryption done. Ciphertext passed to client.'


if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')
    app.run(port=5000, debug=True)
