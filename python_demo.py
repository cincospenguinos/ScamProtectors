# you can import stuff
import math

# write single lines commands, which execute in order
x = math.cos(1)
print(x)


# define functions, which must be declared before used
def my_function(untyped_parameter, optional_parameter=True):
    if optional_parameter:
        return untyped_parameter + 1
    else:
        return untyped_parameter + 2


# here is where we declare main and most in-line code should go here
def main():

    x = 3

    y = my_function(x)
    z = my_function(x, optional_parameter=False)

    print(y)
    print(z)

    # you can do almost everything with these two data structures:

    # dictionary
    my_dict = {}
    my_dict["Matt"] = 0
    # no ++ or -- in python :(
    my_dict["Matt"] += 1
    print(my_dict)
    # (python doesn't care about single or double quotes)
    print(my_dict['Matt'])
    # you can cast to types with int() str() etc.
    print(str(my_dict['Matt']) + str(x))

    # list
    my_list = []
    my_list.append("Matt")
    my_list.append("Andre")
    my_list.append("Jess")
    my_list.append("Candace")
    print(my_list)

    #slicing is super useful in python [start:stop:increment], empty defaults to beginning or end

    # beginning to 2 (exclusive)
    print(my_list[:2])

    # 2 (inclusive) to end
    print(my_list[2:])

    # from 3rd to the last to the end
    print(my_list[-3:])

    # beginning to end backwards
    print(my_list[::-1])

    # beginning to end by twos
    print(my_list[::2])

    # list comprehension can save TONS of time [expression for var in list if expression]

    my_list = [1, 2, 3, 4, 5]

    new_list = [x + 1 for x in my_list if x % 2 == 1]

    print(new_list)


# this allows a python file to be used as an executable (main will run) or as a library (main will not)
if __name__ == "__main__":
    main()


