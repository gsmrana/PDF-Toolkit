# PDF Toolkit
A collection of pdf utility tools.

## Environment Setup

Install Python and UV Package Manager

https://docs.astral.sh/uv/getting-started/installation

```
winget install --id Python.Python.3.12
winget install --id=astral-sh.uv  -e
```

Install packages in a virtual environment

```
uv sync
```

Upgrade all packages

```
uv lock --upgrade
uv sync
```

## PDF/Image Conversion

```
uv run pdf_to_image.py
uv run image_to_pdf.py

```

## PDF/Text Extraction

```
uv run pdf_to_text_excel.py
uv run image_to_ocr_text.py
```
