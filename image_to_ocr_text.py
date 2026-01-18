import os
import easyocr

ocr_reader = easyocr.Reader(['en'], gpu=False)
#ocr_reader = easyocr.Reader(['en', 'bn'], gpu=True)

def image_ocr(image_path, header):
    ocr_result = ocr_reader.readtext(image_path)
    page_text = f"\r\r==================== {header} ====================\r"
    page_text += '\r'.join([detection[1] for detection in ocr_result])
    return page_text

def extract_text_from_images(image_dir, output_name):
    ocr_pages = []
    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))])
    ocr_pages.append(f"========== Directory: {image_dir}, Total Images: {len(image_files)} ==========")
    
    for idx, image_file in enumerate(image_files):
        print(f"Processing image {idx + 1} of {len(image_files)}: {image_file}")
        image_path = os.path.join(image_dir, image_file)
        page_text = image_ocr(image_path, image_file)
        ocr_pages.append(page_text)
    
    ocr_output_file = os.path.join(image_dir, output_name)
    with open(ocr_output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(ocr_pages))
    print("Total image processed:", len(image_files))
    print("OCR output saved to:", ocr_output_file)

if __name__ == "__main__":
    input_dir = "Images"
        
    print("\nExtracting OCR Text...")
    extract_text_from_images(input_dir, "OCR_Output.txt")
