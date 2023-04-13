from bs4 import BeautifulSoup
import phpserialize

def generate_html_planted(html_content, keyword):
    content = BeautifulSoup(html_content, 'html.parser')
    for index, ptag in enumerate(content.find_all('p')):
        if index == 0:
            ptag.string = '{} {}'.format(keyword, ptag.text)

        length_p =  len(ptag.text)

        if length_p > 100:
            ptag.string = '{} {}'.format(ptag.text, keyword)

    return str(content)


def generate_meta(meta_string, keyword):
    if meta_string:
        deserialized = phpserialize.loads(meta_string.encode('utf-8'))
        deserialized['keywords'] = keyword

    else:
        deserialized = {
            'keywords': keyword
        }

    serialized = phpserialize.dumps(deserialized)

    return serialized.decode('utf-8')
