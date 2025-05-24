from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
from docx import Document

from paths import Paths


def read_pdf(project, file_name):
    path = Paths().get_project_artifact(project, artifact=file_name)
    converter = PdfConverter(artifact_dict=create_model_dict(), )
    rendered = converter(str(path))
    text, _, images = text_from_rendered(rendered)
    return text

def read_docx(project, file_name):
    path = Paths().get_project_artifact(project, artifact=file_name)
    doc = Document(str(path))
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)
