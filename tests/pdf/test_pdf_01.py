from anthropic import BaseModel

from pdf.pdf_monster import PdfMonster
from pdf.pdf_reader import read_pdf, read_docx
import justext


class Directive(BaseModel):
    """
    Класс, описываюший документ "Предписание"
    """
    publish_date: str  # пример формата "5 июня 2014 года"
    city: str  # Город, район
    case_number: str  # номер дела
    case_name: str  # наименование дела
    bid_notice_number: str  # номер  извещения об аукцыоне или конкурсе
    cancel: bool  # предпиcание требует аннулирования
    bid_lots: list[
        str]  # лоты (позиции) аукцона, в именительном падеже. Cтарайся найти и родительские категории позиции. например: 'На поставку медицинского оборудования: система ультразвуковой визуализации универсальная, с питанием от сети' -> ['медицинское оборудование. система ультразвуковой визуализации универсальная, с питанием от сети']
    bid: str  # наименование закупки, конкурса, аукциона
    organisations: list[str]  # список организаций
    complainant: str  # организация, подавшая жалобу
    commission_name: str  # наименование комиссии
    commission_members: list[str]  # члены комиссии
    complaint_resume: str  # резюме по жалобе или проблеме, на которую выносится предписание комиссии
    directive: str  # текст предписания как есть
    directive_end_date: str  # дата исполнения предписания
    penalty: str  # санкции в случае невыполнения предписания

class PolicyDoc(BaseModel):
    """
    Класс, описываюший документ "ПОЛОЖЕНИЕ О ЗАКУПКЕ"
    """
    policy_name: str  # Наименование документа.
    competitive_is_not_electronic:bool # Предусмотрено проведение конкурентных закупок не только в электронной форме
    date_report:str #Дата расчета сведений о закупках российского происхождения
    bid_security_start_amount:str # Размер обеспечения заявки относительно НМЦД
    bid_security_end_amound:str    #Размер обеспечения заявки до
    contract_security_advance_percent_threshold:str   #Процент размера аванса при превышении которого, размер обеспечения исполнения договора устанавливается в размере аванса
    ep_sgoz_percent:str #Процент закупки у единственного поставщика в совокупном годовом объеме закупок
    con_guarantee_disable:bool #conGuaranteeDisable

def test_pdf_prompt():
    p = PdfMonster()
    prompt = p._get_system_prompt()

    for item in prompt:
        print(item)


def test_pdf_read():
    txt = read_pdf("pdf", "2_Предписание.pdf")
    print(txt)


def test_pdf_direction():
    p = PdfMonster()
    t = p.get_result(Directive, "2_Предписание.pdf")
    print(t)

def test_docx_direction():
    p = PdfMonster()
    t = p.get_result_docx(PolicyDoc, "Татспиртпром.docx")
    print(t)


def test_word_read():
    txt = read_docx("pdf", "Татспиртпром.docx")
    #print(txt)
    txt2 = justext.justext(txt, justext.get_stoplist("Russian"))
    print()


    full_text = []
    for paragraph in txt2:
        if not paragraph.is_boilerplate:
            full_text.append(paragraph.text)

    txt3 = '\n'.join(full_text)
    print(len(txt))
    print(len(txt3))