import math


class Calculator:
    def init(self):
        self.__init__ = []
        self.operations = ["+", "-", "*", "/", "^", "^2", "sin", "cos", "tg", "ln", "lg"]
        self.firstoperations = ["sin", "cos", "tg", "ln", "lg"]

    def go(self, string):
        arr = self.inputing(string)
        self.schet(arr)
        return arr[0]

    def summing(self, num_1, num_2):
        return num_1 + num_2

    def subtraction(self, num_1, num_2):
        return num_1 - num_2

    def division(self, num_1, num_2):
        return num_1 / num_2

    def multiplying(self, num_1, num_2):
        return num_1 * num_2

    def getdegree(self, num_1, num_2):
        return num_1**num_2

    def getsquare(self, num_1):
        return num_1 ^ 2

    def sin(self, num_1):
        return math.sin(num_1 * 0.0174533)

    def cos(self, num_1):
        return math.cos(num_1 * 0.0174533)

    def tg(self, num_1):
        return math.tan(num_1 * 0.0174533)

    def ln(self, num_1):
        return math.log(num_1)

    def lg(self, num_1):
        return math.log10(num_1)

    def inputing(self, string: str):
        k = 0
        arr = []
        while k != len(string) - 1:
            if string[k].isdigit():
                l = 0
                while string[l + k].isdigit() or string[l + k] == "." and l + k < len(string) - 2:
                    l += 1
                arr.append(string[k : l + k])
                k += l
            if string[k].isalpha():
                m = 0
                while string[m + k].isalpha() and l + k < len(string) - 2:
                    m += 1
                if string[k : m + k] in self.firstoperations:
                    arr.append(string[k : m + k])
                else:
                    raise AssertionError("Wrong input")
                k += m
            if string[k] in ["+", "-", "*", "/"]:
                arr.append(string[k])
                k += 1
            if string[k] == "^":
                if string[k + 1] == "2":
                    arr.append(string[k : k + 1])
                    k += 2
                else:
                    arr.append("^")
                    k += 1
        return arr

    def schet(self, arr):
        for sth in self.firstoperations:
            if sth in arr:
                ind = arr.index(sth)
                if sth == "sin":
                    elem = str(self.sin(float(arr[ind + 1])))
                elif sth == "cos":
                    elem = str(self.cos(float(arr[ind + 1])))
                elif sth == "tg":
                    elem = str(self.tg(float(arr[ind + 1])))
                elif sth == "lg":
                    elem = str(self.lg(float(arr[ind + 1])))
                elif sth == "ln":
                    elem = str(self.ln(float(arr[ind + 1])))
                arr[ind] = elem
                del arr[ind + 1]
        while "^" in arr:
            i = arr.index("^")
            elem = str(self.getdegree(float(arr[i - 1]), float(arr[i + 1])))
            arr[i - 1] = elem
            del arr[i]
        while "^2" in arr:
            i = arr.index("^2")
            elem = str(self.getsquare(float(arr[i - 1])))
            arr[i - 1] = elem

            del arr[i]
        while "*" in arr:
            i = arr.index("*")
            elem = str(self.multiplying(float(arr[i - 1]), float(arr[i + 1])))
            arr[i - 1] = elem
            del arr[i + 1]
            del arr[i]
        while "/" in arr:
            i = arr.index("/")
            elem = str(self.division(float(arr[i - 1]), float(arr[i + 1])))
            arr[i - 1] = elem
            del arr[i + 1]
            del arr[i]
        while "+" in arr:
            i = arr.index("+")
            elem = str(self.summing(float(arr[i - 1]), float(arr[i + 1])))
            arr[i - 1] = elem
            del arr[i + 1]
            del arr[i]
        while "-" in arr:
            i = arr.index("-")
            elem = str(self.subtraction(float(arr[i - 1]), float(arr[i + 1])))
            arr[i - 1] = elem
            del arr[i + 1]
            del arr[i]
        return arr

    a = Calculator()
    g = input()
    g += " "
    print(a.go(g))
