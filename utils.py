import re
import pymorphy2

morph = pymorphy2.MorphAnalyzer()

def camel_case_split(str):
    words = [[str[0]]]

    for c in str[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return [''.join(word) for word in words]

def split_camel_case(tokens):
    splited = []
    added = []

    for token in tokens:
        words = camel_case_split(token)
        if len(words) > 0:
            splited.append(token)
            added.extend(words)

    tokens -= set(splited)
    tokens |= set(added)
    return tokens

def to_normal_form(word):
    p = morph.parse(word)[0]
    if p.normalized.is_known:
        normal_form = p.normal_form
    else:
        normal_form = word.lower()
    return normal_form

def is_cyrillic(text):
    return bool(re.fullmatch('[а-яА-ЯёЁ]+', text))

def is_english(text):
    return bool(re.fullmatch('[a-zA-Z]+', text))