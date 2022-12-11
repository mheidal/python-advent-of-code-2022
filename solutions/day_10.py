class RegisterCycle:
    def __init__(self):
        self.cycle = 0
        self.register = 1
        self.summed_signals = 0
        self.output = ""

    def increment(self):
        self.cycle += 1
        if (self.cycle -20) % 40 == 0:
            self.summed_signals += self.cycle * self.register
        crt_pos = (self.cycle - 1) % 40
        if -1 <= (self.register - crt_pos) <= 1:
            self.output += "█"
        else:
            self.output += " "
        if crt_pos == 39:
            self.output += '\n'

    def add_to_register(self, val: int):
        self.register += val

    def __repr__(self):
        return f"cycle={self.cycle}, reg={self.register}, sum={self.summed_signals}"


def run_instructions() -> RegisterCycle:
    register_cycle = RegisterCycle()
    with open(f"../inputs/day_10.txt", "r") as input_file:
        for line in input_file.readlines():
            register_cycle.increment()
            line = line.strip()
            if line != "noop":
                register_cycle.increment()
                register_cycle.add_to_register(int(line.split(' ')[1]))
    return register_cycle


def part_1():
    register_cycle = run_instructions()
    print(register_cycle.summed_signals)


def part_2():
    register_cycle = run_instructions()
    print(register_cycle.output)


if __name__ == "__main__":
    part_1()
    part_2()
