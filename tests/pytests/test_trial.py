#!/usr/bin/python3
import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, tags, partial_credit

from enum import Flag

class MatchMode(Flag):
    StartsWith = 1
    EndsWith = 2
    ExactMatch = StartsWith | EndsWith
    Regex = 4 # Currently not honored
    TrimWhitespace = 8
    SkipBlankLines = 16

def trimOutput(output:str, mode:MatchMode):
    def trim(line: str):
        if MatchMode.TrimWhitespace in mode:
            return line.strip()
        else:
            return line
    return [trim(line) for line in output.split('\n') if MatchMode.SkipBlankLines not in mode or line != '']

class TestTrial(unittest.TestCase):
    # Configuration Options
    ProgramName = './bracket' # Name of the student's compiled program

    def runTrial(self, args=None, *, input=None, inputFile=None, expOutput=None, solFile=None, mode=MatchMode.ExactMatch|MatchMode.TrimWhitespace, showInput=True):
        import subprocess
        # Invoke subprocess
        exec = [TestTrial.ProgramName]
        if args:
            exec.extend(args)
            # TODO
        if inputFile:
            with open(inputFile, 'r') as fin:
                process = subprocess.run(exec, stdin=fin, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        else:
            process = subprocess.run(exec, input=input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        # Get actual solution from subprocess
        errors = process.stderr
        actResults = trimOutput(process.stdout, mode)
        self.assertEqual(process.returncode, 0, msg=errors)

        # Get expected solution
        if solFile:
            with open(solFile, 'r') as fin:
                expResults = trimOutput(''.join(line for line in fin), mode)
        elif expOutput:
            expResults = expOutput.split('\n')
        else:
            return
        
        # Check answer
        if MatchMode.StartsWith in mode:
            if expResults[-1] == '':
                expResults = expResults[:-1]
            for i, (act, exp) in enumerate(zip(actResults, expResults)):
                if showInput and input:
                    self.assertEqual(exp, act, msg=f'For input "{input}", difference in output on line {i+1}.\nExpected: "{exp}"\nFound: "{act}"\n')
                else:
                    self.assertEqual(exp, act, msg=f'Difference in output on line {i+1}.\nExpected: "{exp}"\nFound: "{act}"\n')
        elif MatchMode.EndsWith in mode:
            n = len(expResults)
            for i, (act, exp) in enumerate(zip(actResults[-n:], expResults)):
                if showInput and input:
                    self.assertEqual(exp, act, msg=f'For input "{input}", difference in output on line {i+n+1}.\nExpected: "{exp}"\nFound: "{act}"\n')
                else:
                    self.assertEqual(exp, act, msg=f'Difference in output on line {i+n+1}.\nExpected: "{exp}"\nFound: "{act}"\n')
        if MatchMode.ExactMatch in mode:
            self.assertEqual(len(exp), len(act), msg=f"Wrong number of lines produced.\nExpected: {len(exp)}\nFound: {len(act)}")

    # Unit Tests

    @weight(2)
    @number('2.1')
    def test_hasResults(self):
        """Has Results"""
        self.runTrial(inputFile="data/matchedSquare.txt")
    
    @weight(1)
    @number('2.2')
    def test_matchBracket(self):
        """Bracket"""
        self.runTrial(input='1\n[]\n', expOutput='Yes')

    @weight(1)
    @number('2.3')
    def test_matchParenthesis(self):
        """Parenthesis"""
        self.runTrial(input='1\n()\n', expOutput='Yes')

    @weight(1)
    @number('2.4')
    def test_matchBraces(self):
        """Braces"""
        self.runTrial(input='1\n{}\n', expOutput='Yes')

    @weight(1)
    @number('2.5')
    def test_matchChevrons(self):
        """Chevrons"""
        self.runTrial(input='1\n<>\n', expOutput='Yes')
    
    @weight(1)
    @number('2.6')
    def test_mismatchBracket(self):
        """Left bracket"""
        self.runTrial(input='1\n[\n', expOutput='No')

    @weight(1)
    @number('2.7')
    def test_mismatchParenthesis(self):
        """Right parenthesis"""
        self.runTrial(input='1\n)\n', expOutput='No')

    @weight(1)
    @number('2.8')
    def test_mismatchClose(self):
        """Extra close"""
        self.runTrial(input='1\n{}}\n', expOutput='No')

    @weight(1)
    @number('2.9')
    def test_mismatchOpen(self):
        """Extra open"""
        self.runTrial(input='1\n<><\n', expOutput='No')
    
    @weight(1)
    @number('2.10')
    def test_reverse(self):
        """Reverse"""
        self.runTrial(input='1\n)(\n', expOutput='No')
    
    @weight(1)
    @number('2.11')
    def test_blank(self):
        """Blank"""
        self.runTrial(input='1\n\n', expOutput='Yes')

    @weight(1)
    @number('2.12')
    def test_nested(self):
        """Nested"""
        self.runTrial(input='1\n([])\n', expOutput='Yes')
    
    @weight(1)
    @number('2.13')
    def test_sequential(self):
        """Sequential"""
        self.runTrial(input='1\n[]{}\n', expOutput='Yes')
            
    @weight(1)
    @number('2.14')
    def test_mixed(self):
        """Mixed"""
        self.runTrial(input='1\n[{]}\n', expOutput='No')

    @weight(1)
    @number('3.1')
    def test_start(self):
        "Nazib Dataset, first lines"
        self.runTrial(inputFile="data/nazib.txt", solFile="expected/nazib-start.txt", mode=MatchMode.StartsWith | MatchMode.TrimWhitespace)
    
    @weight(1)
    @number('3.2')
    def test_end(self):
        "Nazib Dataset, last lines"
        self.runTrial(inputFile="data/nazib.txt", solFile="expected/nazib-end.txt", mode=MatchMode.EndsWith | MatchMode.TrimWhitespace)

    @weight(3)
    @number('3.3')
    def test_nazib(self):
        """Nazib Dataset"""
        self.runTrial(inputFile="data/nazib.txt", solFile="expected/nazib.txt")

    @weight(3)
    @number('3.4')
    def test_nasher(self):
        """Nasher Dataset"""
        self.runTrial(inputFile="data/nasher.txt", solFile="expected/nasher.txt")

    @weight(3)
    @number('3.5')
    def test_morass(self):
        """Morass Dataset"""
        self.runTrial(inputFile="data/morass.txt", solFile="expected/morass.txt")
