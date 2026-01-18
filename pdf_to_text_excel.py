import pymupdf
import pdfplumber
import pandas as pd

def extract_text_tables_plumber(pdf_path, output_txt, output_excel=None, password=None):
    excel_writer = pd.ExcelWriter(output_excel, engine="openpyxl")
    pdf_doc = pdfplumber.open(pdf_path, password=password)
    text_pages = []
    text_pages.append(f"========== PDF File: {pdf_path}, Total Pages: {len(pdf_doc.pages)}  ==========")
    
    for page_num, page in enumerate(pdf_doc.pages):
        print(f"Processing page {page_num+1} of {len(pdf_doc.pages)}")
        text_pages.append(f"\r\r==================== Page {page_num+1} ====================\r")
        text_pages.append(page.extract_text())
        tables = page.extract_tables()
        for table_num, table in enumerate(tables):
            print(f"  Processing table {table_num+1} of {len(tables)}")
            df = pd.DataFrame(table[1:], columns=table[0])
            df.to_excel(excel_writer, sheet_name=f"Page{page_num+1:02d}_Table{table_num:02d}", index=False)

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(''.join(text_pages))
    pdf_doc.close()
    print("Text output saved to:", output_txt)
    
    if output_excel:
        if len(excel_writer.sheets):
            excel_writer.close()
            print("Tables output saved to:", output_excel)
        else:
            print("WARNIING: No Tables found!")

def extract_text_tables_pymupdf(pdf_path, output_txt, output_excel=None, password=None):
    pdf_doc = pymupdf.open(pdf_path)    
    if pdf_doc.is_encrypted:
        if not pdf_doc.authenticate(password):
            raise ValueError("Invalid PDF password")

    excel_writer = pd.ExcelWriter(output_excel, engine="openpyxl")
    text_pages = []
    text_pages.append(f"========== PDF File: {pdf_path}, Total Pages: {len(pdf_doc)}  ==========")

    for page_num, page in enumerate(pdf_doc):
        print(f"Processing page {page_num+1} of {len(pdf_doc)}")
        text_pages.append(f"\r\r==================== Page {page_num+1} ====================\r")
        text_pages.append(page.get_text())
        tables = page.find_tables() # bodered tables
        for table_num, table in enumerate(tables):
            print(f"  Processing table {table_num+1}")
            df = table.to_pandas()
            df.to_excel(excel_writer, sheet_name=f"Page{page_num+1:02d}_Table{table_num:02d}", index=False)

    with open(output_txt, 'w', encoding='utf-8') as f:
        f.write(''.join(text_pages))
    pdf_doc.close()
    print("Text output saved to:", output_txt)
    
    if output_excel:
        if len(excel_writer.sheets):
            excel_writer.close()
            print("Tables output saved to:", output_excel)
        else:
            print("WARNIING: No Tables found!")

if __name__ == "__main__":
    input_pdf = "input.pdf"

    #extract_text_tables_plumber(input_pdf, "Text_Output_plumber.txt", "Tables_Output_plumber.xlsx")
    extract_text_tables_pymupdf(input_pdf, "Text_Output_pymupdf.txt", "Tables_Output_pymupdf.xlsx")
