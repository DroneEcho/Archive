#ifndef MODEL_LOAD_SOLUTION_H
#define MODEL_LOAD_SOLUTION_H

#define MODEL_CFG_PATH "./data/model_load.cfg"

#include "config_manager.h"

class model_load_solution
{
public:
    model_load_solution() = default;

    std::shared_ptr<loader_creator> get_creator();
private:
    size_t id = 0;
};

#endif // MODEL_LOAD_SOLUTION_H
