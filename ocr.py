import cv2
import pytesseract
import json
import numpy as np
from difflib import SequenceMatcher
from flask import Flask, render_template, request
import os
from PIL import Image
from pymongo import MongoClient

app = Flask(__name__)

# Constants
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
THRESHOLD_VALUE = 130
LANG = "ind"
ALLOWED_FIELDS = ["NIK", "Nama"]
GROUND_TRUTH = {"NIK": "3205190901000005", "Nama": "DIMAS WAHYUDI"}

# Inisialisasi koneksi MongoDB
mongo_client = MongoClient(
    "mongodb://magangitg:bWFnYW5naXRn@database2.pptik.id:27017/magangitg"
)
db = mongo_client["magangitg"]
collection = db["ktp_ocr"]


# Function Definitions


def similarity_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def calculate_accuracy(ground_truth, extracted_text):
    return similarity_ratio(ground_truth, extracted_text) * 100


def extract_data(image_path):
    try:
        with open(image_path, "rb") as img_file:
            img = cv2.imdecode(
                np.frombuffer(img_file.read(), np.uint8), cv2.IMREAD_COLOR
            )

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshed = cv2.threshold(gray, THRESHOLD_VALUE, 200, cv2.THRESH_BINARY)

        result = pytesseract.image_to_string(
            threshed,
            lang=LANG,
            config="--psm 6 --oem 3 --dpi 300 -c tessedit_char_blacklist=@#$?%^&*()- ",
        )
        return result
    except Exception as e:
        return str(e)


def parse_extracted_data(extracted_text):
    data = {}
    lines = extracted_text.split("\n")
    nik = ""
    nama = ""

    for line in lines:
        for field in ALLOWED_FIELDS:
            if field in line:
                field_value = line.split(":", 1)
                if len(field_value) == 2:
                    field, value = field_value
                    data[field.strip()] = value.strip()
                else:
                    nik_parts = line.split()
                    for part in nik_parts:
                        if part.isdigit() and len(part) >= 10:
                            nik = part
                            data["NIK"] = nik
                            break
                    if not nik:
                        nama = line.strip()
                        data["Nama"] = nama
    return data


def filter_data(data):
    return {field: data[field] for field in ALLOWED_FIELDS if field in data}


def create_json_data(new_filename, filtered_data):
    ordered_data = {"nama_file": new_filename}
    json_data = json.dumps(ordered_data | filtered_data, indent=3)
    return json_data


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file part")

        file = request.files["file"]

        if file and allowed_file(file.filename):
            temp_file_path = "static/temp_image.jpg"
            file.save(temp_file_path)
            result_image_path = os.path.join("static", "result_image.jpg")

            try:
                extracted_text = extract_data(temp_file_path)
                extracted_data = parse_extracted_data(extracted_text)
                filtered_data = filter_data(extracted_data)

                img = Image.open(temp_file_path)
                new_width = 1040
                new_height = 780
                img = img.resize((new_width, new_height), Image.BILINEAR)

                img_np = np.fromfile(temp_file_path, np.uint8)
                img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                _, threshed = cv2.threshold(
                    gray, THRESHOLD_VALUE, 200, cv2.THRESH_BINARY
                )
                result_image_path = os.path.join("static", "result_image.jpg")

                cv2.imwrite(
                    result_image_path,
                    threshed,
                    [int(cv2.IMWRITE_JPEG_QUALITY), 100],
                )

                nik_accuracy = calculate_accuracy(
                    GROUND_TRUTH["NIK"], filtered_data.get("NIK", "")
                )
                nama_accuracy = calculate_accuracy(
                    GROUND_TRUTH["Nama"], filtered_data.get("Nama", "")
                )
                json_data = create_json_data(temp_file_path, filtered_data)
                result = {
                    "json_data": json_data,
                    "nik_accuracy": nik_accuracy,
                    "nama_accuracy": nama_accuracy,
                }
                collection.insert_one(filtered_data)

                uploaded_image_url = result_image_path
                return render_template(
                    "result.html", result=result, uploaded_image_url=result_image_path
                )

            except cv2.error as e:
                return render_template("index.html", error=f"OpenCV Error: {str(e)}")
            except pytesseract.TesseractError as e:
                return render_template("index.html", error=f"Tesseract Error: {str(e)}")
            except Exception as e:
                return render_template("index.html", error=f"Error: {str(e)}")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
