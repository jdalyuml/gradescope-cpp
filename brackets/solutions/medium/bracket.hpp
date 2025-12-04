// Copyright 2023 Dr. Daly
// Permission granted to use and modify for educational purposes
// Copyright [Year] [Yourname]
#pragma once

#ifndef BRACKET_HPP
#define BRACKET_HPP

#include <string>

bool isLBracket(char c);
bool isRBracket(char c);
bool areMatching(char l, char r);

bool isMatched(const std::string& line);

#endif
