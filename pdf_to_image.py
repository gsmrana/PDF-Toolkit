import os
import pymupdf
from PIL import Image
    
def pdf_to_image(pdf_path, output_dir, dpi=72, format=".png", from_page=1, to_page=None):
    pdf = pymupdf.open(pdf_path)
    to_page = to_page if to_page else pdf.page_count
    
    os.makedirs(output_dir, exist_ok=True)
    for page_num in range(from_page, to_page + 1):
        image_file = f"Page_{page_num:03d}{format}"
        print(f"Processing pdf page {page_num} of {to_page}: {image_file}")
        page = pdf[page_num-1]
        
        # Render page to image (higher dpi = better quality)
        zoom = dpi / 72  # 72 is default dpi
        mat = pymupdf.Matrix(zoom, zoom)
        pix = page.get_pixmap(matrix=mat)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_path = os.path.join(output_dir, image_file)
        img.save(image_path)

    pdf.close()
    print("Page extracted:", to_page - from_page + 1)
    print("Images saved to:", output_dir)

if __name__ == "__main__":
    input_pdf = "input.pdf"
    root, ext = os.path.splitext(input_pdf)
    output_dir = f"{root}_Extracted_Pages"
    
    print("Extracting Images...")
    pdf_to_image(input_pdf, output_dir, dpi=72, format=".jpg")
