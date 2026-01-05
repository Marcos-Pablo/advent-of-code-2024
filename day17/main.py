from pathlib import Path
import time
import tracemalloc


class ChronoSpatialComputer:
    def __init__(self) -> None:
        self.current_instruction = 0
        self.extract_instructions_and_registers()
        self.output = []

    def extract_instructions_and_registers(self) -> None:
        script_dir = Path(__file__).parent
        input_path = script_dir / "input.txt"
        with open(input_path.resolve(), "r") as file:
            registers, program = file.read().split("\n\n")
            registers = registers.split("\n")
            self.register_a = int(registers[0].split(": ")[1])
            self.register_b = int(registers[1].split(": ")[1])
            self.register_c = int(registers[2].split(": ")[1])
            self.instructions = list(map(int, program.split(": ")[1].split(",")))

    def execute_program(self):
        count = 0
        while self.current_instruction + 1 < len(self.instructions):
            instruction, operand = self.get_next_instruction_and_operand()
            match instruction:
                case 0:
                    self.adv(operand)
                case 1:
                    self.bxl(operand)
                case 2:
                    self.bst(operand)
                case 3:
                    self.jnz(operand)
                case 4:
                    self.bxc(operand)
                case 5:
                    count += 1
                    self.out(operand)
                case 6:
                    self.bdv(operand)
                case 7:
                    self.cdv(operand)
        self.print_registers()
        print("count -> ", count)

    def get_combo_operand(self, operand: int) -> int:
        match operand:
            case 4:
                return self.register_a
            case 5:
                return self.register_b
            case 6:
                return self.register_c
            case _:
                return operand

    def get_next_instruction_and_operand(self):
        instruction = self.instructions[self.current_instruction]
        operand = self.instructions[self.current_instruction + 1]
        self.current_instruction += 2
        return instruction, operand

    def adv(self, operand):
        self.register_a >>= self.get_combo_operand(operand)

    def bxl(self, operand):
        self.register_b ^= operand

    def bst(self, operand):
        self.register_b = self.get_combo_operand(operand) & 0b111

    def jnz(self, operand):
        if self.register_a == 0:
            return
        self.current_instruction = operand

    def bxc(self, _):
        self.register_b ^= self.register_c

    def out(self, operand):
        self.output.append(self.get_combo_operand(operand) & 0b111)

    def bdv(self, operand):
        self.register_b = self.register_a >> self.get_combo_operand(operand)

    def cdv(self, operand):
        self.register_c = self.register_a >> self.get_combo_operand(operand)

    def get_output(self):
        return ",".join(map(str, self.output))

    def print_registers(self):
        print(f"register A -> {self.register_a}")
        print(f"register B -> {self.register_b}")
        print(f"register C -> {self.register_c}")


def simulate_program():
    a = 64196994
    b = 0
    c = 0
    output = []
    while True:
        b = (a & 7) ^ 1
        c = (a >> b) & 7
        b ^= 5
        b ^= c
        output.append(str(b))
        a >>= 3
        if not a:
            break
    print(",".join(output))


def simulate_example():
    a = 7
    output = []
    while True:
        a >>= 3
        output.append(str(a & 7))
        if not a:
            break
    print(",".join(output))
    reverse_example()


def reverse_example():
    a = 3
    for _ in range(4):
        a <<= 3


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()
    computer = ChronoSpatialComputer()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    start = time.perf_counter()
    computer.execute_program()
    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 1: {computer.get_output()}")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    start = time.perf_counter()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Response part 2: ")
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )

    print("==================================")
    simulate_program()
    simulate_example()


main()
