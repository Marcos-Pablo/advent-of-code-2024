from collections import defaultdict, deque
from pathlib import Path
import time
import tracemalloc


def extract_wires_and_gates1():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    wires: dict[str, int | None] = defaultdict(lambda: None)
    out_to_gate: dict[str, tuple | None] = defaultdict(lambda: None)
    gate_lookup: dict[tuple, str | None] = defaultdict(lambda: None)
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

            out_to_gate[output_wire] = (operator, wire_a, wire_b)
            gate_lookup[(operator, frozenset({wire_a, wire_b}))] = output_wire
        return wires, gates, out_to_gate, gate_lookup


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


def find_swapped_wires(out_to_gate, gate_lookup):
    LEFT = 25
    swapped_wires = []

    def p(label, value=""):
        print(f"{label:<{LEFT}}= {value}")

    def is_xor_xy(w, i):
        if w not in out_to_gate:
            return False
        op, a, b = out_to_gate[w]
        return op == "XOR" and {a, b} == {f"x{i:02d}", f"y{i:02d}"}

    prev_t, prev_c = None, None
    fanout = defaultdict(list)  # wire -> list of (op, other_wire, out_wire)

    for (op, inputs), out in gate_lookup.items():
        a, b = tuple(inputs)
        fanout[a].append((op, b, out))
        fanout[b].append((op, a, out))

    for i in range(45):
        print()
        z_index = f"z{i:02d}"
        z = out_to_gate[z_index]

        p(z_index, z)
        if i == 0:
            continue

        op, A, B = z[0], z[1], z[2]

        if is_xor_xy(A, i):
            t_label, carry_label = A, B
        elif is_xor_xy(B, i):
            t_label, carry_label = B, A
        else:
            p("!!!", f"swap evidence: {z_index} isn't XOR(t{i}, carry{i})")
            t_candidate_label = gate_lookup[
                ("XOR", frozenset({f"x{i:02d}", f"y{i:02d}"}))
            ]
            t_candidate_wire = out_to_gate[t_candidate_label]
            p(f"{t_candidate_label} (candidate t{i})", t_candidate_wire)

            c1 = gate_lookup[("AND", frozenset({f"x{i - 1:02d}", f"y{i - 1:02d}"}))]
            c2 = gate_lookup.get(("AND", frozenset({prev_t, prev_c})))

            if c2 is None:
                p(
                    "!!!",
                    f"can't find AND(prev_t, prev_c) at bit {i}; prev labels likely swapped upstream",
                )

            candidate_carry_label = gate_lookup[("OR", frozenset({c1, c2}))]
            candidate_carry_wire = out_to_gate[candidate_carry_label]
            p(f"{candidate_carry_label} (candidate carry{i})", candidate_carry_wire)

            if candidate_carry_wire and candidate_carry_wire[0] != "AND":
                c1 = out_to_gate.get(candidate_carry_wire[1])
                c2 = out_to_gate.get(candidate_carry_wire[2])
                p(f"{candidate_carry_wire[1]}", c1)
                p(f"{candidate_carry_wire[2]}", c2)

            key = ("XOR", frozenset({t_candidate_label, candidate_carry_label}))
            actual_z_label = gate_lookup.get(key)
            if actual_z_label is None and z_index == "z39":
                p(
                    "!!!",
                    f"missing gate: XOR({t_candidate_label}, {candidate_carry_label})",
                )
                p("bng", out_to_gate["bng"])
                p("vbm", out_to_gate["vbm"])
                print()
                for op, other, out in fanout["fjp"]:
                    print(
                        "fjp",
                        op,
                        other,
                        "->",
                        out,
                        " | other gate:",
                        out_to_gate.get(other),
                    )

                for op, other, out in fanout["hsf"]:
                    if op in ("XOR", "AND"):
                        print(
                            "hsf",
                            op,
                            other,
                            "->",
                            out,
                            " other=",
                            out_to_gate.get(other),
                        )

                swapped_wires.append("fjp")
                swapped_wires.append("bng")

                continue

            actual_z_wire = out_to_gate[actual_z_label]
            swapped_wires.append(z_index)
            swapped_wires.append(actual_z_label)

            p(f"{actual_z_label} (original z{i:02}) ", actual_z_wire)
            continue

        prev_t = t_label
        prev_c = carry_label
        t_wire = out_to_gate.get(t_label)
        carry_wire = out_to_gate.get(carry_label)

        p(f"{t_label} (t{i})", t_wire)
        p(f"{carry_label} (carry{i})", carry_wire)

        if carry_wire and carry_wire[0] != "AND":
            c1 = out_to_gate.get(carry_wire[1])
            c2 = out_to_gate.get(carry_wire[2])
            p(f"{carry_wire[1]}", c1)
            p(f"{carry_wire[2]}", c2)
    print()
    return ",".join(sorted(swapped_wires))


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    wires, gates, out_to_gate, gate_lookup = extract_wires_and_gates1()

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

    swapped_wires = find_swapped_wires(out_to_gate, gate_lookup)

    print(f"Response part 2: {swapped_wires}")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
