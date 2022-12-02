import pywikibot
from general_definitions import HDI_YEAR


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

		for fieldstring in template_with_args[1]:
			field, value = fieldstring.split('=', 1)
			self.fields[field] = value

	def set_field(self, field_name: str, field_value: str):
		self.fields[field_name] = field_value

	def generate_raw(self):
		raw = '{{Info/Município do Brasil\n'
		for field, value in self.fields.items():
			raw += '| ' + field + ' ' * (24 - len(field)) + ' = ' + value + '\n'

		raw += '}}'
		return raw

	def hdi_is_correct(self):
		return \
			self.fields['idh'] and \
			self.fields['idh_ref'] and \
			(self.fields['data-idh'].strip().isNumeric() and self.fields['data-idh'].strip() == HDI_YEAR)
