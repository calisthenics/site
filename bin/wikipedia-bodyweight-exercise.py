#!/usr/bin/env python
# coding: utf-8
import re
import requests

from datetime import datetime
from bs4 import BeautifulSoup
from logya.core import Logya
from logya.path import slugify, target_file
from logya.writer import encode_content, write


logya = Logya()
logya.init_env()

url = 'https://en.wikipedia.org/wiki/Bodyweight_exercise'
html = requests.get(url).text
soup = BeautifulSoup(html, 'lxml')

replacements = {
    'bodybuilders': 'bodybuilder',
    'boots': 'boot',
    'chairs': 'chair',
    'climbers': 'climber',
    'crosses': 'cross',
    'curls': 'curl',
    'darlings': 'darling',
    'dips': 'dip',
    'extensions': 'extension',
    'humpers': 'humper',
    'ins': 'in',
    'kicks': 'kick',
    'knives': 'knife',
    'lifts': 'lift',
    'little piggies': '3 little pigs',
    'lunges': 'lunge',
    'maybes': 'maybe',
    'mikes': 'mike',
    'mornings': 'morning',
    'offs': 'off',
    'plunges': 'plunge',
    'push exercises': 'push',
    'raises': 'raise',
    'scissors': 'scissor',
    'spidermans': 'spiderman',
    'supermans': 'superman',
    'swimmers': 'swimmer',
    'squats': 'squat',
    'ups': 'up'
}


def canonical_name(name):
    name = name.replace('[explain]', '').strip().lower()
    for source, target in replacements.items():
        name = re.sub(r'\b{}\b'.format(source), target, name)
    return name.title()


def clean_text(text):
    return text.replace('[citation needed]', '').strip()


# Only interested in TOC numbers 4 to 8.
tocnumbers = range(4, 9)

toc1_items = soup.find(id='toc').find_all(class_='toclevel-1')
groups = [i for i in toc1_items if int(i.find('a').find(class_='tocnumber').text) in tocnumbers]

assert len(groups) == len(tocnumbers)

# Assemble exercise documents
count_docs = 0
for group in groups:
    group_name = group.find('a').find(class_='toctext').text.strip()
    for item in group.find('ul').find_all('a'):
        href = item.attrs['href']
        heading = soup.find(id=href.lstrip('#')).parent
        name = canonical_name(item.find(class_='toctext').text)
        body = []
        variants = []
        muscles = []

        for sibling in heading.find_next_siblings():
            if sibling.name == 'p':
                body.append(clean_text(sibling.text))
            elif sibling.name == 'dl':
                dth = sibling.find('dt').text.strip().lower()
                if dth == 'common variants':
                    variants = [canonical_name(i.text) for i in sibling.find_all('dd') if i.text != 'none']
                elif dth == 'muscle groups':
                    muscles = [canonical_name(i.text) for i in sibling.find_all('dd')]
            elif sibling.name == 'h3':
                break

        doc = {
            'created': datetime.now(),
            'description': body[0].split('. ')[0] + '.',
            'groups': [canonical_name(group_name)],
            'muscles': muscles,
            'template': 'exercise.html',
            'title': name,
            'variants': variants
        }
        # Files shall be saved as md files, so calling write_content directly
        # is not possible as it would save as html.
        filename = '/exercise/{}.md'.format(slugify(name))
        write(
            target_file(logya.dir_content, filename),
            encode_content(doc, '\n\n'.join(body)))

        count_docs += 1

assert count_docs > 60

