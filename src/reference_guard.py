"""When a field is going to be replaced, so must be its reference. In some cases, the reference to be replaced
was being used in another part of the article, so this module contains utilities to make sure that the bot will
not leave broken references when editing."""

from typing import Optional


def extract_refname(text: str) -> Optional[str]:
    """Takes the reference text and attempts to discover its name and returns it, or None if no name."""
    closing_tag_index = text.find('>')
    if closing_tag_index == -1:
        raise ReferenceReallocationError

    name_arg_index = text.find('name=')
    if name_arg_index == -1:
        spaced_named_arg_index = text.find('name =')
        if spaced_named_arg_index == -1:
            return None
        else:
            name_arg_index = spaced_named_arg_index + len('name =')
    else:
        name_arg_index += len('name=')

    if name_arg_index > closing_tag_index:
        return None

    between_quotes = False
    refname = ''
    while True:
        if text[name_arg_index] == '>':
            break
        if not between_quotes and text[name_arg_index] in (' ', '/'):
            break
        if text[name_arg_index] in ('"', "'"):
            between_quotes = not between_quotes
        if text[name_arg_index] not in (' ', '"', "'", '>'):
            refname += text[name_arg_index]
        name_arg_index += 1

    return refname


def extract_body(text: str):
    """Returns the body string of the reference, if there is one."""
    if '{{' not in text:
        return None
    body_start_index = text.find('>') + 1
    body_end_index = text[body_start_index:].find('</')
    if body_end_index == 0 or body_end_index == -1:
        raise ReferenceReallocationError
    body_end_index += body_start_index

    return text[body_start_index:body_end_index]


def inject_body_in_reuse_reference(text: str, refname: str, body: str):
    index = text.index(refname) + len(refname)
    while index < len(text):
        if text[index:index + 2] == '/>':
            return text[:index] + '>' + body + '</ref>'
        if text[index] == '>':
            return text[:index + 1] + body + text[index + 1:]
        index += 1

    else:
        raise ReferenceReallocationError


# def find_next_usage(article_raw: str, refname: str):
#     first_usage_index = article_raw.index(refname) + len(refname)
#     text = article_raw[first_usage_index:]
#
#     next_usage_start_index = -1
#     next_usage_end_index = -1
#
#     while True:
#         usage_candidate_index = text.find(refname)
#         if usage_candidate_index == -1:
#             return None
#         look_backwards_index = usage_candidate_index
#         while look_backwards_index + 10 > usage_candidate_index:
#             look_backwards_index -= 1
#             if text[look_backwards_index - 2:look_backwards_index + 1] == 'ref':
#                 look_backwards_index -= 2
#                 while text[look_backwards_index] != '<':
#                     look_backwards_index -= 1
#                 next_usage_start_index = first_usage_index + look_backwards_index
#                 break
#
#         else:
#             continue


class ReferenceReallocationError(Exception):
    ...


if __name__ == '__main__':
    ref1 = """<ref name=":0">{{citar web|url=https://atarde.uol.com.br/bahia/noticias/1631647-obra-da-ponte-para-itaparica-comeca-em-agosto-de-2015|titulo=Obra da ponte para Itaparica começa em agosto de 2015|data=|acessodata=20/06/2020|publicado=|ultimo=|primeiro=}}</ref> mas os estudos demoraram a ser concluídos, o impacto ambiental foi mais de uma vez questionado por acadêmicos"""
    ref2 = """<ref name="Não_nomeado-yLuX-1">{{Citar web |url=https://www.ebiografia.com/william_harvey/ |titulo=Biografia de William Harvey |acessodata=2020-08-30 |website=eBiografia |lingua=pt-br}}</ref>"""
    ref3 = """<ref name=dodd40>{{harvnb|Dodd|1909|p=40}}</ref>"""
    ref4 = """<ref name="curran108" />"""
    ref5 = """<ref>{{Citar web|url=http://www.chapelpoint.org/historyPastors.asp|titulo=Pastors of St. Ignatius Church|website=St. Ignatius Catholic Church, Chapel Point|wayb=20110725154706|urlmorta=sim}}</ref>"""

    print(extract_refname(ref1))
    print(extract_refname(ref2))
    print(extract_refname(ref3))
    print(extract_refname(ref4))
    print(extract_refname(ref5))

    print(extract_body(ref1))
    print(extract_body(ref2))
    print(extract_body(ref3))
    print(extract_body(ref4))
    print(extract_body(ref5))

    print(inject_body_in_reuse_reference(text=ref4, body=extract_body(ref5), refname=extract_refname(ref4)))
