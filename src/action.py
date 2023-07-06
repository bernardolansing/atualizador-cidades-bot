"""
This module is responsible for performing the editions.
It must implement the function perform(), that creates and returns a SerialEdits instance.

Every time that the bot needs to perform a mass edit, this is the file to be changed. The other
files are the library, and should only be edited only to improve or adequate to yet unpredicted
phenomena.

Always run this code in debug mode (DEBUG_MODE=1 in .env file) before performing an actual
edit in Wikipedia pages. Debug mode copies the new article source to the clipboard, so you
can easily swap it with the current source when viewing in the browser.
"""

import xlrd
import csv
import unicodedata
import re
from edit import SerialEdits
from general_utils import make_reference, states, get_state_name_by_acronym
from infobox import RankableField

CURRENT_STATE_TARGET = 'RS'


def perform() -> SerialEdits:
    operation = SerialEdits()

    state = CURRENT_STATE_TARGET
    state_name = get_state_name_by_acronym(state)
    cities = make_cities_dict(state)

    population_reference = make_reference(refname='ATT_BOT_POP_0522', publisher='IBGE', year=2021,
                                          title='ESTIMATIVAS DA POPULAÇÃO RESIDENTE NO BRASIL E UNIDADES DA FEDERAÇÃO '
                                                'COM DATA DE REFERÊNCIA EM 1º DE JULHO DE 2021',
                                          link='https://ftp.ibge.gov.br/Estimativas_de_Populacao/Estimativas_2021/'
                                               'POP2021_20221212.pdf')
    igp_reference = make_reference(refname='ATT_BOT_PIB_0522', publisher='IBGE', year=2020,
                                   link='https://ftp.ibge.gov.br/Pib_Municipios/2020/base/base_de_dados_2010_2020_xls'
                                        '.zip', title='Produto Interno Bruto dos Municípios - 2010 a 2020')
    hdi_reference = make_reference(refname='ATT_BOT_IDH_0522', publisher='IBGE', year=2010, title='Ranking',
                                   link='http://www.atlasbrasil.org.br/ranking')

    selected_cities = list(cities.items())[363:364]

    for city, data in selected_cities:
        try:
            edit = operation.new_edit(city, state_name)
        except:
            print('error while creating edit object for', city)
            continue
        try:
            area_reference = make_reference(refname='ATT_BOT_AREA_0522',
                                            link=f'https://www.ibge.gov.br/cidades-e-estados/{state.lower()}/'
                                                 f'{city_name_to_ibge_link(city)}.html',
                                            title='Cidades e Estados', publisher='IBGE', year=2021)

            infobox = edit.get_infobox()
            infobox.edit_population(data['population'], 2021, reference=population_reference)
            infobox.edit_area(data['area'], reference=area_reference)
            infobox.edit_igp_per_capita(data['igp_per_capita'], 2020)
            infobox.edit_hdi(data['hdi'], 2010, reference=hdi_reference)

            pop_rank_br = data.get('population_rank_br')
            pop_rank_state = data.get('population_rank_state')
            infobox.edit_ranking_field(
                ranking=RankableField.POPULATION,
                pos_in_state=pop_rank_state,
                pos_in_country=pop_rank_br,
                state_complete_ranking_article_name='Lista de municípios do Rio Grande do Sul por população',
                country_complete_ranking_article_name='Lista de municípios do Brasil por população',
                state=state
            )

            hdi_rank_br = data.get('hdi_rank_br')
            hdi_rank_state = data.get('hdi_rank_state')
            if hdi_rank_state and hdi_rank_br:
                infobox.edit_ranking_field(
                    ranking=RankableField.HDI,
                    pos_in_state=hdi_rank_state,
                    pos_in_country=hdi_rank_br,
                    state_complete_ranking_article_name='Lista de municípios do Rio Grande do Sul por IDH-M',
                    country_complete_ranking_article_name='Lista de municípios do Brasil por IDH',
                    state=state
                )

            # some cities may not be included at igp and gini tables
            igp = data.get('igp')
            igp_rank_br = data.get('igp_rank_br')
            igp_rank_state = data.get('igp_rank_state')
            if igp:
                infobox.edit_igp(igp, 2020, reference=igp_reference)
            if igp_rank_state:
                infobox.edit_ranking_field(
                    ranking=RankableField.IGP,
                    pos_in_state=igp_rank_state,
                    pos_in_country=igp_rank_br,
                    state_complete_ranking_article_name='Lista de municípios do Rio Grande do Sul por PIB',
                    country_complete_ranking_article_name='Lista de municípios do Brasil por PIB',
                    state=state,
                )

            edit.commit(infobox)
        except:
            edit.report_failure()

    return operation


def city_name_to_ibge_link(city_name: str):
    link = city_name.lower().replace(' ', '-')
    return unicodedata.normalize('NFKD', link).encode('ASCII', 'ignore').decode('ASCII')  # remove accents and other
    # letter marks


def process_gini(state_acronym: str):
    sheet = xlrd.open_workbook('datafiles/gini-br.xls').sheet_by_index(0)
    obj = {}
    all_ginis = []
    state_ginis = []

    row = 2
    while len(sheet.cell_value(row, 0)) >= 2:
        city_name = sheet.cell_value(row, 0)[:-5]
        gini = sheet.cell_value(row, 1)
        if f'({state_acronym.upper()})' in sheet.cell_value(row, 0):
            obj[city_name] = {'gini': gini}
            state_ginis.append(gini)
        all_ginis.append(gini)
        row += 1

    all_ginis.sort()
    state_ginis.sort()

    for entry in obj.values():
        entry['gini_rank_br'] = all_ginis.index(entry['gini']) + 1
        entry['gini_rank_state'] = state_ginis.index(entry['gini']) + 1

    return obj


def process_igp(state_acronym: str):
    sheet = xlrd.open_workbook('datafiles/pib.xls').sheet_by_index(0)
    obj = {}
    all_igps = []
    state_igps = []

    row = 4
    while len(sheet.cell_value(row, 0)) >= 2:
        city_name = sheet.cell_value(row, 0)[:-5]
        igp = sheet.cell_value(row, 1) * 1000
        if f'({state_acronym.upper()})' in sheet.cell_value(row, 0):
            obj[city_name] = {'igp': igp}
            state_igps.append(igp)
        all_igps.append(igp)
        row += 1

    all_igps.sort(reverse=True)
    state_igps.sort(reverse=True)

    for entry in obj.values():
        entry['igp_rank_br'] = all_igps.index(entry['igp']) + 1
        entry['igp_rank_state'] = state_igps.index(entry['igp']) + 1

    return obj


def process_population(state_acronym: str):
    sheet = xlrd.open_workbook('datafiles/pop_cidades_2022_previa.xls').sheet_by_index(0)
    obj = {}
    all_populations = []
    state_populations = []

    row = 2
    while True:
        state = sheet.cell_value(row, 0)
        if not state:
            break
        city_name = sheet.cell_value(row, 3)
        try:
            population = int(sheet.cell_value(row, 4))
        except ValueError:
            population = int(re.sub(pattern='[^0-9]', repl='', string=sheet.cell_value(row, 4)))

        all_populations.append(population)
        if state == state_acronym:
            state_populations.append(population)
            obj[city_name] = {'population': population}

        row += 1

    all_populations.sort(reverse=True)
    state_populations.sort(reverse=True)

    for entry in obj.values():
        entry['population_rank_br'] = all_populations.index(entry['population']) + 1
        entry['population_rank_state'] = state_populations.index(entry['population']) + 1

    return obj


def make_cities_dict(state_acronym: str):
    general_sheet = xlrd.open_workbook(f'datafiles/info-{state_acronym.lower()}.xls').sheet_by_index(0)

    cities = {}
    row = 3
    while len(general_sheet.cell_value(row, 0)) >= 2:
        city_name = general_sheet.cell_value(row, 0)
        hdi = general_sheet.cell_value(row, 8)
        cities[city_name] = {
            'area': general_sheet.cell_value(row, 4),
            'hdi': hdi,
            'igp_per_capita': general_sheet.cell_value(row, 12)
        }

        row += 1

    gini_obj = process_gini(state_acronym)
    igp_obj = process_igp(state_acronym)
    population_obj = process_population(state_acronym)
    process_pop_and_hdi_rankings(cities)

    for city, entry in cities.items():
        try:
            entry.update(gini_obj[city])
            entry.update(igp_obj[city])
            entry.update(population_obj[city])
        except KeyError:
            continue

    return cities


def process_pop_and_hdi_rankings(cities: dict):
    all_br_hdi = []
    all_state_hdi = []

    for state in states.keys():
        with open(f'datafiles/info-{state.lower()}.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for i in range(3):
                next(reader)  # discard first three rows

            for row in reader:
                city_name = row[0]
                if not city_name:
                    break  # city rows end before a blank row
                hdi_available = row[8] != '-'  # city was founded before the last census
                if hdi_available:
                    hdi = float(row[8].replace(',', '.'))

                if hdi_available:
                    all_br_hdi.append(hdi)
                if state == CURRENT_STATE_TARGET:
                    if hdi_available:
                        all_state_hdi.append(hdi)

    all_br_hdi.sort(reverse=True)
    all_state_hdi.sort(reverse=True)

    with open(f'datafiles/info-{CURRENT_STATE_TARGET.lower()}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for _ in range(3):
            next(reader)  # discard first 3 rows

        for row in reader:
            city_name = row[0]
            if not city_name:
                break  # no more cities

            hdi = float(row[8].replace(',', '.')) if row[8] != '-' else None
            if hdi:
                cities[city_name]['hdi_rank_br'] = all_br_hdi.index(hdi) + 1
                cities[city_name]['hdi_rank_state'] = all_state_hdi.index(hdi) + 1
