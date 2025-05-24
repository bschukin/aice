from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered



def main():

    converter = PdfConverter(artifact_dict=create_model_dict(),)
    rendered = converter("nontext.pdf")
    text, _, images = text_from_rendered(rendered)
    print("======")
    print(text)
    print("======")
    print(images)

if __name__ == '__main__':
    main()


