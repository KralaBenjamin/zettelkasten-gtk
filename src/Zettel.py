import re


class Zettel:
    def __init__(self, text = "",
                 file_name = "",
                 text_section_name = "Text",
                 link_section_name = "Links",
                 source_section_name = "Quelle") -> None:
        self.raw_text = text
        self.file_name = file_name
        self.tags = extract_tags(text)
        self.title = extract_title(text)
        self.links = extract_section(text, link_section_name)
        zettel_text = extract_section(text, text_section_name, return_list=False)
        self.text = zettel_text.replace("\n", " ")

        self.quelle = extract_section(text, source_section_name, return_list=False)


def extract_tags(text):
    pat = re.compile("#\w+[\s+\n]") # Checks for hashtags like #example
    tags = re.findall(pat, text)
    tags = [tag[:-1] for tag in tags]

    return tags


def extract_title(text):
    lines = text.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]


def extract_section(text, section, return_list = True):
    lines = text.split("\n")
    section_started = False
    section_completed = False
    section_found = False
    section_lines = list()
    for i, line in enumerate(lines):
        line = line.strip()
        if len(line) > 0:
            if not section_started \
                    and line.startswith(f"## {section}")\
                    and not section_completed:
                section_started = True
                section_found = True
            elif section_started and line.startswith(f"## "):
                section_completed = True
                section_started = False
            elif section_started:
                section_lines.append(line)
            if line.startswith(f"## {section}")\
                    and section_completed:
                ## here we have a double section
                raise ParseErrorException(line = i, exceptionSource="doubleSection")
    if not section_found:
        raise ParseErrorException(exceptionSource="noSectionFound",
                                  text=f"""
section:{section}
{text}
""")
    if return_list:
        return section_lines
    else:
        return "\n".join(section_lines)


class ParseErrorException(Exception):

    def __init__(self, line = -1,
                 exceptionSource = "",
                 text=""):
        self.line = line
        self.exceptionSource = exceptionSource
        self.text = text
        super().__init__(f"line {line}: {exceptionSource} \n {text}")
