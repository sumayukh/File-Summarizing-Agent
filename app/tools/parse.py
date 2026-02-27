import pdfplumber
import docx

class ParserService:
    def __init__(self, file_stream, mime_type):
        self.file_stream = file_stream
        self.mime_type = mime_type

    def parse_pdf(self, file_stream):
        text = ""
        with pdfplumber.open(file_stream) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def parse_docx(self, file_stream):
        document = docx.Document(file_stream)
        return "\n".join([para.text for para in document.paragraphs])

    def parse_txt(self, file_stream):
        return file_stream.read().decode("utf-8")
    
    def parse_file(self):
        match self.mime_type:
            case "application/pdf":
                return self.parse_pdf(self.file_stream)
            case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self.parse_docx(self.file_stream)
            case "text/plain":
                return self.parse_txt(self.file_stream)
            case _:
                raise ValueError(f"Unsupported file type: {self.mime_type}")