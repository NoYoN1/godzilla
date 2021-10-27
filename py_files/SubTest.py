class SubTest:

    # constructor of Main class
    def __init__(self):
        # Initialization of the Strings
        self.String1 = "Hello"
        self.String2 = "World"

    def Function1(self):
        # calling Function2 Method
        global a
        self.Function2()
        print("Function1 : ", self.String2)
        a = "Function1 : ", self.String2

    def Function2(self):
        print("Function2 : ", self.String1)
