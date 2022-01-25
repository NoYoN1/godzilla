# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age


# p1 = Person("Harry potter", 25)
# p2 = Person("Hulk", 35)

# p = [p1, p2]


# class Movie:
#     def __init__(self, name):
#         self.name = name


# m1 = Movie("Iron Man")
# m2 = Movie("Spider Man")

# m = [m1, m2]

# for i in m:
#     print(i.name)
# class fun:
#     def fun1():
#         fun1.var = 100
#         print(fun1.var)

#     def fun2():
#         print(fun1.var)

#     fun1()
#     fun2()

#     print(fun1.var)

# from SubTest import SubTest

# Instance of Class Main
# Object = SubTest()

# # Calling Function1
# Object.Function1()
# Object.String1
# print(Object.String1)


# ccc = cerebro
# print("a1 " + str(a1))
# print("aaaaaa " + str(aaa))

class Val:

    def __init__(self):
        self.a = Val.val

    def val(self, num):
        self.b = num
        return self.b


class Calc:
    def cal(self):
        aa = 10
        bb = Val().a
        cc = aa + bb
        print("sum: " + cc)


Val().val(10)
