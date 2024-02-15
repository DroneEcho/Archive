#ifndef CONVEYOR_H
#define CONVEYOR_H

#include <random>
#include <vector>
#include <iostream>
#include <queue>
#include <thread>
#include <chrono>
#include <ctime>
#include <mutex>
#include <fstream>
#include "moor.h"


#define THREADS 3
#define STEP_SIZE 100
#define STEP_COUNT 5


struct queues_s
{
    std::queue<request> q1;
    std::queue<request> q2;
    std::queue<request> q3;
};

using queues_t = struct queues_s;

void parse_linear(string str, size_t size, bool is_print);
void parse_parallel(string str, size_t size, bool is_print);
void time_mes(void);
void info_stages(void);
request generate(string str);

#endif
