from flask import Flask, request, send_file, render_template
import numpy as np
from numpy.polynomial import polynomial as poly
from PIL import Image
import pickle
import os


def polymul(x, y, modulus, poly_mod):
    return np.int64(np.round(poly.polydiv(poly.polymul(x, y) % modulus, poly_mod)[1] % modulus))


def polyadd(x, y, modulus, poly_mod):
    return np.int64(np.round(poly.polydiv(poly.polyadd(x, y) % modulus, poly_mod)[1] % modulus))


def decrypt(sk, size, q, t, poly_mod, ct):
    scaled_pt = polyadd(polymul(ct[1], sk, q, poly_mod), ct[0], q, poly_mod)
    delta = q // t
    decrypted_poly = np.round(scaled_pt / delta) % t
    return int(decrypted_poly[0])


def read_image(file_path):
    with Image.open(file_path) as img:
        return np.array(img.convert("RGB"), dtype=np.int64)


def array_to_image(arr, shape):
    return Image.fromarray(np.uint8(np.reshape(arr, shape)))


def decrypt_to_array(sk, size, q, t, poly_mod, ct):
    decrypted_arr = []
    for c in ct:
        decrypted_arr.append(decrypt(sk, size, q, t, poly_mod, c))
    return decrypted_arr


def decrypt_(sk, size, q, t, poly_mod, ct):
    decrypted_r = decrypt_to_array(sk, size, q, t, poly_mod, ct[0])
    decrypted_g = decrypt_to_array(sk, size, q, t, poly_mod, ct[1])
    decrypted_b = decrypt_to_array(sk, size, q, t, poly_mod, ct[2])
    decrypted_img = np.stack([decrypted_r, decrypted_g, decrypted_b], axis=-1)
    return decrypted_img


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/decrypt', methods=['POST'])
def decrypt_route():
    n = 2**4  # polynomial modulus degree
    q = 2**15  # ciphertext modulus
    t = 2**8  # plaintext modulus
    poly_mod = np.array([1] + [0] * (n - 1) + [1])

    cipher_file = request.files['ciphertext']
    image_files = request.files.getlist('images')

    cipher_file_path = cipher_file.filename
    image_file_paths = []

    for image_file in image_files:
        image_file_path = os.path.join('images', image_file.filename)
        image_file.save(image_file_path)
        image_file_paths.append(image_file_path)

    with open(cipher_file_path, 'rb') as f:
        combined_ct = pickle.load(f)
    with open('secret_key.pkl', 'rb') as f:
        sk = pickle.load(f)

    decrypted_combined_array = decrypt_(sk, n, q, t, poly_mod, combined_ct)

    image1_array = read_image(image_file_paths[0])
    image2_array = read_image(image_file_paths[1])

    decrypted_combined_array = np.array(
        decrypted_combined_array).reshape(image1_array.shape)
    
    subtracted_array_tmp = [(combined - img1) % t for combined, img1 in zip(
        decrypted_combined_array.reshape(-1, 3), image1_array.reshape(-1, 3))]
    subtracted_array = [(combined - img2) % t for combined, img2 in zip(
        np.array(subtracted_array_tmp).reshape(-1, 3), image2_array.reshape(-1, 3))]
    subtracted_array = np.array(subtracted_array).reshape(image1_array.shape)

    subtracted_img = array_to_image(subtracted_array, image1_array.shape)
    subtracted_img.save("subtracted_image.png")

    return send_file("subtracted_image.png", mimetype='image/png')


if __name__ == "__main__":
    if not os.path.exists('images'):
        os.makedirs('images')
    app.run(port=5001, debug=True)
