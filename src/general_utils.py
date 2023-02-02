from datetime import date
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

states = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espírito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MT': 'Mato Grosso',
    'MS': 'Mato Grosso do Sul',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}


def get_state_name_by_acronym(acronym: str):
    return states[acronym]


def get_state_acronym_by_name(name: str):
    keys = list(states.keys())
    return keys.index(name)


def generate_access_date():
    today = date.today()

    day = str(today.day).zfill(2)
    month = [
        'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho',
        'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'
    ][today.month - 1]
    year = today.year

    return f'{day} de {month} de {year}'


def format_as_currency(n: float):
    return locale.currency(n, grouping=True, symbol=False)


def make_reference(refname: str, link: str, title: str, publisher: str, year):
    """Creates and returns a full reference and another ref that links for it. Use the full reference
    only once, and then its link every other time."""
    ref = '<ref name="' + refname + '">{{Citar web'
    ref += ' |url=' + link
    ref += ' |titulo=' + title
    ref += ' |publicado=' + publisher
    ref += ' |ano=' + str(year)
    ref += '}}</ref>'

    ref_tag = f'<ref name="{refname}" />'

    return ref, ref_tag
