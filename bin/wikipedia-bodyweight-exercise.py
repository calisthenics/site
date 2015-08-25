#!/usr/bin/env python
# coding: utf-8
import os
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
    'bams': 'bam',
    'bodybuilders': 'bodybuilder',
    'boots': 'boot',
    'chairs': 'chair',
    'climbers': 'climber',
    'crosses': 'cross',
    'curls': 'curl',
    'darlings': 'darling',
    'dips': 'dip',
    'dogs': 'dog',
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
    'rotations': 'rotation',
    'scissors': 'scissor',
    'spidermans': 'spiderman',
    'supermans': 'superman',
    'swimmers': 'swimmer',
    'squats': 'squat',
    'ups': 'up'
}


def canonical_name(name):
    name = name.strip().lower()
    if name.startswith('full body'):
        return ''

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
for group in groups:
    group_name = group.find('a').find(class_='toctext').text.strip()
    for item in group.find('ul').find_all('a'):
        href = item.attrs['href']
        heading = soup.find(id=href.lstrip('#')).parent
        name = canonical_name(item.find(class_='toctext').text)
        groups = [canonical_name(group_name)]
        body = []
        variants = []
        muscles = []

        for sibling in heading.find_next_siblings():
            if sibling.name == 'p':
                body.append(clean_text(sibling.text))
            elif sibling.name == 'dl':
                dth = sibling.find('dt').text.strip().lower()
                if dth == 'common variants':
                    variants = list(filter(None, [canonical_name(i.text) for i in sibling.find_all('dd') if i.text != 'none']))
                elif dth == 'muscle groups':
                    muscles = list(filter(None, [canonical_name(i.text) for i in sibling.find_all('dd')]))
            elif sibling.name == 'h3':
                break

        doc = {
            'created': datetime.now(),
            'description': body[0].split('. ')[0] + '.',
            'groups': groups,
            'muscles': muscles,
            'template': 'exercise.html',
            'title': name,
            'variants': variants
        }
        # Files shall be saved as md files, so calling write_content directly
        # is not possible as it would save as html.
        filename = target_file(logya.dir_content, '/exercise/{}.md'.format(slugify(name)))
        if not os.path.exists(filename):
            write(filename, encode_content(doc, '\n\n'.join(body)))

        # Create stub files for variants
        for variant in variants:
            filename = target_file(logya.dir_content, '/exercise/{}.md'.format(slugify(variant)))
            if not os.path.exists(filename):
                ex_variants = set(variants).union(set([name])).difference(set([variant]))
                doc = {
                    'created': datetime.now(),
                    'description': '',
                    'groups': groups,
                    'muscles': muscles,
                    'template': 'exercise.html',
                    'title': variant,
                    'variants': ex_variants
                }
                write(filename, encode_content(doc, ''))


        # Create stub files for muscles
        for muscle in muscles:
            filename = target_file(logya.dir_content, '/muscle/{}.md'.format(slugify(muscle)))
            if not os.path.exists(filename):
                doc = {
                    'created': datetime.now(),
                    'description': '',
                    'template': 'muscle.html',
                    'title': muscle
                }
                write(filename, encode_content(doc, ''))