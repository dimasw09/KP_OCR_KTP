import cv2
import pytesseract
import json

def extract_text_from_image(img_path):
    try:
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, threshed = cv2.threshold(gray, 170, 255, cv2.THRESH_TRUNC)

        result = pytesseract.image_to_string(threshed, lang="ind")

        data = {}
        for line in result.split("\n"):
            if "”—" in line:
                line = line.replace("”—", ":")
            line = line.replace("?", "7").replace("b", "6")

            if ":" in line:
                key, value = map(str.strip, line.split(":", 1))
                data[key] = value
            print(data)
        return data
    except Exception as e:
        raise Exception(f"Error extracting text from image: {str(e)}")

def filter_data(data):
    filtered_data = {
        key: value for key, value in data.items() if key.lower() in ["nik", "nama"]
    }
    return filtered_data

def create_json_data(image_file, filtered_data):
    ordered_data = {"nama file": image_file, **filtered_data}
    json_data = json.dumps(ordered_data, indent=3, ensure_ascii=False)
    return json_data

if __name__ == "__main__":
    image_file = "KTPscan/ktp (4).jpeg"
    
    try:
        extracted_data = extract_text_from_image(image_file)
        filtered_data = filter_data(extracted_data)
        json_data = create_json_data(image_file, filtered_data)
        print(json_data)
    except Exception as e:
        print(f"Error processing image {image_file}: {str(e)}")
