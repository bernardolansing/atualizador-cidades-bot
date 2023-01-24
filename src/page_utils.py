import pywikibot

site = pywikibot.Site('pt')


def produce_new_raw(old_page_raw: str, infobox_raw: str):
	start_index = old_page_raw.index('{{Info/Município do Brasil')

	opened_brackets = 1
	last_char = ''
	final_index = start_index + 2
	while True:
		if old_page_raw[final_index] == last_char == '{':
			opened_brackets += 1

		elif old_page_raw[final_index] == last_char == '}':
			opened_brackets -= 1

		if not opened_brackets:
			break

		final_index += 1
		last_char = old_page_raw[final_index]

	return old_page_raw[:start_index] + infobox_raw + old_page_raw[final_index + 2:]


def find_city_article(city: str, state: str):
	supposed_page = pywikibot.Page(site, city)

	if is_disambiguation(supposed_page) or not is_city_article(supposed_page):
		supposed_page = pywikibot.Page(site, city + f' ({state})')

	if not is_city_article(supposed_page):
		raise Exception(f'Failed to find city: {city}, state: {state}')

	return supposed_page


def unformat_article_text(article: pywikibot.Page):
	return article.text.replace(' ', '')


def is_disambiguation(article: pywikibot.Page):
	return '{{Desambiguação|' in unformat_article_text(article)


def is_city_article(article: pywikibot.Page):
	return '{{Info/MunicípiodoBrasil' in unformat_article_text(article)
