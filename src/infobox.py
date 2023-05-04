import pywikibot
from general_utils import format_as_currency
from enum import StrEnum

INFOBOX_FIELDS_IN_ORDER = ('nome', 'nome_oficial', 'preposição', 'foto', 'leg_foto', 'oculta bandeira', 'bandeira',
                           'oculta brasão', 'brasão', 'link_bandeira', 'link_brasão', 'oculta hino', 'link_hino',
                           'lema', 'apelido', 'gentílico', 'mapa', 'esconde_estado', 'posição', 'latP', 'latG', 'latM',
                           'latS', 'lonP', 'lonG', 'lonM', 'lonS', 'estado', 'região_intermediária', 'região_imediata',
                           'região_metropolitana', 'vizinhos', 'dist_capital', 'dist_capital_ref', 'capital_link',
                           'fundação', 'emancipação', 'aniversário', 'distritos', 'distritos_ref', 'prefeito',
                           'partido', 'mandato_início', 'vereadores', 'vereadores_ref', 'área', 'área_ref', 'área_pos',
                           'área_urbana', 'área_urbana_data', 'área_urbana_ref', 'população', 'data_pop', 'pop_data',
                           'população_data', 'população_ref', 'população_pos', 'densidade', 'clima', 'sigla_clima',
                           'clima_ref', 'altitude', 'altitude_ref', 'fuso', 'CEP', 'idh', 'idh_data', 'data_idh',
                           'idh_ref', 'idh_pos', 'gini', 'gini_data', 'data_gini', 'gini_ref', 'gini_pos', 'pib',
                           'pib_data', 'data_pib', 'pib_ref', 'pib_pos', 'pib_per_capita', 'pib_per_capita_data',
                           'data_pib_per_capita', 'padroeiro', 'site_prefeitura', 'site', 'site_câmara')

DEPRECATED_INFOBOX_FIELDS = 'mandato_fim', 'fim_mandato'


class RankableField(StrEnum):
    POPULATION = 'população_pos'
    HDI = 'idh_pos'
    GINI = 'gini_pos'
    IGP = 'pib_pos'


class Infobox:
    def __init__(self, article: pywikibot.Page):
        self.fields = {}
        template_with_args = None
        for template in article.templatesWithParams():
            if template[0].title() == 'Predefinição:Info/Município do Brasil':
                template_with_args = template
                break

        if not template_with_args:
            raise Exception('Could not find info template in given article.')

        args_string = template_with_args[1]
        for fieldstring in args_string:
            try:
                field, value = fieldstring.split('=', 1)
                self.fields[field] = value

            # unexpected field format
            except ValueError:
                continue

    def _set_field(self, field_name: str, field_value: str):
        self.fields[field_name] = field_value

    def edit_hdi(self, hdi, year, reference: str = None):
        # zpad in right side, for fixed 0.123 hdi format
        self._set_field('idh', str(hdi).replace(',', '.') + '0' * (5 - len(str(hdi))))
        self._set_field('data_idh', str(year))
        self._set_field('idh_ref', reference if reference else '')

    def edit_gini(self, gini: float, year, reference: str = None):
        self._set_field('gini', str(gini).replace(',', '.'))
        self._set_field('data_gini', str(year))
        self._set_field('gini_ref', reference if reference else '')

    def edit_population(self, population, year, reference: str = None):
        self._set_field('população', str(population))
        self._set_field('população_data', str(year))
        self._set_field('população_ref', reference if reference else '')

    def edit_ranking_field(self,
                           ranking: RankableField,
                           pos_in_state: int = None,
                           state: str = None,
                           state_complete_ranking_article_name: str = None,
                           pos_in_country: int = None,
                           country_complete_ranking_article_name: str = None):
        assert ranking and state and pos_in_state and pos_in_country

        field_value = ''
        if state_complete_ranking_article_name:
            field_value += f'[[{state_complete_ranking_article_name}|{state}: {pos_in_state}º]] '
        else:
            field_value += f'{state}: {pos_in_state}º '

        if country_complete_ranking_article_name:
            field_value += f'[[{country_complete_ranking_article_name}|BR: {pos_in_country}º]]'
        else:
            field_value += f'BR: {pos_in_country}º'

        self._set_field(ranking, field_value)

    def edit_area(self, area: float, reference: str = None):
        self._set_field('área', str(area))
        self._set_field('área_ref', reference if reference else '')

    def edit_igp(self, igp: float, year, reference: str = None):
        self._set_field('pib', format_as_currency(igp))
        self._set_field('pib_data', str(year))
        self._set_field('pib_ref', reference if reference else '')

    def edit_igp_per_capita(self, igp_per_capita: float, year):
        self._set_field('pib_per_capita', format_as_currency(igp_per_capita))
        self._set_field('pib_per_capita_data', year)

    def generate_raw(self):
        params = sorted(self.fields.items(), key=infobox_field_sorting_function)

        raw = '{{Info/Município do Brasil\n'
        for field, value in params:
            if field in DEPRECATED_INFOBOX_FIELDS:
                continue
            raw += f'| {field} = {value}\n'

        raw += '}}'
        return raw


def infobox_field_sorting_function(field_value_pair: tuple):
    field = field_value_pair[0]
    try:
        return INFOBOX_FIELDS_IN_ORDER.index(field)
    except ValueError:  # found a field that is not in the list. This could be an invalid field or a new one.
        return len(INFOBOX_FIELDS_IN_ORDER)
