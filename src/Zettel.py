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
    section_lines = list()
    for line in lines:
        if len(line) > 0:
            if not section_started and line.startswith(f"## {section}"):
                section_started = True
            elif section_started and line.startswith(f"## "):
                break
            elif section_started:
                section_lines.append(line)
    if return_list:
        return section_lines
    else:
        return "\n".join(section_lines)





