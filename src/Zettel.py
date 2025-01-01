"""
This module handels all stuff related to the Zettel Class
"""

import re


class Zettel:
    """
    This class abstracts a Zettel of a Zettelkasten.
    """

    def __init__(
        self,
        text: str = "",
        file_name: str = "",
        text_section_name: str = "Text",
        link_section_name: str = "Links",
        source_section_name: str = "Quelle",
    ) -> None:
        """
        Initiliase one Zettel. text is the text of Zettel,
        file_name the file name of Zettel.
        text_section_name is the md heading of text section.
        link_section_name is the md heading of link section.
        source_section_name is the md heading of source section.
        """
        self.raw_text = text
        self.file_name = file_name
        self.tags = extract_tags(text)
        self.title = extract_title(text)
        self.links = extract_section(text, link_section_name)
        zettel_text = extract_section(text, text_section_name, return_list=False)
        self.text = zettel_text.replace("\n", " ")

        self.source = extract_section(text, source_section_name, return_list=False)


def extract_tags(text: str):
    """
    checks that no letter and no hashtag comes before and after e.g #aue#uaioe
    so all hashtags are seperated by blank spaces
    tags have the structure hashtag letter
    """
    pat = re.compile(r"(?<![\w#])#\w+(?![\w#])")

    tags = re.findall(pat, text)

    return tags


def extract_title(text: str):
    """
    Function extracts the title from the text.
    """
    lines = text.split("\n")
    found_title = False
    title = ""
    for n_line, line in enumerate(lines):
        # case where we have two or more titles
        if found_title and line.startswith("# "):
            raise ParseErrorException(
                line=n_line, exceptionSource="DoubleTitle", text=text
            )
        # normal case where we find the title
        if not found_title and line.startswith("# "):
            found_title = True
            title = line[2:]
    if found_title:
        return title
    else:
        raise ParseErrorException(exceptionSource="NoTitleFound")


def extract_section(text: str, section_name: str, return_list: bool = True):
    """
    Extracts the section with section_name from text.
    returns list of liste if return of list is true
    otherwise we return a string.
    """
    lines = text.splitlines()
    section_started = False
    section_completed = False
    section_found = False
    section_lines = list()
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) > 0:
            # we found the head of the section
            if (
                not section_started
                and line.startswith(f"## {section_name}")
                and not section_completed
            ):
                section_started = True
                section_found = True
            # we found the end of the section
            elif section_started and line.startswith("## "):
                section_completed = True
                section_started = False
            # we add the line as it is part of the section
            elif section_started:
                section_lines.append(line)
            # here we have a double section
            if line.startswith(f"## {section_name}") and section_completed:
                raise ParseErrorException(line=i, exceptionSource="doubleSection")
    if not section_found:
        raise ParseErrorException(
            exceptionSource="noSectionFound", text=f"""section:{section_name}\n{text}"""
        )
    if return_list:
        return section_lines
    else:
        return "\n".join(section_lines)


class ParseErrorException(Exception):
    """
    Exception class for the case, where Zettel class can't parse a text.
    """

    def __init__(self, line: int = -1, exceptionSource: str = "", text: str = ""):
        """
        Initialise.
        line is the line in the text,
        exceptionSource details the parsing problem,
        text is the causing text.
        """
        self.line = line
        self.exception_source = exceptionSource
        self.text = text
        super().__init__(f"line {line}: {exceptionSource} \n {text}")
