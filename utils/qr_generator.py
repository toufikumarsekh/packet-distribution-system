import qrcode
import os


def generate_qr(qr_url):

    folder = "static/qr_codes"

    if not os.path.exists(folder):
        os.makedirs(folder)

    token = qr_url.split("/")[-1]

    filename = f"{token}.png"

    filepath = os.path.join(
        folder,
        filename
    )

    qr = qrcode.make(qr_url)

    qr.save(filepath)

    return filename