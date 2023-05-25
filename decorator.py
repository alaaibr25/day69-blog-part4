#💛 a function returns a value based on the given arguments
# def add_one(number):
#     return number + 1
#
# print(add_one(2))

#💛 functions are first-class objects

# def say_hello(name):
#     return f"hello{name}"
#
# def greeting(greeter_func):
#     return greeter_func("LOLO")
#
# print(greeting(say_hello))   #helloLOLO

#💛 inner functions

# def parent_func():
#     print("from the parent")
#
#     def fisrt_child():
#         print("from child 1")
#
#     def second_child():
#         print("from child 2")

    # second_child()
    # fisrt_child()

# parent_func()

#🤍 the order does not matter,
#the printing only happens when the inner functions are executed
#the inner functions are not defined until the parent function is called


#💛 Returning Functions From Functions

# def parent(num):
#     def first_child():
#         return "from child 1"
#
#     def second_child():
#         return "from child 2"
#
#     if num == 1:

        #💦evaluating the function
        # return first_child()      #from child 1

        #💦reference to the function
    #     return first_child          #<function parent.<locals>.first_child at 0x000001F50625D260>
    # else:
        # return second_child()       #from child 2
#         return second_child
#
# first = parent(1)
# second = parent(2)
#
# print(first, second)

#💛 Simple Decorators

# def my_decorator(func):
#     def wrapper():
#         print("printing BEFORE the function is called")
#         func()
#         print("printing AFTER the function is called")
#     return wrapper
#
# def say_whee():
#     print("wheeeee")

# say_whee()     #wheeeee
# print(say_whee)   #<function say_whee at 0x0000026097A8D260>

# say_whee = my_decorator(say_whee)
# say_whee()
# print(say_whee)    #<function my_decorator.<locals>.wrapper at 0x000001E8BAEFA0C0>

#====================================================================#

#💛 Syntactic Sugar!


# def my_decorator(func):
#     def wrapper():
#         print("printing BEFORE the function is called")
#         func()
#         print("printing AFTER the function is called")
#     return wrapper
#
# @my_decorator
# def say_whee():
#     print("wheeeee")
#
# say_whee()


#====================================================================#
#💛Reusing Decorators
#----------------------------------------#
# 💚 do_twice decorator
# def do_twice(func):
#     def wrapper():
#         func()
#         func()
#
#     return wrapper
#----------------------------------------#

# @do_twice
# def say_whee():
#     print("whee")

# say_whee()

#----------------------------------------#
#💛Decorating Functions With Arguments
#🔴ERROR

# @do_twice
# def greet(name):
#     print(f"Hello{name}")

# greet("world")      #💔Error
#----------------------------------------#
#✔1

# def do_twice(func):
#     def wrapper(name):
#         func(name)
#         func(name)
#
#     return wrapper

# @do_twice
# def greet(name):
#     print(f"Hello{name}")
#
# greet("world")

# @do_twice
# def say_whee():
#     print("whee")
# say_whee()     #💔ERROR

#----------------------------------------#
#✔2

# def do_it(func):
#     def wrapper(*args, **kwargs):
#         func(*args, **kwargs)
#     return wrapper
#
# @do_it
# def greet(name):
#     print(f"Hello{name}")
#
# greet("world")

#💚Now both your say_whee() and greet() examples works
# @do_it
# def say_whee():
#     print("whee")

# say_whee()

#====================================================================#
#💛  Returning Values From Decorated Functions


# def do_it(func):
#     def wrapper(*args, **kwargs):
#         func(*args, **kwargs)
#     return wrapper

# @do_it
# def return_greeting(name):
#     print("create greeting")
#     return f"Hi {name}"

# return_greeting("fofo")       #it will print not return
# print(return_greeting("fofo"))  #print then None

#💚make the wrapper function returns the return value of the decorated function
#----------------------------------------#
#✔

# def do_return_print(func):
#     def wrapper(*args,**kwargs):
#         func(*args,**kwargs)
#         return func(*args, **kwargs)
#     return wrapper
#
# @do_return_print
# def return_greeting(name):
#     print("create greeting2")
#     return f"Hi {name}"
#
# print(return_greeting("lolo"))

#====================================================================#
#💛 Introspection is the ability of an object to know about its own attributes at runtime

# print(print)   #<built-in function print>
# print(print.__name__)    #print

# print(help(print))
#----------------------------------------#

# def decorator_func(func):
#     def wrapper(*args, **kwargs):
#         func()
#     return wrapper

#❣before decorator

# def say_whee():
#     print("whee")

# print(say_whee.__name__)     #say_whee

#❣After decorator

# @decorator_func
# def say_whee_decor():
#     print("whee")

# print(say_whee_decor.__name__)     #wrapper

#🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻🔻
#❣  @functools.wraps decorator
#will preserve information about the original function

# import functools
#
# def decor_func(func):
#     @functools.wraps(func)
#     def wrapper():
#         func()
#     return wrapper
#
# @decor_func
# def say_whee_decor():
#     print("whee")
#
# print(say_whee_decor.__name__)     #✔say_whee_decor
# say_whee_decor()
#====================================================================#
#====================================================================#
#💛💛A Few Real World Examples
#----------------------------------------#
#🟨1 boilerplate template
# import functools
#
# def decor(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         value = func(*args, **kwargs)
#         return value
#     return wrapper

#----------------------------------------#
#🟨2 Timing Functions
# import functools
# import time
#
# perf = time.perf_counter()
#
# def timer(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         start = perf
#         value = func(*args, **kwargs)
#         end = perf
#
#         run_time = end - start
#         print(f"Finished{func.__name__!r} in {run_time:.4f} sec")
#         return value
#     return wrapper


# @timer
# def waste_time(num):
#     for _ in range(num):
#         sum([i**2 for i in range(10000)])

# waste_time(1)

#----------------------------------------#
#🟨3 Flask login

# from flask import Flask, g, request, redirect, url_for
# import functools
# app = Flask(__name__)

# def login(func):
#     """Make sure user is logged in before proceeding"""
#     def wrapper(*args, **kwargs):
#         if g.user is None:
#             return redirect(url_for("login", next=request.url))
#         return func(*args, **kwargs)
#     return wrapper

# from functools import wraps
# @wraps(func)
























































#====================================================================#




