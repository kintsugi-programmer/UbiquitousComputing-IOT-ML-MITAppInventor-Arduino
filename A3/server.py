from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Request form:", request.form)
    print("Request files:", request.files.keys())

    # ✅ First, try to get the file from multipart/form-data
    if 'filename' in request.files:
        uploaded_file = request.files['filename']
        if uploaded_file.filename == '':
            return "No file selected", 400

        os.makedirs('uploads', exist_ok=True)
        save_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(save_path)

        return jsonify({"message": "File uploaded successfully!", "filename": uploaded_file.filename}), 200

    # ✅ If no file in `request.files`, fallback to raw binary data
    raw_data = request.get_data()
    if raw_data:
        os.makedirs('uploads', exist_ok=True)
        file_path = os.path.join('uploads', "uploaded_image.jpg")
        with open(file_path, "wb") as f:
            f.write(raw_data)

        return jsonify({"message": "File uploaded as binary!", "filename": "uploaded_image.jpg"}), 200

    return "No file received", 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
