CC = g++
CFLAGS = --std=c++17 -Wall -Werror -pedantic -g
LIB = -lboost_unit_test_framework
# Your .hpp files
DEPS = bracket.hpp
# Your compiled .o files
OBJECTS = bracket.o
# The name of your program
PROGRAM = bracket

.PHONY: all clean lint

# all isn't first since the students don't have the required test file

%.o: %.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<

$(PROGRAM): main.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

test: test.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

all: $(PROGRAM) test

clean:
	rm *.o $(PROGRAM)

lint:
	cpplint *.cpp *.hpp
