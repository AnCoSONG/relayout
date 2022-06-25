from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
import jieba
from yattag import Doc
import jieba.posseg as pseg
from fastapi.middleware.cors import CORSMiddleware
# jieba.enable_parallel(4)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
class Text(BaseModel):
    content: List[str]

def trim(s: str):
    # return s
    temp = s.strip()
    return temp.replace(' ', '')

def _analyze_json(text: Text):
    paragraphs = text.content
    trimmed_paragraphs = list(map(trim, paragraphs))
    ret = []
    for par_id, trimmed_paragraph in enumerate(trimmed_paragraphs):
        words = pseg.cut(trimmed_paragraph)
        ret.append([])
        for word, flag in words:
            ret[par_id].append({'word': word, 'flag': flag})
    
    return ret

def _analyze_html(text_: Text):
    paragraphs = text_.content
    trimmed_paragraphs = list(map(trim, paragraphs))
    doc, tag, text = Doc().tagtext()
    with tag('article'):
        for trimmed_paragraph in trimmed_paragraphs:
            with tag('p'):
                words = pseg.cut(trimmed_paragraph)
                for word, flag in words:
                    with tag('span', klass=f'jieba-{flag}'):
                        text(word)
    data = doc.getvalue()
    return data

@app.post('/api/analyze')
def analyze(html: bool, text: Text):
    if html:
        return _analyze_html(text)
    else:
        return _analyze_json(text)

    
