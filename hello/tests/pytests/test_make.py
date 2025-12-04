import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, tags, partial_credit
import Config

Timeout = 60 # Seconds

class TestMake(unittest.TestCase):

    @weight(1)
    @number("0.1")
    @tags("submission")
    @unittest.skipUnless(Config.RunImp(), "Implementation test")
    def test_req_files(self):
        """Files Submitted"""
        import os, re
        with open("requiredfiles.txt", "r") as files:
            missing = [f.strip() for f in files if not os.path.isfile(f.strip())]
            self.failIf(missing, "Files not submitted:\n\t{0}".format("\n\t".join(missing)))
        filere = re.compile('\\w+_\\w+_hw0+.(pdf|docx)')
        self.assertTrue(any(filere.match(f.lower()) for f in os.listdir('.')), msg="Couldn't find your writeup.")

    @weight(1)
    @number("0.2")
    @tags("make")
    @unittest.skipUnless(Config.RunImp(), "Implementation test")
    def test_prog_exists(self):
        """Make"""
        import os
        with open("compiledfiles.txt", "r") as files:
            missing = [f.strip() for f in files if not os.path.isfile(f.strip())]
            self.failIf(missing, "Missing compiled files:\n\t{0}".format("\n\t".join(missing)))
        reqFlags = ['-Wall', '-Werror', '-pedantic']
        with open("makeout.txt", "r") as file:
            for line in file:
                if "g++" in line:
                    for flag in reqFlags:
                        self.assertIn(flag, line.strip(), f'{flag} flag is required when compiling')


    @number("0.3")
    @tags("lint")
    @partial_credit(0)
    def test_lint(self, set_score=None):
        """Lint"""
        import os, subprocess, re
        maxPenalty = 5
        process = subprocess.run(["cpplint *.cpp *.hpp"],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, timeout=Timeout)
        msg = process.stdout
        #regex = re.compile(r"Total errors found: (\d*)")
        regex = re.compile(r"\w+\.\w+:\d+:.*\[(.*)\] \[\w*\]")
        failed = set()
        for line in msg.split('\n'):
            match = regex.search(line)
            if match:
                failed.add(match.group(1))
        numFailed = len(failed)

        # check for NOLINT in code to try to cheat this
        def isCodeFile(f):
            (_, ext) = os.path.splitext(f)
            extensions = {'.cpp', '.hpp', '.c', '.h'}
            return os.path.isfile(f) and ext in extensions
        files = [f for f in os.listdir() if isCodeFile(f)]
        for f in files:
            with open(f, 'r') as file:
                for i, line in enumerate(file):
                    if 'NOLINT' in line:
                        numFailed += 1
                        msg += f'Lint suppression not allowed: {f}:{i+1}\n'

        set_score(-min(numFailed, maxPenalty))
        self.failIf(numFailed != 0, f'\n{msg}')
        #self.fail(msg = match)
    
    @number("0.4")
    @tags("valgrind")
    @partial_credit(0)
    def test_valgrind(self, set_score=None):
        """Valgrind"""
        import subprocess, re
        set_score(-5)
        try:
            process = subprocess.run(["valgrind ./program"],
                    stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, timeout=Timeout)
        except subprocess.TimeoutExpired as ex:
            if ex.output:
                self.fail(f'valgrind timedout\n{ex.output.decode()}')
            else:
                self.fail('valgrind timedout (no output)')
        msg = process.stdout

        errre = re.compile(r'ERROR SUMMARY: (\d*) errors*')
        match = errre.search(msg)
        self.assertIsNotNone(match, msg)
        numFails = int(match.group(1))
        self.assertEqual(numFails, 0, msg)
        set_score(0)
    
    # @number("1.0")
    # @tags("test")
    # @partial_credit(2)
    # def test_theirs(self, set_score=None):
    #     """Your Tests"""
    #     import subprocess, re
    #     try:
    #         process = subprocess.run(["./test"],
    #                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, timeout=Timeout)
    #     except subprocess.TimeoutExpired as ex:
    #         if ex.output:
    #             self.fail('self unit tests timedout\n{ex.output.decode}')
    #         else:
    #             self.fail('self unit tests timedout (no output)')
    #     numTests = 0
    #     numFailed = 0
    #     testre = re.compile(r"Running (\d*) test cases*...")
    #     failre = re.compile(r"\*\*\* (\d*) (failures are|failure is) detected in the test module.*")
    #     msg = process.stdout
        
    #     match = testre.search(msg)
    #     if match:
    #         numTests = int(match.group(1))
    #     match = failre.search(msg)
    #     if match:
    #         numFailed = int(match.group(1))

    #     TestsRequired = 4
    #     t = min(numTests, TestsRequired)
    #     s = max(t - numFailed, 0) * 2 / TestsRequired
        
    #     set_score(s)
    #     self.assertGreaterEqual(numTests, TestsRequired, msg)
    #     self.assertEqual(numFailed, 0, msg)
    #     self.assertTrue(process.returncode == 0, msg)
        
