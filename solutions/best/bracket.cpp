// Copyright 2023 Jaeda
#include "bracket.hpp"

#include <stack>

bool isLBracket(char c) {
    return c == '(' || c == '[' || c == '{' || c == '<';
}

bool isRBracket(char c) {
    return c == ')' || c == ']' || c == '}' || c == '>';
}

bool areMatching(char l, char r) {
    return (r - l) == 1 || (r - l) == 2;
}

bool isMatched(const std::string& line) {
    std::stack<char> lbrackets;
    for (char c : line) {
        if (isLBracket(c)) {
            lbrackets.push(c);
        } else if (isRBracket(c)) {
            if (lbrackets.empty() || !areMatching(lbrackets.top(), c)) {
                return false;
            }
            lbrackets.pop();
        }
    }
    return lbrackets.empty();
}
