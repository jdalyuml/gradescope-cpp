import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, tags, partial_credit

Timeout = 60 # Seconds

def clean(regex:str):
    regex.replace('(love|dislike)', 'love')
    regex.replace('\\', '')
    return regex

class TestRead(unittest.TestCase):
    def trial(self, regex):
        import os, subprocess, re, difflib
        if not os.path.isfile('program'):
            self.fail('Program did not compile')
        
        process = subprocess.run(['./program'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=Timeout)
        msg = process.stdout.strip()
        err = f'Found: {msg}\nLooking for: {clean(regex)}'
        self.assertTrue(re.search(regex, msg), msg=err)

    @number('1.0')
    @weight(1)
    def test_hello(self):
        '''Checks for the text "Hello, world!"'''
        self.trial('Hello, world!')

    @number('1.1')
    @weight(2)
    def test_default(self):
        '''Checks for your secret world'''
        import json, random
        with open('/autograder/submission_metadata.json', 'r') as metain:
            meta = json.load(metain)
        with open('dictionary.txt') as dictionary:
            words = [w.strip() for w in dictionary if len(w.strip()) == 6]
        username = meta['users'][0]['name']
        rng = random.Random(username)
        word = rng.choice(words)
        self.trial(word)
