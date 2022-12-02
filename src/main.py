from general_definitions import HDI_YEAR, hdi_reference_text
from infobox import Infobox
from city_finder import find_city_article
from city_editor import produce_new_raw


def edit_hdi(infobox: Infobox, hdi: str):
	infobox.set_field('idh', hdi)
	infobox.set_field('data_idh', HDI_YEAR)
	infobox.set_field('idh_ref', hdi_reference_text)


# def main():
# 	for state in states_names:
# 		for city in cities_names:
# 			try:
# 				article = find_city_article(city, state)
# 			except Exception():
# 				print(f'Failed to locate city: {city} - {state}')
# 				continue
#
# 			infobox = Infobox(article)
# 			# edit_hdi(infobox, )


article = find_city_article('Melgaço', 'Pará')
infobox = Infobox(article)
edit_hdi(infobox, '0.418')
article.text = produce_new_raw(article.text, infobox.generate_raw())
article.save('Atualizado IDHM.')
