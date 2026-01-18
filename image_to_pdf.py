import os
import pymupdf
from PIL import Image

def combine_pdfs(pdf_dir, clean_garbage=0, optimize=False):
    pdf_doc = pymupdf.open()
    pdf_files = sorted([f for f in os.listdir(pdf_dir) if f.lower().endswith(('.pdf'))])
    
    for idx, image_file in enumerate(pdf_files):
        print(f"Processing pdf {idx + 1} of {len(pdf_files)}: {image_file}")
        image_path = os.path.join(pdf_dir, image_file)
        img_doc = pymupdf.open(image_path)
        pdf_bytes = img_doc.convert_to_pdf()
        img_pdf = pymupdf.open("pdf", pdf_bytes)
        pdf_doc.insert_pdf(img_pdf)
        img_doc.close()

    output_pdf = os.path.join(pdf_dir, f"{pdf_dir}_Combined.pdf")
    pdf_doc.save(output_pdf, garbage=clean_garbage, deflate=optimize, clean=optimize, deflate_images=optimize)
    pdf_doc.close()
    print("Total combined PDFs:", len(pdf_files))
    print("PDF output saved to:", output_pdf) 

# page_size = [None, "A4", "Letter"]
def image_to_pdf(image_dir, output_pdf, clean_garbage=4, optimize=True, page_size=None):
    pdf_doc = pymupdf.open()
    global_page_rect = pymupdf.paper_rect(page_size) if page_size else None
    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))])
    
    for idx, image_file in enumerate(image_files):
        print(f"Processing image {idx + 1} of {len(image_files)}: {image_file}")
        image_path = os.path.join(image_dir, image_file)
        img_doc = pymupdf.open(image_path)
        page_rect = global_page_rect if page_size else img_doc[0].rect
        page = pdf_doc.new_page(
            width=page_rect.width,
            height=page_rect.height
        )
        page.insert_image(
            page.rect, 
            filename=image_path, 
            keep_proportion=True
        )
        img_doc.close()

    pdf_doc.save(output_pdf, garbage=clean_garbage, deflate=optimize, clean=optimize, deflate_images=optimize)
    pdf_doc.close()
    print("Total combined images:", len(image_files))
    print("PDF output saved to:", output_pdf)

def webp_to_pdf(image_dir, output_pdf):
    image_files = sorted([f for f in os.listdir(image_dir) if f.lower().endswith(('.webp', '.jpg'))])
    
    images = []
    for idx, image_file in enumerate(image_files):
        print(f"Processing image {idx + 1} of {len(image_files)}: {image_file}")
        image_path = os.path.join(image_dir, image_file)
        img = Image.open(image_path)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        images.append(img)

    if images:
        images[0].save(
            output_pdf, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=images[1:]
        )
    print("Total combined images:", len(image_files))
    print("PDF output saved to:", output_pdf)

if __name__ == "__main__":
    input_dir = "Input_Images"
    output_pdf = os.path.join(input_dir, "Combined.pdf")

    #combine_pdfs(input_dir)
    image_to_pdf(input_dir, output_pdf)
