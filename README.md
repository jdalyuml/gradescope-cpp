# Gradescope C++ Autograder

A package for autograding multi-file C++ programs on Gradescope.  This allows for unit tests using the Boost Unit Test Framework as well as I/O tests using Python.

As an example, there are two sample projects included.  The first project is a "hello world" assignment with a twist; the student has to additionally print a random word selected for them by the autograder.  The students will have to make at least two submissions since they won't know what their personal word is until after they have made a submission.  This will help students acclimate to the idea that it is acceptable to make multiple submissions.

The second sample project is for bracket matching.  The compiled version for this program solves problem 673 on the [Online Judge](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=8&page=show_problem&problem=614), but the student is also required to implement an `isMatched` function that tests a singled line.  The function will be tested using unit tests in C++ and the complete program will be invoked in Python.



## Configuration

### Projects

The `common/Projects.cfg` file contains a list of projects and maps the assignment name on Gradescope to a directory in the autograder.  The project names in the `Projects.cfg` file should be lower-case.  Your assignment name on Gradescope can use normal capitalization.  The autograder (through the `common/ProjectSelector.py` script) will take any part of the assignment name before the first ":", convert it to lower-case, and use it to determine which project should be run.

### Late Penalties

The `common/Projects.cfg` file also contains information about late penalties.  The autograder gets submission and deadline times (including any personal extensions) from Gradescope and computes late penalties automatically.  **Late penalties are only applied to the autograded portion**; penalties for the manual portion must be applied manually.

The `PenaltyPerDay` field is how much to deduct for each day or fraction thereof that the submission is late (default -10%), up to the limit set by `MaxPenalty` (default -50%).  The `Leeway` field gives a little window after the nominal deadline where it is not penalized for those students submitting close to the deadline (default 10 minutes).  The autograder also allows for a reduced penalty for students who make their first submission on time but continue working after the deadline.  The `Grace` field is a time window in which a student who has made an on-time submission will receive _no_ late penalty (default 1 day).  If their final submission is after the grace window, they receive the normal late penalty reduced by the amount in the `Semigrace` field (default 5%).  Under the defaults, a student who submits for the first time two days late will receive a -20% penalty whereas a student who had an on-time solution but made their final submission two days late will receive only a -15% penalty.

For group assignments, the behavior is currently undefined if some of them have extensions; it selects one of the student's deadlines arbitrarily.

### Makefile

A sample Makefile has been supplied in the starter code.  You can change the expected .hpp, .o, and produced program in the Makefile before giving it to students.

### List of Required Files

The `requiredfiles.txt` file contains a list of file names that students are required to supply.  Their submissions are expected to contain files matching those names exactly.  The `compiledfiles.txt` file is similar, but contains the names of any compiled files that should be produced by their makefile.

The required and compiled files are worth points separately and are controlled by the `@weight` annotation on the first two tests of `tests/tests/test_make.py` file.

### Valgrind and Lint tests

The last two tests for `test_make.py` test for linting using [cpplint](https://github.com/cpplint/cpplint) and memory errors using [Valgrind](https://valgrind.org/docs/manual/index.html).  By default, each is worth 0 points; students lose points for having lint or memory errors.  **The `valgrind` command needs to be editted to include their program name.**

Each lint error costs 1 point, up to the maximum in the `MaxLintPenalty` variable.
Any error when running `valgrind` deducts points equal to the `ValgrindPenalty` variable.
You can adjust which lint issues to ignore in the `common/CPPLINT.cfg` file, as is normal for `cpplint`.

### I/O Tests

The `tests/pytests/test_trial.py` file contains I/O tests.  Set the name of the student's program by changing the `ProgramName` variable.  Each test is a Python `unittest` test and has annotations from the Gradescope [decorators](https://gradescope-autograders.readthedocs.io/en/latest/python/) library.

A `runTrial` helper function is provided that will invoke the student's program.  Optional parameters exist for setting the programs command-line arguments, input over stdin, and expected output over stdout.  If expected output is provided it checks that the output the program provides over stdout matches that provided by the given output.  By default, differences in leading and trailing whitespace (but not intermediate whitespace) is ignored.  This behavior can be changed by changing the mode argument.

### Unit Tests

The `tests/cpptests` directory contains the C++ [Boost unit tests](https://www.boost.org/doc/libs/1_82_0/libs/test/doc/html/index.html).  Each test is defined its own file.  This makes the tests more severable; if there is a compiler error when building one test, the other tests may still build correctly.

The actual test that are run are controlled by the `Tests.yaml` file.  Each test has 4 parts.  `program` is the name of one of the test and should have a corresponding `.cpp` file to go with it.  `number` controls the order that the tests will be displayed in Gradescope.  `desc` is a message that will be printed as part of the results describing the test so that the students can have more information about what the test does.  Finally, `weight` is how many points the test is worth.  A passing test is worth that number of points and a failing test is worth 0 points.  Unlike the Python tests, it is currently not possible to assign partial or negative credit to C++ tests.


