from bs4 import BeautifulSoup
import re

import validators

import constants
#from bs4.element import Comment


def get_html(webpage):
    soup = BeautifulSoup(webpage, 'html.parser')

    # kill all script and style elements
    for script in soup(['script', 'style', 'meta', '[document]']):
        script.extract()  # rip it out

    # get html tag contents
    html = soup.find('html')

    #remove all links
    for a in soup.findAll():
        del a['href']

    #return base64 bytecode of html page
    #b64code = base64.b64encode(bytes(str(html), 'utf-8'))
    return html
    #b64decoded = str(base64.b64decode(b64code), 'utf-8')


def link_cleaner(link):
    #strip the url for spaces
    clean_link = link.strip()

    #to avoid '/' or '?' at the end creating duplicate entries in db
    if clean_link[-1:] in ['/', '?']:
        clean_link = clean_link[:-1]
    return clean_link


def validate_link(link):
    if validators.url(link) == True:
        return True
    else:
        return False