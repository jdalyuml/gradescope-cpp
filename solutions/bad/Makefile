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

all: $(PROGRAM) $(PROGRAM).a

%.o: %.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<

$(PROGRAM): main.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

$(PROGRAM).a: $(OBJECTS)
	ar rcs $@ $^

clean:
	rm *.o $(PROGRAM)

lint:
	cpplint *.cpp *.hpp
