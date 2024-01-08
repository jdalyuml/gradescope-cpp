CC = g++
CFLAGS = --std=c++17 -Wall -Werror -pedantic -g
LIB = -lboost_unit_test_framework

STATIC_LIB = bracket.a

%.o: %.cpp
	$(CC) $(CFLAGS) -c $<

%.test: %.o
	$(CC) $(CFLAGS) -o $@ $^ ../${STATIC_LIB} $(LIB)
