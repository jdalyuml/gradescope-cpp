// Copyright 2023 Dr. Daly
#include "common.hpp"


BOOST_AUTO_TEST_CASE(TestRBrace) {
    BOOST_REQUIRE(!isMatched("}"));
}
