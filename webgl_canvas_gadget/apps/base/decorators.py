def jinja2_global(function):
    function.jinja2_global = True
    return function

def jinja2_filter(function):
    function.jinja2_filter = True
    return function

def jinja2_test(function):
    function.jinja2_test = True
    return function