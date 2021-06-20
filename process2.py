from lxml import etree
from pathlib import Path
from re import finditer, escape, compile, match
from pyinflect import getAllInflections
from docx import Document


with open("words.txt") as word_file:
    word_list = [
        word.strip() for word in word_file if not word.startswith("#") and word.strip()
    ]
print(len(word_list))

re_dict = {}
for word in word_list:
    word_re = f"({escape(word)})|({escape(word.capitalize())})"
    word_ext_set = set()
    for word_ext_list in getAllInflections(word, 'N').values():
        for word_ext in word_ext_list:
            word_ext_set.add(word_ext)
    for word_ext_list in getAllInflections(word, 'V').values():
        for word_ext in word_ext_list:
            word_ext_set.add(word_ext)
    for word_ext in word_ext_set:
        word_re += f"|({escape(word_ext)})|({escape(word_ext.capitalize())})"    
    word_re = r"(?<![a-zA-Z])(" + word_re + r")(?![a-zA-Z])"
    re_dict[word] = compile(word_re)


def find_all(word, text):
    return list(finditer(re_dict[word], text))


i = 0
data = []
for article_path in Path("articles").iterdir():
    print(article_path)
    with open(article_path) as article_file:
        html = etree.HTML(article_file.read())
        # print(etree.tostring(html))
        # title = match(r".*Passage 0[123] (.*)", article_path.stem)[1]
        title = article_path.stem
        # print(title)
        para_list = [p.text for p in html.cssselect("p") if p.text]

        article_data = {}
        article_data["title"] = title
        article_data["para"] = []
        appeared_set = set()
        for text in para_list:  # title?
            text_marked = []
            for word in word_list:
                if find_list := find_all(word, text):
                    appeared_set.add(word)
                    text_marked += find_list
            text_marked = sorted(text_marked, key=lambda m: m.start(0))
            # print(text_marked)
            article_data["para"].append({"text": text, "marked": text_marked})
        print(len(appeared_set))
        article_data["count"] = len(appeared_set)
        data.append(article_data)

    i += 1
    # if i > 10:
    #     break

data = sorted(data, key=lambda article: article["count"], reverse=True)

document = Document()
for article in data:
    # print(article["title"])
    # print(article["count"])
    document.add_heading(article["title"])
    for para in article["para"]:
        p = document.add_paragraph()
        pos = 0
        for mark in para["marked"]:
            p.add_run(para["text"][pos : mark.start(0)])
            p.add_run(para["text"][max(mark.start(0), pos) : mark.end(0)]).bold = True
            pos = mark.end(0)
        p.add_run(para["text"][pos:])
    document.add_paragraph(f'count: {article["count"]}')
    document.add_page_break()

document.save('output.docx')
