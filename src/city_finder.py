import pywikibot
from json import loads

site = pywikibot.Site('pt')


with open('datafiles/estados-cidades.json', 'r') as locations:
	cities_json = loads(locations.read())

cities_names = [state['cidades'] for state in cities_json['estados']]
states_names = [state['nome'] for state in cities_json['estados']]


def find_city_article(city: str, state: str):
	supposed_page = pywikibot.Page(site, city)

	if is_disambiguation(supposed_page) or not is_city_article(supposed_page):
		supposed_page = pywikibot.Page(site, city + f' ({state})')

	if not is_city_article(supposed_page):
		raise Exception(f'Failed to find city: {city}, state: {state}')

	return supposed_page


# returns article text without spaces
def unformat_article_text(article: pywikibot.Page):
	return article.text.replace(' ', '')


def is_disambiguation(article: pywikibot.Page):
	return '{{Desambiguação|' in unformat_article_text(article)


def is_city_article(article: pywikibot.Page):
	return '{{Info/MunicípiodoBrasil' in unformat_article_text(article)
