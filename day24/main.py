from collections import defaultdict, deque
from pathlib import Path
import time
import tracemalloc


def extract_wires_and_gates():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    wires: dict[str, int | None] = defaultdict(lambda: None)
    gates = deque()
    with open(input_path.resolve(), "r") as file:
        initial_values, gate_lines = file.read().split("\n\n")
        for line in initial_values.splitlines():
            wire, value = line.split(": ")
            wires[wire] = int(value)

        for line in gate_lines.splitlines():
            input, output = line.split("->")
            wire_a, operator, wire_b = input.strip().split(" ")
            output_wire = output.strip()

            gates.append(
                {
                    "wire_a": wire_a,
                    "wire_b": wire_b,
                    "operator": operator,
                    "output_wire": output_wire,
                }
            )
        return wires, gates


def process_instructions(wires, gates):
    while gates:
        gate = gates.popleft()
        if wires[gate["wire_a"]] == None or wires[gate["wire_b"]] == None:
            gates.append(gate)
            continue

        match gate["operator"]:
            case "AND":
                wires[gate["output_wire"]] = (
                    wires[gate["wire_a"]] & wires[gate["wire_b"]]
                )
            case "OR":
                wires[gate["output_wire"]] = (
                    wires[gate["wire_a"]] | wires[gate["wire_b"]]
                )
            case "XOR":
                wires[gate["output_wire"]] = (
                    wires[gate["wire_a"]] ^ wires[gate["wire_b"]]
                )


def extract_z_values(wires):
    z_wires = {}
    for wire, val in wires.items():
        if wire.startswith("z"):
            z_wires[wire] = val
    sorted_items = sorted(z_wires.items(), reverse=True)
    binary_num = "".join(list(map(lambda item: str(item[1]), sorted_items)))
    num = int(binary_num, 2)
    return num


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    wires, gates = extract_wires_and_gates()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    process_instructions(wires, gates)
    num = extract_z_values(wires)

    print(f"Response part 1: {num}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    print(f"Response part 2: ")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
