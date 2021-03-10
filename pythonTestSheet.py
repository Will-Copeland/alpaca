def indentIfTest(arg):
    print(arg)

    x = 0
    y = -1

    if x > y:
        print("x > y")

    if y > x:
        print("y > x")
    elif True:
        print("helo")

    print("anyway")


def nullishCheck(arg=None):
    print("arg is: ", arg)
    result1 = arg or "be"
    print(result1)


# indentIfTest("helo")
# nullishCheck()


def argumentOrderCheck(arg1, arg2, arg3):
    print("arg1 ", arg1)
    print("arg2 ", arg2)
    print("arg3 ", arg3)



argumentOrderCheck(arg2="two", arg3="three", arg1="one")