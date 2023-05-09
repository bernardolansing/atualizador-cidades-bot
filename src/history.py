from datetime import datetime
from general_utils import generate_access_date

AMOUNT_OF_DIGITS_FOR_HISTORY_ENTRY_ID = 5

with open('history.txt', 'r') as file:
    current_history = file.read()


def new_history_entry(amount_ordered: int, amount_done: int, operator_name: str, reference_summary: str,
                      public_summary: str):

    entry_id = get_new_id()
    now = datetime.now()
    timezone = 'GMT ' + datetime.now().astimezone().tzinfo.tzname(datetime.now().astimezone())
    time_annotation = generate_access_date() + f' {now.hour}:{now.minute} ({timezone})'
    percent_done = to_percentage(amount_done / amount_ordered)
    percent_failed = to_percentage((amount_ordered - amount_done) / amount_ordered)

    text = f'[{entry_id}] @ {time_annotation}\n' \
           + f'Edições encomendadas: {amount_ordered}\n' \
           + f'Edições concluídas: {amount_done} ({percent_done})\n' \
           + f'Edições fracassadas: {amount_ordered - amount_done} ({percent_failed})\n' \
           + f'Comentário interno: {reference_summary}\n' \
           + f'Descrição pública da edição: {public_summary}\n' \
           + f'Operador: {operator_name}\n'

    insert_into_file_and_write(text)


def to_percentage(f: float):
    f *= 100
    return f'{f:.0f}%'


def get_new_id():
    start_index = current_history.find('[') + 1
    end_index = current_history.find(']')

    # no logs in history
    if start_index == 0:
        return '00001'

    num_index = int(current_history[start_index:end_index])
    new_index = str(num_index + 1).zfill(AMOUNT_OF_DIGITS_FOR_HISTORY_ENTRY_ID)
    return new_index


def insert_into_file_and_write(new_entry_text: str):
    # end of header is marked with 120 traces in a row
    end_of_header_index = current_history.find(120 * '-') + 120

    header_slice = current_history[:end_of_header_index + 1]
    previous_entries_slice = current_history[end_of_header_index + 1:]
    entire_text = header_slice + new_entry_text + '\n' + previous_entries_slice

    with open('history.txt', 'wt') as file:
        file.write(entire_text)
