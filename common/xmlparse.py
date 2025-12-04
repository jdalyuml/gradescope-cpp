#!/usr/bin/python

from datetime import datetime, timedelta
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
    if 'output' not in py:
        py['output'] = ''

    # Load C++ test results
    try:
        with open('/autograder/results/cpptests.json', 'r') as fin:
            for line in fin:
                cpp = json.loads(line)
                #print(cpp['name'])
                #print(cpp)
                py['tests'].append(cpp)

    except:
        print('C++ Autograder test results cannot be opened')
        py['output'] += '\n<font color="red">C++ Autograder test results cannot be opened</font>; there may have been problems compiling the unit tests.\n'
    
    # Set's the minimum score to zero in case they have penalties in excess of points earned
    py['score'] = max(sum(float(test['score']) for test in py['tests']), 0)
    

    try:
        with open('/autograder/submission_metadata.json', 'r') as metain:
            meta = json.load(metain)
        # 2023-06-13T21:00:00.000000-07:00
        TimeFormat = '%Y-%m-%dT%H:%M:%S.%f%z'
            
        # These are the important grading settings to change
        PenaltyPerDay = 0.1 # Percentage lost per day
        Semigrace = 0.05 # Reduce late penalty if they had a prior on-time submission
        MaxPenalty = 0.5 # Maximum percent that can be lost for late penalty 
        Leeway = timedelta(minutes = 10) # Allowance for submitting at the deadline window
        Grace = timedelta(days = 1) # Don't penalize them if they realize and fix something the morning after

        subdate = datetime.strptime(meta['created_at'], TimeFormat)
        duedate = datetime.strptime(meta['assignment']['due_date'], TimeFormat)
        hasOntime = any(datetime.strptime(sub['submission_time'], TimeFormat) < duedate + Leeway for sub in meta['previous_submissions'])
        truedelta = subdate - duedate
        delta = truedelta - Leeway
        if delta < Leeway:
            py['output'] += 'On time'
        elif delta < Grace and hasOntime:
            # Grace submission
            py['output'] += 'Grace be upon you'
        else:
            # late submission
            if delta.seconds > 0:
                days = delta.days + 1
            else:
                days = delta.days
            penalty = days * PenaltyPerDay
            if hasOntime:
                penalty -= Semigrace
            penalty = 1 - min(penalty, MaxPenalty)
            oldscore = py['score']
            newscore = oldscore * penalty
            pdelta = timedelta(days = truedelta.days, seconds = truedelta.seconds) # Don't print obscene detail, seconds is enough
            py['output'] += f'<font color="red">Late by {pdelta}</font>'
            py['output'] += f'\nAutograder score reduced {100 * (1 - penalty)}% to {100 * penalty}%: {oldscore} -> {newscore}'
            py['score'] = newscore
            #py['output'] += f'\nPenalty: {penalty}%'
    except Exception as ex:
        py['output'] += '<font color="red">Problem opening metadata</font>\n'
        py['output'] += str(ex)
    
    with open('/autograder/results/results.json', 'w') as fout:
        # fout.write(suite.toJSON())
        json.dump(py, fout, indent=2)


if __name__ == '__main__':
    Main()

