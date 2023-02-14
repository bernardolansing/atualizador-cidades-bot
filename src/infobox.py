import pywikibot
from general_utils import format_as_currency


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
        self._set_field('idh', str(hdi).replace(',', '.'))
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

    def edit_igp(self, igp: float, year, reference: str = None):
        self._set_field('pib', format_as_currency(igp))
        self._set_field('pib_data', str(year))
        self._set_field('pib_ref', reference if reference else '')

    def edit_igp_per_capita(self, igp_per_capita: float, year):
        self._set_field('pib_per_capita', format_as_currency(igp_per_capita))
        self._set_field('pib_per_capita_data', year)

    def generate_raw(self):
        raw = '{{Info/Município do Brasil\n'
        for field, value in self.fields.items():
            raw += '| ' + field + ' = ' + str(value) + '\n'

        raw += '}}'
        return raw
