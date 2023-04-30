# This module is responsible for performing the editions.
# It must implement the function perform(), that creates and returns a SerialEdits instance

from edit import SerialEdits
import xlrd
from general_utils import make_reference, states, get_state_name_by_acronym
from infobox import RankableField
import csv

CURRENT_STATE_TARGET = 'RS'


def perform() -> SerialEdits:
    operation = SerialEdits()

    state = CURRENT_STATE_TARGET
    state_name = get_state_name_by_acronym(state)
    cities = make_cities_dict(state)

    standart_reference = make_reference(
        refname='IBGE-CIDADES-ESTADOS',
        link=f'https://www.ibge.gov.br/cidades-e-estados/{state.lower()}/',
        title='Cidades e Estados',
        publisher='IBGE',
        year=2021
    )

    igp_reference = make_reference(
        refname='PIB',
        link='https://sidra.ibge.gov.br/tabela/5938#resultado',
        title='Tabela 5938 - Produto interno bruto a preços correntes, impostos, líquidos de subsídios, sobre produtos a preços correntes e valor adicionado bruto a preços correntes total e por atividade econômica, e respectivas participações - Referência 2010',
        publisher='IBGE',
        year=2020
    )

    selected_cities = list(cities.items())[40:45]

    for city, data in selected_cities:
        edit = operation.new_edit(city, state_name)
        infobox = edit.get_infobox()
        infobox.edit_population(data['population'], 2021, reference=standart_reference)
        infobox.edit_area(data['area'], reference=standart_reference)
        infobox.edit_igp_per_capita(data['igp_per_capita'], 2020)
        infobox.edit_hdi(data['hdi'], 2010, reference=standart_reference)

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

        gini = data.get('gini')
        gini_rank_br = data.get('gini_rank_br')
        gini_rank_state = data.get('gini_rank_state')

        if gini:
            infobox.edit_gini(gini, 2010, reference=standart_reference)

        if gini_rank_br and gini_rank_state:
            infobox.edit_ranking_field(
                ranking=RankableField.GINI,
                pos_in_state=gini_rank_state,
                pos_in_country=gini_rank_br,
                state=state
            )

        edit.commit(infobox)

    return operation


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


def process_igp(state_acronym):
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


def make_cities_dict(state_acronym: str):
    general_sheet = xlrd.open_workbook(f'datafiles/info-{state_acronym.lower()}.xls').sheet_by_index(0)

    cities = {}
    row = 3
    while len(general_sheet.cell_value(row, 0)) >= 2:
        city_name = general_sheet.cell_value(row, 0)
        pop = int(general_sheet.cell_value(row, 5))
        hdi = general_sheet.cell_value(row, 8)
        cities[city_name] = {
            'population': pop,
            'area': general_sheet.cell_value(row, 4),
            'hdi': hdi,
            'igp_per_capita': general_sheet.cell_value(row, 12)
        }

        row += 1

    gini_obj = process_gini(state_acronym)
    igp_obj = process_igp(state_acronym)
    process_pop_and_hdi_rankings(cities)

    for city, entry in cities.items():
        try:
            entry.update(gini_obj[city])
            entry.update(igp_obj[city])
        except KeyError:
            continue

    return cities


def process_pop_and_hdi_rankings(cities: dict):
    all_br_pop = []
    all_br_hdi = []
    all_state_pop = []
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
                population = int(row[5])
                if row[8] != '-':  # city was founded before the last census
                    hdi = float(row[8].replace(',', '.'))

                all_br_pop.append(population)
                all_br_hdi.append(hdi)
                if state == CURRENT_STATE_TARGET:
                    all_state_pop.append(population)
                    all_state_hdi.append(hdi)

    all_br_pop.sort(reverse=True)
    all_br_hdi.sort(reverse=True)
    all_state_pop.sort(reverse=True)
    all_state_hdi.sort(reverse=True)

    with open(f'datafiles/info-{CURRENT_STATE_TARGET.lower()}.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for _ in range(3):
            next(reader)  # discard first 3 rows

        for row in reader:
            city_name = row[0]
            if not city_name:
                break  # no more cities

            population = int(row[5])
            hdi = float(row[8].replace(',', '.')) if row[8] != '-' else None

            cities[city_name]['population_rank_br'] = all_br_pop.index(population) + 1
            cities[city_name]['population_rank_state'] = all_state_pop.index(population) + 1
            if hdi:
                cities[city_name]['hdi_rank_br'] = all_br_hdi.index(hdi) + 1
                cities[city_name]['hdi_rank_state'] = all_state_hdi.index(hdi) + 1
