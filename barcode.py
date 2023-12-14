from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import cv2
from pyzbar.pyzbar import decode
import os
import tempfile

app = Flask(__name__)

# Method to decode the barcode
def BarcodeReader(image_path):
    # Read the image in numpy array using cv2
    img = cv2.imread(image_path)

    # Decode the barcode image
    detectedBarcodes = decode(img)

    result = []

    # If not detected then add a message to the result
    if not detectedBarcodes:
        result.append({"message": "Barcode Not Detected or your barcode is blank/corrupted!"})
    else:
        # Traverse through all the detected barcodes in image
        for barcode in detectedBarcodes:
            result.append({"barcode_data": barcode.data.decode("utf-8"), "barcode_type": barcode.type})

    return result

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        # Use tempfile to handle temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            file.save(temp_file.name)
            barcode_info = BarcodeReader(temp_file.name)

        # File will be deleted after exiting the with block

        return jsonify(barcode_info)

if __name__ == "__main__":
    app.run(debug=True)
