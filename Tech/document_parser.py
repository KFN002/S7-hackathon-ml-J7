import os
import pdfplumber
import pytesseract
from PIL import Image
import docx
import json


class DocumentProcessor:
    def __init__(self, storage_path="documents"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.documents = {}

    def extract_text_from_pdf(self, file_path):
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text

    def extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def extract_text_from_image(self, file_path):
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

    def process_file(self, file_path):
        ext = file_path.split('.')[-1].lower()
        if ext == "pdf":
            return self.extract_text_from_pdf(file_path)
        elif ext == "docx":
            return self.extract_text_from_docx(file_path)
        elif ext in ["png", "jpg", "jpeg"]:
            return self.extract_text_from_image(file_path)
        else:
            with open(file_path, 'r', encoding='utf-8') as file:
                return file.read()

    def save_document(self, file_id, file_path):
        text = self.process_file(file_path)
        self.documents[file_id] = text
        return text

    def get_all_text(self):
        return "\n".join(self.documents.values())


processor = DocumentProcessor()
