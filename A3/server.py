from flask import Flask, request, jsonify
import os

# modal load code


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is running!"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_unique_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{name}_{counter}{ext}"
        counter += 1
    
    return new_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    print("Request form:", request.form)
    print("Request files:", request.files.keys())

    # ✅ First, try to get the file from multipart/form-data
    if 'filename' in request.files:
        uploaded_file = request.files['filename']
        if uploaded_file.filename == '':
            return "No file selected", 400

        unique_filename = get_unique_filename(UPLOAD_FOLDER, uploaded_file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        uploaded_file.save(save_path)

        
        # return jsonify({"message": "File uploaded successfully!", "filename": unique_filename}), 200

    # ✅ If no file in `request.files`, fallback to raw binary data
    raw_data = request.get_data()
    if raw_data:
        unique_filename = get_unique_filename(UPLOAD_FOLDER, "uploaded_image.jpg")
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        with open(file_path, "wb") as f:
            f.write(raw_data)

        # return jsonify({"message": "File uploaded as binary!", "filename": unique_filename}), 200

    # return "No file received", 400


@app.route('/upload2', methods=['POST'])
def upload2():
    # ✅ Handling JSON Data
    if request.is_json:
        data = request.get_json()
        print("Received JSON Data:", data)

        # Extract specific fields from JSON (modify as needed)
        distance = data.get("distance", "N/A")
        light = data.get("light", "N/A")
        latitude = data.get("latitude", "N/A")
        longitude = data.get("longitude", "N/A")
        ax = data.get("ax", "N/A")
        ay = data.get("ay", "N/A")
        az = data.get("az", "N/A")
        gx = data.get("gx", "N/A")
        gy = data.get("gy", "N/A")
        gz = data.get("gz", "N/A")

        # Save structured data to a log file
        os.makedirs("data_logs", exist_ok=True)
        with open("data_logs/sensor_data.txt", "a") as f:
            f.write(f"Distance: {distance}, Light: {light}, Lat: {latitude}, Long: {longitude}, "
                    f"AX: {ax}, AY: {ay}, AZ: {az}, GX: {gx}, GY: {gy}, GZ: {gz}\n")

    # ✅ Handling File Uploads (Images)
    if "filename" in request.files:
        uploaded_file = request.files["filename"]
        if uploaded_file.filename != "":
            os.makedirs("uploads", exist_ok=True)
            save_path = os.path.join("uploads", uploaded_file.filename)
            uploaded_file.save(save_path)
            return jsonify({
                "message": "File and data uploaded successfully!",
                "filename": uploaded_file.filename
            }), 200
    
    predict()
    # return jsonify({"message": "Data received without a file"}), 200


def predict():
    prediction = ''
    # modal run code
    return prediction


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

