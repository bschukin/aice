from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown

from pushkin.prompts.pushkin_commands_schema import ChangeItem, PushkinResponse
from utils.sugar import substring_after, iif, is_empty_or_whitespace

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
    :param delete_target_header
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
    text: str

    def getMDText(self) -> str:
        return ""


class Line(MdElement):

    def getMDText(self) -> str:
        stripped = self.text.strip()
        if not stripped:
            return self.text
        if stripped.startswith("-"):
            return self.text
        return "- " + self.text


class Section(MdElement):
    level: int = 0
    parent: Optional[Section] = None
    content: list[MdElement] = Field(default_factory=list)
    isNew: bool = False

    def _make_hashes(self) -> str:
        return '#' * (self.level + 1)

    def getMDText(self) -> str:
        content_str = "\n".join(line.getMDText() for line in self.content)
        return f"{self._make_hashes()} {self.text}\n{content_str}"

    def findParent(self, level: int) -> Optional[Section]:
        if self.level < level:
            return self
        if self.level == level:
            return self.parent
        if self.parent is None:
            return None
        return self.parent.findParent(level)

    def findSubsection(self, section: str) -> Section:
        return next(
            (item for item in self.content if isinstance(item, Section) and string_is_string(item.text, section)), None)

    def addSubsection(self, section) -> Section:
        s = Section(text=section, level=self.level + 1, isNew=True)
        self.content.append(s)
        return s

    def findOrAddSubsection(self, section):
        if section is None:
            return None
        return self.findSubsection(section) or self.addSubsection(section)

    def findNode(self, node: MdElement) -> MdElement | None:
        return next((item for item in self.content if string_is_string(item.text, node.text)), None)

    def findAndDeleteNode(self, node: MdElement) -> MdElement | None:
        n = self.findNode(node)
        if n is None:
            return None
        self.content.remove(n)
        return n

    def findLine(self, line: str) -> Line:
        return next((item for item in self.content if isinstance(item, Line) and (string_is_string(item.text, line))),
                    None)

    def findAndDeleteLine(self, line: str) -> Line | None:
        l = self.findLine(line)
        if l is None:
            return None
        self.content.remove(l)
        return l

    def findAndChangeLine(self, old_line: str, new_line: str) -> Line | None:
        l = self.findLine(old_line)
        if l is None:
            return None
        index = self.content.index(l)
        self.content.remove(l)
        self.content.insert(index, Line(text=new_line))
        return l


class MD(MdElement):
    text: str = ""
    content: list[Line | Section] = Field(default=[])

    def getMDText(self) -> str:
        content_str = "\n".join(line.getMDText() for line in self.content)
        return content_str

    def findOrAddSectionByPath(self, path: list[str]) -> Optional[Section]:
        section = None
        for sec in path:
            section = self.findOrAddSection(sec) if section is None else section.findOrAddSubsection(sec)
        return section

    def findSection(self, section: str) -> Section:
        return next(
            (item for item in self.content if isinstance(item, Section) and string_is_string(item.text, section)), None)

    def addSection(self, section) -> Section:
        s = Section(text=section)
        self.content.append(s)
        return s

    def findOrAddSection(self, section):
        if section is None:
            return None
        return self.findSection(section) or self.addSection(section)


def buildMDTree(text: str) -> MD:
    lines = text.split('\n')
    curr_section: Section | None = None
    md = MD()
    for line in lines:
        node = getNode(line)
        match node:
            case Section():
                parent = None if curr_section is None else curr_section.findParent(node.level)
                node.parent = parent
                if parent:
                    parent.content.append(node)
                else:
                    md.content.append(node)
                curr_section = node
            case Line():
                if curr_section:
                    curr_section.content.append(node)
                else:
                    md.content.append(node)
    return md


def getNode(value: str) -> (Line | Section):
    v = value.strip()
    match v:
        case _ if v.startswith("### "):
            return Section(text=substring_after(v, "### "), level=2)
        case _ if v.startswith("## "):
            return Section(text=substring_after(v, "## "), level=1)
        case _ if v.startswith("# "):
            return Section(text=substring_after(v, "# "), level=0)
        case _:
            return Line(text=substring_after(v, "-").strip())


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
            raise Exception("tod0")

    return result.getMDText()


def handle_add(tree: MD, item: ChangeItem):
    section = tree.findOrAddSectionByPath(item.sections)
    node = getNode(item.new_text)

    if section is not None:
        section.content.append(node)
    else:
        tree.content.append(node)


def handle_edit(tree: MD, item: ChangeItem):
    section = tree.findOrAddSectionByPath(item.sections)

    if section is not None:
        section.findAndChangeLine(item.old_text, item.new_text)
    else:
        raise Exception("is it fiasko")


def handle_delete(tree: MD, item: ChangeItem):
    if item.old_text is None:
        section = tree.findOrAddSectionByPath(item.sections[:-1])
        node = getNode(item.sections[-1])
    else:
        section = tree.findOrAddSectionByPath(item.sections)
        node = getNode(item.old_text)

    if section is not None:
        n = section.findAndDeleteNode(node)
    else:
        raise Exception("is it fiasko")


def string_is_string(str1: str, str2: str) -> bool:
    if not str1 and not  str2:
        return True

    s1 = str1.lower().strip()  # todo еще удалять все пробелы внутри строки
    s2 = str2.lower().strip()  # todo еще удалять все пробелы внутри строки

    if not s1 and s2:
        return False
    if s1 and not s2:
        return False

    return s1 == s2 or s1 in s2 or s2 in s1
