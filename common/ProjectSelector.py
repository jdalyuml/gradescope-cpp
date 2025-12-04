#!/usr/bin/python3

import configparser
import json
import os
import re

cfg = configparser.ConfigParser()
cfg.read('Projects.cfg')
projects = cfg['Projects']
settings = cfg['Settings']

projre = r'(hw\s*\d+)'
shortener = r'(hw)\s*(\d+)'

with open('/autograder/submission_metadata.json', 'r') as fin:
    meta = json.load(fin)

title = meta['assignment']['title']
pnum = title.split(':')[0].lower()

if 'hwx' in pnum:
    if not os.path.exists('/autograder/submission/changes.txt'):
        print('Could not find changelog file: changes.txt')
        exit(1)
    with open('/autograder/submission/changes.txt') as changelog:
        data = changelog.read().lower()
        results = re.search(projre, data)
        if not results:
            print('Could not find assignment number in changelog')
            exit(1)
        pnum = results.group(1)
        print(f'Selected assignment: {pnum}')
    

pname = projects[pnum]
separateTests = settings.getboolean('SeparateTestsAndImp')
isTests = 'test' in title.lower()

hasTests = not separateTests or isTests
hasImp = not separateTests or not isTests

with open('/autograder/files.cfg', 'w') as fout:
    fout.write(f'PROJ_NAME={pname}\n')
    fout.write(f'PROJ_NUM={pnum}\n')
    fout.write(f'TESTS={hasTests}\n')
    fout.write(f'IMP={hasImp}\n')

