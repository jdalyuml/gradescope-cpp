// Copyright 2023 Jaeda
#include <iostream>

#include "bracket.hpp"

using std::cin;
using std::cout;
using std::endl;
using std::string;

int main() {
    int numLines;
    cin >> numLines;
    cin.get();// Burn extra newline
    for (int i = 0; i < numLines; i++) {
        string line;
        getline(cin, line);
        if (isMatched(line)) {
            cout << "Yes" << endl;
        }else{
            cout << "No" << endl;
        }
    }
    return 0;
}
