input = "4	1	15	12	0	9	9	5	5	8	7	3	14	5	12	3"
# input = "0	2	7	0"

input = list(map(lambda x: int(x), input.split()))

class StateMachine:
    def __init__(self, init):
        self.banks = init

    def __str__(self):
        return str(self.banks)

    def step(self):
        redistribute = max(self.banks)
        index = self.banks.index(redistribute)
        self.banks[index] = 0
        while redistribute > 0:
            index += 1
            index %= len(self.banks)
            self.banks[index] += 1
            redistribute -= 1

class StateMachineStopper:
    def __init__(self, sm):
        self.sm = sm

    def repeat(self):
        count = 0
        self.visited = set()
        self.visited.add(str(self.sm))
        while True:
            count += 1
            self.sm.step()
            # print(self.sm)
            if str(self.sm) in self.visited:
                return count
            else:
                self.visited.add(str(self.sm))

sm = StateMachine(input)
print(StateMachineStopper(sm).repeat())
print(StateMachineStopper(sm).repeat())
