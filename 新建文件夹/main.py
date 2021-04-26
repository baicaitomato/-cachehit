import math

class slot:
    def __init__(self, tag, t):
        self.tag = tag
        self.t = t

    def getT(self):
        return self.t

    def getTag(self):
        return self.tag

    def change(self, tag, t):
        self.tag = tag
        self.t = t

    def __str__(self):
        return self.tag

class SetFIFO:
    def __init__(self, w):
        #Since the size is not big, this is lst but not heap
        self.lst = [slot('', i - w) for i in range(w)]

    def check(self, currtag, t):
        for i in self.lst:
            if i.getTag() == currtag:
                return True
        return False

    def put(self, currtag, t):
        least = self.lst[0].getT() + 1
        index = 0
        for i in range(len(self.lst)):
            if self.lst[i].getT() < least:
                index = i
                least = self.lst[i].getT()
        self.lst[index].change(currtag, t)

    def __str__(self):
        s = ""
        for i in range(len(self.lst)):
            s += "---" + "way " + str(i) + " : " + str(self.lst[i]) + "\n"
        return s[:-1]

class SetLRU(SetFIFO):
    def check(self, currtag, t):
        for i in self.lst:
            if i.getTag() == currtag:
                i.change(i.getTag(), t)
                return True
        return False


class RAM:
    def __init__(self, w, block, type):
        self.way = w
        self.block = block
        self.nsets = block / w
        if type == 0:
            self.ram = [SetFIFO(w) for i in range(int(self.nsets))]
        else:
            self.ram = [SetLRU(w) for i in range(int(self.nsets))]

    def getNsets(self):
        return self.nsets

    def check(self, currtag, currset, t):
        if self.ram[currset].check(currtag, t):
            print("hit!\n")
            print(currtag, " in ", currset)
            return 1
        else:
            print("miss\n")
            self.ram[currset].put(currtag, t)
            return 0

    def printRAM(self):
        for i in range(len(self.ram)):
            print("set", i, ": ")
            print(self.ram[i])


def print_ram(w, block, byte_in_block, digit, type):
    ram = RAM(w, block, type)
    print("有", ram.getNsets(), "个set")

    setbit = math.ceil(math.log(ram.getNsets(), 2))
    print("有", setbit, "个setbit")

    offset = math.ceil(math.log(byte_in_block, 2))
    print("有", offset, "个offsetbit")

    n = 0
    t = 0
    while True:
        ram.printRAM()
        if digit == 2:
            c = input("输入二进制地址: ")
        else:
            while True:
                c = input("输入十六进制地址: ")
                try:
                    c = bin(int(c.upper(), 16))[2:]
                    break
                except ValueError:
                    print("请输入正确十六位数字")
        currtag = c[0:(len(c) - setbit - offset)]
        print("currtag:", currtag)
        if ram.getNsets() == 1:
            currset = 0
        else:
            currset = int(c[len(currtag):(len(currtag) + setbit)])
        print("currset:", currset)
        n += ram.check(currtag, currset, t)
        print("现在有", n, "hit")
        if input("继续运行吗? Y/N:").upper() == 'N':
            break
        t += 1

def inp():
    w = int(input("请输入way: "))
    b = int(input("请输入blocks数量: "))
    bb = int(input("请输入一个block有多少bytes: "))
    type = int(input("输入0为FIFO, 输入1为LRU: "))
    if type != 0 and type != 1:
        print("请输入0或者1")
        return
    digit = int(input("输入2为2进制, 输入16为16进制: "))
    if digit != 2 and digit != 16:
        print("请输入2或者16")
        return
    print_ram(w, b, bb, digit, type)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    inp()