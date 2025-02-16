input = """
set i 31
set a 1
mul p 17
jgz p p
mul a 2
add i -1
jgz i -2
add a -1
set i 127
set p 316
mul p 8505
mod p a
mul p 129749
add p 12345
mod p a
set b p
mod b 10000
snd b
add i -1
jgz i -9
jgz a 3
rcv b
jgz b -1
set f 0
set i 126
rcv a
rcv b
set p a
mul p -1
add p b
jgz p 4
snd a
set a b
jgz 1 3
snd b
set f 1
add i -1
jgz i -11
snd a
jgz f -16
jgz a -19
"""

abc = []
for i in range(ord('a'), ord('z') + 1):
    abc.append(chr(i))

class Processor:
    def __init__(self, prg):
        self.lastsound = None
        self.prg = prg
        self.ip = 0
        self.halted = False
        self.reg = {}
        for c in abc:
            self.reg[c] = 0

    def eval(self, ci):
        if ci in abc:
            return self.reg[ci]
        else:
            return int(ci)

    def snd(self, ci):
        self.lastsound = self.eval(ci)
        self.ip += 1

    def set(self, xc, yci):
        self.reg[xc] = self.eval(yci)
        self.ip += 1

    def add(self, xc, yci):
        self.reg[xc] += self.eval(yci)
        self.ip += 1

    def mul(self, xc, yci):
        self.reg[xc] *= self.eval(yci)
        self.ip += 1

    def mod(self, xc, yci):
        self.reg[xc] %= self.eval(yci)
        self.ip += 1

    def jgz(self, xci, yci):
        x = self.eval(xci)
        y = self.eval(yci)
        if x > 0:
            self.ip += y
        else:
            self.ip += 1

    def rcv(self, xci):
        x = self.eval(xci)
        if x != 0:
            self.halted = True
        else:
            self.ip += 1

    def run(self):
        while not self.halted:
            instr, *params = self.prg[self.ip].split(' ')
            f = getattr(self, instr, None)
            f(*params)

prgi = input.splitlines()
prg = []
for p in prgi:
    if p != '':
        prg.append(p)

proc = Processor(prg)
proc.run()
print(proc.lastsound)
