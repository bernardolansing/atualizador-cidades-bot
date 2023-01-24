from page_utils import find_city_article, produce_new_raw
from general_utils import get_state_name_by_acronym
from history import new_history_entry
from infobox import Infobox
from pywikibot import Page


class Edit:
    def __init__(self, article: Page, edit_id: int, city_name: str, state_acronym: str, summary: str):
        self.success = None
        self.id = edit_id
        self.article = article
        self.edit_title = f'[{edit_id}] {city_name} - {state_acronym} ({article.full_url()})'
        self.summary = summary

    def get_infobox(self):
        return Infobox(self.article)

    def commit(self, new_infobox: Infobox):
        new_source = produce_new_raw(self.article.text, new_infobox.generate_raw())
        self.article.text = new_source
        try:
            self.article.save(summary=self.summary)
        except:
            self.report_failure()
            return

        print('Success at', self.edit_title)
        self.success = True

    def report_failure(self):
        print('Failure at', self.edit_title)
        self.success = False


class SerialEdits:
    def __init__(self):
        self.current_id = 1
        self.edits = []

        while True:
            operator = input('Please, identify yourself as a operator. ')
            reference_summary = input('Provide a brief summary for internal reference. ')
            public_summary = input('Write the edit summary (it will appear at each article history). ')

            print('You are', operator)
            print('Description of this execution:', reference_summary)
            print('Each edit will be recorded with the message:', public_summary)
            print('Do you confirm this information and do you want to proceed with the execution?')
            answer = input('[y] to confirm, any other input to repeat the questions. ')
            if answer.lower() == 'y':
                break

        self.operator = operator
        self.reference_summary = reference_summary
        self.public_summary = public_summary

    def new_edit(self, city_name: str, state: str):
        state_name = get_state_name_by_acronym(state) if len(state) == 2 else state
        page = find_city_article(city_name, state_name)
        new_edit = Edit(page, self.current_id, city_name, state_name, self.public_summary)
        self.edits.append(new_edit)
        self.current_id += 1
        return new_edit

    def finish(self):
        while True:
            answer = input('Do you wish to report a success rate? [y] / [n] ')
            if answer.lower() == 'y':
                reported_success_count = int(input('How many pages were successfully edited? '))
                break
            else:
                reported_success_count = None
                break

        done_count = 0
        for edit in self.edits:
            if edit.success:
                done_count += 1

        new_history_entry(
            amount_ordered=self.current_id - 1,
            amount_done=done_count,
            operator_name=self.operator,
            reference_summary=self.reference_summary,
            public_summary=self.public_summary,
            reported_sucess=reported_success_count
        )
