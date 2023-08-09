#!/usr/bin/python

import json
import xml.etree.ElementTree as ET

class TestResults:
    def __init__(self, name, maxScore, score=None, number = None, msg = ''):
        self.name = name
        self.max_score = maxScore
        if score is None:
            self.score = maxScore
        else:
            self.score = score
        self.number = number
        self.output = msg
    
    def __str__(self):
        return f"{self.name}: {self.score}/{self.maxScore}"
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

class TestSuite:
    def __init__(self, tests) -> None:
        self.tests = tests
    
    def toJSON(self):
        return json.dumps({"tests":[t.__dict__ for t in self.tests]}, indent=2)

def ParseTest(test):
    name = test.attrib['name']
    score = None
    maxScore = 0
    msg = ''
    number = ''
    for child in test:
        if child.tag == 'Message':
            parts = child.text.split(':')
            if parts[0] == 'Weight':
                maxScore = parts[1]
            elif parts[0] == 'Points':
                score = parts[1]
            elif parts[0] == 'Number':
                number = parts[1]
        elif 'Error' in child.tag:
            if score is None:
                score = 0
            msg = child.text
    return TestResults(name, maxScore, score = score, msg = msg, number = number)


def Main():

    # Load Python test results
    try:
        with open('/autograder/results/pytests.json', 'r') as fin:
            py = json.load(fin)
    except:
        py = {
            "output": '<font color="red">Python autograder tests failed</font>; your program might not have compiled.',
            "output_format": "simple_format",
            "test_output_format": "text",
            "test_name_format": "text",
            "visibility": "visible",
            "stdout_visibility": "visible",
            "extra_data": {},
            "tests": []
        }

    # Load C++ test results
    try:
        tree = ET.parse('results.xml')
        root = tree.getroot()
        tests = [ParseTest(test) for test in root.findall('TestSuite/TestCase')]
        suite = TestSuite(tests)
        encoded = suite.toJSON()
        cpp = json.loads(encoded)
        py['tests'].extend(cpp['tests'])
    except:
        py['output'] += '\n<font color="red">C++ Autograder test results cannot be opened</font>; there may have been problems compiling the unit tests.'
    
    # Set's the minimum score to zero in case they have penalties in excess of points earned
    py['score'] = max(sum(float(test['score']) for test in py['tests']), 0)
    
    
    with open('/autograder/results/results.json', 'w') as fout:
        # fout.write(suite.toJSON())
        json.dump(py, fout, indent=2)


if __name__ == '__main__':
    Main()

