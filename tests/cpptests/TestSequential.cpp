// Copyright 2023 Dr. Daly
#include "common.hpp"

BOOST_AUTO_TEST_CASE(TestSequential) {
    BOOST_REQUIRE_EQUAL(isMatched("()[]{}<>"), true);
}
