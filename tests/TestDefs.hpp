// Copyright 2023 Dr. Daly
#pragma once

#include <string>
#include <sstream>

#include <boost/test/included/unit_test.hpp>
#include <boost/test/tools/floating_point_comparison.hpp>

namespace utf = boost::unit_test;

template<typename T>
std::string StrCat(std::string s, T x) {
    std::stringstream ss;
    ss << s;
    ss << x;
    return ss.str();
}

// ./test -f XML -l unit_scope > results.xml
#define TEST_WEIGHT(X) BOOST_TEST_MESSAGE(StrCat("Weight:", X))
#define TEST_POINTS(X) BOOST_TEST_MESSAGE(StrCat("Points:", X))

#define TEST_NUM(X) BOOST_TEST_MESSAGE(StrCat("Number:", X))
