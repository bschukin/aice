from typing import List

from pydantic import BaseModel, Field, field_validator
from rich.console import Console
from rich.markdown import Markdown

from pushkin.prompts.pushkin_commands_schema import ChangeItem, PushkinResponse
from utils.sugar import substring_after, iif

console = Console()


def print_markdown(text):
    md = Markdown(text)
    console.print(md)


def insert_section_into_markdown(content, target_header, new_content, delete_target_header: bool = False) -> str:
    """
    Вставляет новый раздел после указанного заголовка в Markdown содержимое.

    :param content: Строка с содержимым MD файла
    :param target_header: Заголовок, после которого нужно вставить новый раздел (например, "# Схема")
    :param new_content: Содержимое нового раздела
    :return: Модифицированное содержимое
    """
    lines = content.split('\n')
    new_section = f"\n{new_content}\n"
    result = []
    found = False

    for line in lines:
        if line.strip() == target_header and not found:
            if not delete_target_header:
                result.append(line)
            result.append(new_section)
            found = True
        else:
            result.append(line)

    return '\n'.join(result)

class MdElement(BaseModel):
    def getMDText(self)->str:
        return ""

class Line(MdElement):
    text: str
    def getMDText(self)->str:
        return self.text

class Subsection(MdElement):
    name: str
    content: List[Line] = Field(default=[])

    def getMDText(self)->str:
        content_str = "\n".join(line.getMDText() for line in self.content)
        return f"## {self.name}\n{content_str}"

    def findLine(self, line:str)->Line:
        return next((item for item in self.content if isinstance(item, Line) and (string_is_string(item.text, line))), None)

    def findAndDeleteLine(self, line:str)->Line|None:
        l = self.findLine(line)
        if l is None:
            return None
        self.content.remove(l)
        return l

    def findAndChangeLine(self, old_line:str, new_line:str)->Line|None:
        l = self.findLine(old_line)
        if l is None:
            return None
        index = self.content.index(l)
        self.content.remove(l)
        self.content.insert(index, Line(text=new_line))
        return l



class Section(MdElement):
    name: str
    content: list[Line | Subsection] = Field(default=[])

    def getMDText(self)->str:
        content_str = "\n".join(line.getMDText() for line in self.content)
        return f"# {self.name}\n{content_str}"

    def findSubsection(self, section:str)->Subsection:
        return next((item for item in self.content if isinstance(item, Subsection) and string_is_string(item.name,section) ), None)

    def addSubsection(self, section)->Subsection:
        s = Subsection(name=section)
        self.content.append(s)
        return s

    def findOrAddSubsection(self, section):
        if section is None:
            return None
        return self.findSubsection(section) or self.addSubsection(section)

class MD(MdElement):
    content: list[Line | Section] = Field(default=[])

    def getMDText(self)->str:
        content_str = "\n".join(line.getMDText() for line in self.content)
        return content_str

    def findSection(self, section:str)->Section:
        return next((item for item in self.content if isinstance(item, Section) and string_is_string(item.name,  section)), None)

    def addSection(self, section)->Section:
        s = Section(name=section)
        self.content.append(s)
        return s

    def findOrAddSection(self, section):
        if section is None:
            return None
        return self.findSection(section) or self.addSection(section)



def buildMDTree(text: str) -> MD:
    lines = text.split('\n')
    curr_section:Section | None = None
    curr_subsection: Section  | None = None
    md = MD()
    for line in lines:
        node = switch_match(line)
        match node:
            case Section():
                curr_section = node
                curr_subsection = None
                md.content.append(node)
            case Subsection():
                curr_subsection = node
                curr_section.content.append(node)
            case Line():
                if curr_subsection:
                    curr_subsection.content.append(node)
                else:
                    if curr_section:
                        curr_section.content.append(node)
                    else:
                        md.content.append(node)

    return md


def switch_match(value: str) -> (Line | Subsection | Section):
    v = value.strip()
    match v:
        case _ if v.startswith("## "):
            return Subsection(name=substring_after(v, "## "))
        case _ if v.startswith("# "):
            return Section(name=substring_after(v, "# "))
        case _:
            return Line(text=v)


def apply_md_changes(md_text: str, changes: PushkinResponse) -> str:
    return apply_markdown_changes(md_text, changes.changes_made)

def apply_markdown_changes(md_text: str, changes: List[ChangeItem]) -> str:
    result = buildMDTree(md_text)

    for change in changes:
        if change.type == "add":
            handle_add(result, change)
        elif change.type == "edit":
            handle_edit(result, change)
        elif change.type == "delete":
            handle_delete(result, change)
        elif change.type == "move":
            raise Exception("t0d0")

    return result.getMDText()

def handle_add(tree:MD, item:ChangeItem):
    section = tree.findOrAddSection(item.section)
    subsection = section.findOrAddSubsection(item.subsection)
    line = item.new_text
    if subsection is not None:
        subsection.content.append(Line(text=line))
    else:
        section.content.append(Line(text=line))

def handle_edit(tree:MD, item:ChangeItem):
    section = tree.findOrAddSection(item.section)
    subsection = section.findOrAddSubsection(item.subsection)

    if subsection is not None:
        subsection.findAndChangeLine(item.old_text, item.new_text)
    else:
        raise Exception("is it fiasko")
        #section.content.append(Line(text=line))


def handle_delete(tree:MD, item:ChangeItem):
    section = tree.findOrAddSection(item.section)
    subsection = section.findOrAddSubsection(item.subsection)
    old_lines = item.old_text.split('\n')

    for line in old_lines:
        l = subsection.findAndDeleteLine(line)
        print(l)

def string_is_string(str1:str, str2:str)->bool:
    s1 = str1.lower().strip()  #todo еще удалять все пробелы внутри строки
    s2 = str2.lower().strip()  #todo еще удалять все пробелы внутри строки

    if not s1 and s2:
        return False
    if s1 and not s2:
        return False

    return s1==s2 or s1 in s2 or s2 in s1


