CC = g++
#CFLAGS = --std=c++17 -Wall -Werror -pedantic
CFLAGS = --std=c++20 -Wall -Werror -pedantic -g
LIB = -lboost_unit_test_framework

DEPS = $(wildcard *.hpp)
SOURCE = $(filter-out main.cpp, $(wildcard *.cpp))
OBJECTS = $(SOURCE:%.cpp=%.o)

PROGRAM = program

all: $(PROGRAM)

%.o: cpptests/%.cpp
	$(CC) $(CFLAGS) -c $<

%.o: %.cpp $(DEPS)
	$(CC) $(CFLAGS) -c $<

%.test: %.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^ $(LIB)

$(PROGRAM): main.o $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $^