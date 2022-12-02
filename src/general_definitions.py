from datetime import date


def generate_access_date():
	today = date.today()

	day = str(today.day).zfill(2)
	month = [
		'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
		'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
	][today.month - 1]
	year = today.year

	return f'{day} de {month} de {year}'


HDI_YEAR = '2010'
hdi_reference_text = """\
<ref name="PNUD_IDH_2010">{{citar web |url=https://www.undp.org/pt/brazil/idhm-munic%C3%ADpios-2010 \
|titulo=IDHM Municípios 2010 |data=2013 |obra=[[Atlas do Desenvolvimento Humano do Brasil]] 2013 \
|publicado=[[Programa das Nações Unidas para o Desenvolvimento]] (PNUD) |acessodata=\
""" + generate_access_date() + '}}</ref>'
