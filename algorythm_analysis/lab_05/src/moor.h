#ifndef MOOR_H
#define MOOR_H

#include <iostream>
#include <string>
#include <vector>
using namespace std;

struct log
{
    std::string data;
    float start;
    float end;
};

using log_s = struct log;

struct pred
{
    bool operator()(const log_s& dot1, const log_s& dot2)
    {
        return dot1.start < dot2.start;
    }
};

struct request
{
    string text;

    string sub_str;
    vector<int> inputs;
    int comb = 0;
    int ans = 0;

    vector<log_s> logger;
};

using request = struct request;


// Funcs
void search( string txt, string pat, int &ans);
void search_detect(string txt, string pat, vector<int>& inp, int &comb);

#endif
