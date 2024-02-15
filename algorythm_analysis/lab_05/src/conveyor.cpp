#include "conveyor.h"
#include <algorithm>
double time_now = 0;

std::vector<double> t1;
std::vector<double> t2;
std::vector<double> t3;

std::vector<log_s> to_print;
std::string path = "C:/Users/Maria/Desktop/aa/lab_05/src/src/log";

request generate(string str)
{
    request tmp;
    int length = 100;
    static string charset = "abcdefghijklmnopqrstuvwxyz";
    tmp.text.resize(length);
    for (int i = 0; i < length; i++)
        tmp.text[i] = charset[rand() % charset.length()];
    tmp.sub_str = str;
    return tmp;
}

void log_in_file( request req, int task_num)
{
    std::ofstream out;
    std::string to_log = path+ "/" + to_string(task_num) + ".txt";
    out.open(to_log);

    out << req.sub_str << endl;
    out << req.text << endl;
    out << req.ans << " : ";
    for (auto& inp: req.inputs)
        out << inp << " ";
    out << endl;
    out << req.comb << endl;
    out.close();
}
void log_linear(request &req, int task_num, int stage_num, bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double start_res_time = time_now, res_time = 0;

    time_start = std::chrono::system_clock::now();
    if (stage_num == 1)
    {
        search(req.text, req.sub_str, req.ans);
    }
    else if (stage_num == 2)
    {
        search_detect(req.text, req.sub_str, req.inputs, req.comb);
    }
    else if (stage_num == 3)
    {
        log_in_file(req, task_num);
    }

    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count()) / 1e9;

    time_now = start_res_time + res_time;

    if (is_print)
    {
        log_s tmp;
        tmp.data = "Task: "+ to_string(task_num) +", Tape: " + to_string(stage_num) + ", Start: "+ \
                to_string(start_res_time) + ", End: " + to_string(start_res_time + res_time) + "\n";
        tmp.start = start_res_time;
        tmp.end = start_res_time + res_time;
        req.logger.push_back(tmp);
    }
}


void log_conveyor(request &req, int task_num, int stage_num, bool is_print)
{
    std::chrono::time_point<std::chrono::system_clock> time_start, time_end;
    double res_time = 0;
    double start_res_time = time_now;
    time_start = std::chrono::system_clock::now();
    if (stage_num == 1)
    {
        search(req.text, req.sub_str, req.ans);
    }
    else if (stage_num == 2)
    {
        search_detect(req.text, req.sub_str, req.inputs, req.comb);
    }
    else if (stage_num == 3)
    {
        log_in_file(req, task_num);
    }
    time_end = std::chrono::system_clock::now();

    res_time = (std::chrono::duration_cast<std::chrono::nanoseconds>
            (time_end - time_start).count()) / 1e9;


    time_now = start_res_time + res_time;

    if (is_print)
    {
        log_s tmp;
        tmp.data = "Task: "+ to_string(task_num) +", Tape: " + to_string(stage_num) + ", Start: "+ \
                to_string(start_res_time) + ", End: " + to_string(start_res_time + res_time) + "\n";
        tmp.start = start_res_time;
        tmp.end = start_res_time + res_time;
        req.logger.push_back(tmp);
    }
}


void stage1_linear(request &req, int task_num, bool is_print)
{
    log_linear(req, task_num, 1, is_print);
}



void stage2_linear(request &req, int task_num, bool is_print)
{   
    log_linear(req, task_num, 2, is_print);
}


void stage3_linear(request &req, int task_num, bool is_print)
{   
    log_linear(req, task_num, 3, is_print);
}


void parse_linear(std::string str, size_t size, bool is_print)
{
    time_now = 0;
    to_print.clear();
    std::queue<request> q1;
    std::queue<request> q2;
    std::queue<request> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    for (size_t i = 0; i < size; i++)
    {
        request res = generate(str);
        queues.q1.push(res);
    }

    for (size_t i = 0; i < size; i++)
    {
        request req = queues.q1.front();
        stage1_linear(req, i + 1, is_print);
        queues.q1.pop();
        queues.q2.push(req);

        req = queues.q2.front();
        stage2_linear(req, i + 1, is_print);
        queues.q2.pop();
        queues.q3.push(req);

        req = queues.q3.front();
        stage3_linear(req, i + 1, is_print);
        queues.q3.pop();

        if (is_print)
        {
            for (auto& log1: req.logger)
            {
                to_print.push_back(log1);
            }
        }
    }
    if (is_print)
    {
         sort(to_print.begin(), to_print.end(), pred());
         for (auto& one: to_print)
             cout << one.data;
    }
}

std::mutex m;

void stage1_parallel(std::queue<request> &q1, std::queue<request> &q2, std::queue<request> &q3, bool is_print)
{
    int task_num = 1;

    while(!q1.empty())
    {      
        m.lock();
        request req = q1.front();
        m.unlock();

        log_conveyor(req, task_num++, 1, is_print);

        m.lock();
        q2.push(req);
        q1.pop();
        m.unlock();
    }
}


void stage2_parallel(std::queue<request> &q1, std::queue<request> &q2, std::queue<request> &q3, bool is_print)
{
    int task_num = 1;

    do
    {   
        m.lock();
        bool is_q2empty = q2.empty();
        m.unlock();

        if (!is_q2empty)
        {   
            m.lock();
            request matrix = q2.front();
            m.unlock();

            log_conveyor(matrix, task_num++, 2, is_print);

            m.lock();
            q3.push(matrix);
            q2.pop();
            m.unlock();
        }
    } while (!q1.empty() || !q2.empty());
}


void stage3_parallel(std::queue<request> &q1, std::queue<request> &q2, std::queue<request> &q3, bool is_print)
{
    int task_num = 1;

    do
    {
        m.lock();
        bool is_q3empty = q3.empty();
        m.unlock();

        if (!is_q3empty)
        {
            m.lock();
            request req = q3.front();
            m.unlock();

            log_conveyor(req, task_num++, 3, is_print);

            m.lock();
            q3.pop();
            m.unlock();
            if (is_print)
            {
                for (auto& log1: req.logger)
                {
                    to_print.push_back(log1);
                }
            }
        }
    } while (!q1.empty() || !q2.empty() || !q3.empty());
}


void parse_parallel(std::string str, size_t size, bool is_print)
{
    to_print.clear();
    t1.resize(size + 1);
    t2.resize(size + 1);
    t3.resize(size + 1);

    for (size_t i = 0; i < size + 1; i++)
    {
        t1[i] = 0;
        t2[i] = 0;
        t3[i] = 0;
    }

    std::queue<request> q1;
    std::queue<request> q2;
    std::queue<request> q3;

    queues_t queues = {.q1 = q1, .q2 = q2, .q3 = q3};

    
    for (size_t i = 0; i < size; i++)
    {
        request res = generate(str);
        
        q1.push(res);
    }

    std::thread threads[THREADS];

    threads[0] = std::thread(stage1_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[1] = std::thread(stage2_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);
    threads[2] = std::thread(stage3_parallel, std::ref(q1), std::ref(q2), std::ref(q3), is_print);

    for (int i = 0; i < THREADS; i++)
    {
        threads[i].join();
    }
    if (is_print)
    {
         sort(to_print.begin(), to_print.end(), pred());
         for (auto& one: to_print)
             cout << one.data;
    }
}


void time_mes(void)
{
    int alg_option;

    std::cout << "\n\nAlg: \
                    \n\t1) linear \
                    \n\t2) parallel\n\n";

    std::cin >> alg_option;

    if ((alg_option < 3) && (alg_option > 0))
    {
        printf("\n\n size     |   time \
            \n----------------------\n");
        for (size_t i_size = 100; i_size <= 1000; i_size += STEP_SIZE)
        {
            time_now = 0;

            if (alg_option == 1)
            {
                parse_linear("abc", i_size, false);

                printf("  %3ld     |   %3.4f\n", i_size, time_now);
            }
            else if (alg_option == 2)
            {
                parse_parallel("abc", i_size, false);

                printf("  %3ld     |   %3.4f\n", i_size, time_now);
            }

        }
    }
    else
    {
        printf("Ошибка: Тип замера выбран неварно\n");
    }
}
