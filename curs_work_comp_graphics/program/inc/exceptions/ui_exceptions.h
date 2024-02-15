#ifndef UI_EXCEPTIONS_H
#define UI_EXCEPTIONS_H

#include "base_exception.h"

class ui_field_format_exception: public base_exception
{
public:
    ui_field_format_exception() = default;
    ui_field_format_exception(std::string &message): base_exception(message) {}

    const char *what() const noexcept override
    {
        return "Problem with ui.";
    }
};

#endif // UI_EXCEPTIONS_H
