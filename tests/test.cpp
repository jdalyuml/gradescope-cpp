// Copyright 2023 Dr. Daly
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE Bracket Tests

#include <fstream>
#include <iostream>
#include <string>
#include <sstream>
#include <vector>

#include "TestDefs.hpp"
#include "bracket.hpp"

// Basic functions

BOOST_AUTO_TEST_CASE(TestBlank) {
    TEST_NUM("1.0");
    TEST_WEIGHT(1);
    BOOST_REQUIRE(isMatched(""));
}

BOOST_AUTO_TEST_CASE(TestLBrace) {
    TEST_NUM("1.1");
    TEST_WEIGHT(1);
    BOOST_REQUIRE(!isMatched("{"));
}

BOOST_AUTO_TEST_CASE(TestRBrace) {
    TEST_NUM("1.2");
    TEST_WEIGHT(1);
    BOOST_REQUIRE(!isMatched("}"));
}

BOOST_AUTO_TEST_CASE(TestChevrons) {
    TEST_NUM("1.3");
    TEST_WEIGHT(1);
    BOOST_REQUIRE(isMatched("<>"));
}

BOOST_AUTO_TEST_CASE(TestReverse) {
    TEST_NUM("1.4");
    TEST_WEIGHT(1);
    BOOST_REQUIRE_EQUAL(isMatched("><"), false);
}

BOOST_AUTO_TEST_CASE(TestSequential) {
    TEST_NUM("1.5");
    TEST_WEIGHT(1);
    BOOST_REQUIRE_EQUAL(isMatched("()[]{}<>"), true);
}
