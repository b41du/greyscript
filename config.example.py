# setup database
db_config = {
    'default': 'mysql',
    'mysql': {
        'driver': 'mysql',
        'host': 'localhost',
        'database': 'databasename',
        'user': 'username',
        'password': 'password',
        'prefix': ''
    }
}

# setup file keyword title
path_keyword_title_file = 'path/to/keyword/file.txt'
keyword_title_separator = '***'

# setup articles impacted
impacted_article_status = 2
custom_article_ids = []

# setup article after save
save_article_status = 1
