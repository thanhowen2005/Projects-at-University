#ifndef STRUCT_H
#define STRUCT_H

#include <string>

using namespace std;

struct profile {
    string username;
    string password;
    double normalScore;
    double hiddenScore;
    double stepScore;
};

#endif