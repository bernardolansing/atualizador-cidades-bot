import pywikibot


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
