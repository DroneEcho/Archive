#include <iostream>

#include "conveyor.h"



void print_menu()
{
    printf("\n\nMour algorythm \
        \n\t1. linear \
        \n\t2. conveyer \
        \n\t3. time \
      \n\n\t0. exit\n\n");
}


void run()
{
    int option = -1;

    while (option != 0)
    {
        print_menu();

        std::cout << "Choice: ";
        std::cin >> option;

        if (option == 1)
        {   
            int size = 0;
            std::string str;
            std::cout << "\n\nSize: ";
            std::cin >> size;

            std::cout << "Searched string: ";
            std::cin >> str;
            parse_linear(str, size, true);
        }
        else if (option == 2)
        {
            int size = 0;
            std::string str;
            std::cout << "\n\n Size: ";
            std::cin >> size;

            std::cout << "Searched string: ";
            std::cin >> str;

            parse_parallel(str, size, true);
        }
        else if (option == 3)
        {
            time_mes();
        }
        else
        {
            printf("\nERR\n");
        }
    }
}



int main(void)
{
    srand(time(NULL));
    run();

    return 0;
}
