import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('pytests')
    with open('/autograder/results/pytests.json', 'w') as f:
        JSONTestRunner(visibility='visible', stdout_visibility='visible', stream=f).run(suite)
