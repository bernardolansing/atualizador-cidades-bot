# This module is responsible for performing the editions.
# It must implement the function perform(), that creates and returns a SerialEdits instance
from edit import SerialEdits

import xlrd
from general_utils import generate_access_date


# def perform():
#     operation = SerialEdits()
#
#     sheet = xlrd.open_workbook('datafiles/data.xls').sheet_by_index(0)
#
#     hdi_reference_text = """\
#     <ref name="PNUD_IDH_2010">{{citar web |url=https://www.undp.org/pt/brazil/idhm-munic%C3%ADpios-2010 \
#     |titulo=IDHM Municípios 2010 |ano=2013 \
#     |publicado=[[Programa das Nações Unidas para o Desenvolvimento]] (PNUD)}}</ref>"""
#
#     for row in range(2, 4):
#         city_name = sheet.cell_value(row, 0)[:-5]
#         state_acronym = sheet.cell_value(row, 0)[-3:-1]
#         gini = str(sheet.cell_value(row, 1))
#         hdi = str(sheet.cell_value(row, 2))
#
#         edit = operation.new_edit(city_name, state_acronym)
#         try:
#             infobox = edit.get_infobox()
#             infobox.edit_hdi(hdi, 2010, hdi_reference_text)
#             infobox.edit_gini(gini, 2010)
#         except:
#             edit.report_failure()
#         else:
#             edit.commit(infobox)
#
#     return operation

def perform() -> SerialEdits:
    operation = SerialEdits()

    sheet = xlrd.open_workbook('datafiles/pib.xls').sheet_by_index(0)

    reference = """<ref>{{Citar web|url=https://www.ibge.gov.br/estatisticas/economicas/contas-nacionais/9088-produto-interno-bruto-dos-municipios.html?=&t=resultados|titulo=Produto Interno Bruto dos Municípios|publicado=[[Instituto Brasileiro de Geografia e Estatística|IBGE]]|ano=2020}}</ref>"""

    for i in range(55690, 55692):
        nome = sheet.cell_value(i, 7)
        state = sheet.cell_value(i, 5)
        pib = sheet.cell_value(i, 38) * 1000
        pib_per_capita = sheet.cell_value(i, 39)
        edit = operation.new_edit(nome, state)
        infobox = edit.get_infobox()
        infobox.edit_igp(pib, year=2020, reference=reference)
        infobox.edit_igp_per_capita(pib_per_capita, year=2020)

        edit.commit(infobox)

    return operation
