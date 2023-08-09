# Gradescope C++ Autograder

A package for autograding multi-file C++ programs on Gradescope.  This allows for unit tests using the Boost Unit Test Framework as well as I/O tests using Python.

As an example, a sample project for bracket matching.  The compiled version for this program solves problem 673 on the [Online Judge](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=8&page=show_problem&problem=614), but the student is also required to implement an `isMatched` function that tests a singled line.  The function will be tested using unit tests in C++ and the complete program will be invoked in Python.

## Configuration

### Makefile

A sample Makefile has been supplied in the starter code.  You can change the expected .hpp, .o, and produced program in the Makefile before giving it to students.

### List of Required Files

The `requiredfiles.txt` file contains a list of file names that students are required to supply.  Their submissions are expected to contain files matching those names exactly.  The `compiledfiles.txt` file is similar, but contains the names of any compiled files that should be produced by their makefile.

The required and compiled files are worth points separately and are controlled by the `@weight` annotation on the first two tests of `tests/tests/test_make.py` file.

### Valgrind and Lint tests

The last two tests for `test_make.py` test for linting using [cpplint](https://github.com/cpplint/cpplint) and memory errors using [Valgrind](https://valgrind.org/docs/manual/index.html).  By default, each is worth 0 points; students lose points for having lint or memory errors.  **The `valgrind` command needs to be editted to include their program name.**

Each lint error costs 1 point, up to the maximum in the `MaxLintPenalty` variable.
Any error when running `valgrind` deducts points equal to the `ValgrindPenalty` variable.

### I/O Tests

The `tests/tests/test_trial.py` file contains I/O tests.  Set the name of the student's program by changing the `ProgramName` variable.  Each test is a Python `unittest` test and has annotations from the Gradescope [decorators](https://gradescope-autograders.readthedocs.io/en/latest/python/) library.

A `runTrial` helper function is provided that will invoke the student's program.  Optional parameters exist for setting the programs command-line arguments, input over stdin, and expected output over stdout.  If expected output is provided it checks that the output the program provides over stdout matches that provided by the given output.  By default, differences in leading and trailing whitespace (but not intermediate whitespace) is ignored.  This behavior can be changed by changing the mode argument.

### Unit Tests

The `tests/test.cpp` file contains the C++ [Boost unit tests](https://www.boost.org/doc/libs/1_82_0/libs/test/doc/html/index.html).  Each test uses macros defined in `tests/TestDefs.hpp` to set the attributes.

Use the `TEST_WEIGHT` macro to change the value of the test.  By default, successful tests will award all of the points and failed tests will award 0 points.  Use the `TEST_POINTS` macro to award partial credit.



