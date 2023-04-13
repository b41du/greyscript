from config import (
    db_config,
    path_keyword_title_file,
    keyword_title_separator,
    impacted_article_status,
    custom_article_ids,
    save_article_status
)
from helper import generate_html_planted, generate_meta
from orator import DatabaseManager
from datetime import datetime
import sys

class Main:
    db = None
    articles_data = None
    grey_list = []
    db_config = None
    updated_article = {}
    
    def __init__(self):
        self.db_config = db_config
        self.txt_path = path_keyword_title_file

    def get_connect(self):
        if not self.db:
            self.db = DatabaseManager(self.db_config)
            return self.db
        return self.db

    def get_audit_data(self):
        self.articles_data = self.get_connect().table('zbp_post') \
            .where('log_Status', impacted_article_status) \
            .or_where('log_ID', 'in', custom_article_ids) \
            .get()

        if not self.articles_data:
            self.get_connect().close()
            print('No data article with status audit, system quit..')
            sys.exit()

    def read_and_delete_lines(self, file_path, num_lines):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        if num_lines <= len(lines):
            self.grey_list = lines[:num_lines]
        else:
            print('Add more keywords and tittle need {} lines... script stop..'.format(num_lines))
            self.get_connect().close()
            sys.exit()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines[num_lines:])

    def update_title_and_keyword(self, keyword, title, data):
        result = {}
        result['log_Title'] = '{} {}'.format(title, data['log_Title'])
        result['log_Content'] = generate_html_planted(data['log_Content'], keyword)
        result['log_Meta'] = generate_meta(data['log_Meta'], keyword)
        result['log_Status'] = save_article_status

        try:
            now = datetime.now()
            print(now.strftime("%A, %B %d, %Y %I:%M %p"))
            if self.get_connect().table('zbp_post').where('log_ID', data['log_ID']).update(result):
                print('data id :{}\ntitle {}\nkeyword {}\n\n'.format(data['log_ID'], result['log_Title'], keyword))

            else:
                print('Failed update data, data id {}'.format(data['log_ID']))

        except Exception as e:
            print("An error occurred:", e)

    def updating_article(self):
        self.get_audit_data()
        self.read_and_delete_lines(self.txt_path, self.articles_data.count())
        for idx, element in enumerate(self.grey_list):
            title, keyword = str(element).strip().split(keyword_title_separator)
            article_data = self.articles_data[idx]
            self.update_title_and_keyword(keyword, title, article_data)


if __name__ == '__main__':
    main = Main()
    main.updating_article()
