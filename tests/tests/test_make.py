import unittest
from gradescope_utils.autograder_utils.decorators import weight, number, tags, partial_credit

class TestMake(unittest.TestCase):
    # Configuration Options
    MaxLintPenalty = 5 # Lose 1 point per lint error, up to this maximum
    ValgrindPenalty = 5 # Lose points for having memory leak issues

    @weight(0)
    @number("0.1")
    @tags("submission")
    def test_req_files(self):
        """Files Submitted"""
        import os
        with open("requiredfiles.txt", "r") as files:
            missing = [f.strip() for f in files if not os.path.isfile(f.strip())]
            self.failIf(missing, "Files not submitted:\n\t{0}".format("\n\t".join(missing)))

    @weight(2)
    @number("0.2")
    @tags("make")
    def test_prog_exists(self):
        """Make"""
        import os
        with open("compiledfiles.txt", "r") as files:
            missing = [f.strip() for f in files if not os.path.isfile(f.strip())]
            self.failIf(missing, "File did not build:\n\t{0}".format("\n\t".join(missing)))


    @number("0.3")
    @tags("lint")
    @partial_credit(0)
    def test_lint(self, set_score=None):
        """Lint"""
        import subprocess, re
        process = subprocess.run(["cpplint *.cpp *.hpp"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        msg = ""
        regex = re.compile(r"Total errors found: (\d*)")
        for line in process.stdout:
            msg = msg + line
        match = regex.search(msg)
        if match:
            numFailed = int(match.group(1))
        else:
            numFailed = 0
        set_score(-min(numFailed, TestMake.MaxLintPenalty))
        self.assertEqual(numFailed, 0, msg)
    
    @number("0.4")
    @tags("valgrind")
    @partial_credit(0)
    def test_valgrind(self, set_score=None):
        """Valgrind"""
        import subprocess
        set_score(TestMake.ValgrindPenalty)
        process = subprocess.run(["valgrind ./bracket < data/input.txt"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True)
        msg = ""
        for line in process.stdout:
            msg = msg + line
        self.assertTrue(process.returncode == 0, msg)
        set_score(0)
    