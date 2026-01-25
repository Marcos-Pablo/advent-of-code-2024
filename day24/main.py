from collections import defaultdict, deque
from pathlib import Path
import time
import tracemalloc


def extract_wires_and_gates():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    wires = {}
    out_to_gate = {}
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
        return wires, gates, out_to_gate


def process_instructions(wires, gates):
    while gates:
        gate = gates.popleft()
        if wires.get(gate["wire_a"]) == None or wires.get(gate["wire_b"]) == None:
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


def build_gate_lookup(out_to_gate):
    gate_lookup = {}
    for out, (op, a, b) in out_to_gate.items():
        gate_lookup[(op, frozenset({a, b}))] = out
    return gate_lookup


def build_fanout(gate_lookup):
    fanout = defaultdict(list)

    for (op, inputs), out in gate_lookup.items():
        a, b = tuple(inputs)
        fanout[a].append((op, b, out))
        fanout[b].append((op, a, out))

    return fanout


def find_partner_of_carry(fanout, carry_label):
    """
    For a given carry wire C, find a wire W such that:
      C XOR W -> ...
      C AND W -> ...
    That W is the 'propagate partner' being used with the carry.
    """
    xor_partners = {}
    and_partners = {}
    for op, other, out in fanout.get(carry_label, []):
        if op == "XOR":
            xor_partners[other] = out
        elif op == "AND":
            and_partners[other] = out

    # pick a wire that appears in BOTH XOR and AND with the carry
    for w in xor_partners:
        if w in and_partners:
            return w, xor_partners[w], and_partners[w]

    return None, None, None


def find_swapped_wires(out_to_gate, gate_lookup):
    LEFT = 25
    swapped_wires = []

    def p(label, value=""):
        print(f"{label:<{LEFT}}= {value}")

    def lookup(op, a, b):
        return gate_lookup.get((op, frozenset({a, b})))

    def rebuild_indices():
        nonlocal gate_lookup, fanout
        gate_lookup = build_gate_lookup(out_to_gate)
        fanout = build_fanout(gate_lookup)

    fanout = build_fanout(gate_lookup)

    carry_in = lookup("AND", "x00", "y00")
    if carry_in is None:
        raise ValueError("Couldn't find carry1 = AND(x00,y00).")

    print()
    z0 = out_to_gate["z00"]
    p("z00", z0)

    for i in range(1, 45):
        print()
        z_index = f"z{i:02d}"
        z = out_to_gate[z_index]
        p(z_index, z)

        t = lookup("XOR", f"x{i:02d}", f"y{i:02d}")
        if t is None:
            raise ValueError(f"Couldn't find t{i} = XOR(x{i:02d}, y{i:02d}).")

        expected_sum = lookup("XOR", t, carry_in)

        if expected_sum is None:
            p("!!!", f"missing gate: XOR({t}, {carry_in})")

            used_t, used_sum_out, used_and_out = find_partner_of_carry(fanout, carry_in)

            if used_t is None:
                p("!!!", f"couldn't find XOR+AND partner for carry {carry_in}")
                break

            p(
                "carry pairs with",
                f"{used_t} (XOR-> {used_sum_out}, AND-> {used_and_out})",
            )
            p("expected t", t)

            if used_t != t:
                swapped_wires.extend([used_t, t])
                out_to_gate[used_t], out_to_gate[t] = (
                    out_to_gate[t],
                    out_to_gate[used_t],
                )
                rebuild_indices()

                t = lookup("XOR", f"x{i:02d}", f"y{i:02d}")
                expected_sum = lookup("XOR", t, carry_in)
                if expected_sum is None:
                    p("!!!", "still missing XOR(t, carry) after swap; stopping")
                    break
            else:
                p(
                    "!!!",
                    "unexpected: carry pairs with expected t but XOR key missing; stopping",
                )
                break

        if expected_sum != z_index:
            p("!!!", f"swap evidence: {z_index} should be {expected_sum}")
            swapped_wires.extend([z_index, expected_sum])

            out_to_gate[z_index], out_to_gate[expected_sum] = (
                out_to_gate[expected_sum],
                out_to_gate[z_index],
            )
            rebuild_indices()

            z = out_to_gate[z_index]
            p(f"{expected_sum} (was sum{i})", out_to_gate.get(expected_sum))
            p(f"{z_index} (fixed)", z)

        op, A, B = out_to_gate[z_index]
        if op == "XOR" and (A == t or B == t):
            carry_seen = B if A == t else A
            p(f"{t} (t{i})", out_to_gate.get(t))
            p(f"{carry_seen} (carry{i})", out_to_gate.get(carry_seen))
        else:
            p("note", "z_i label fixed, but inputs don't display as (t, carry) cleanly")

        g = lookup("AND", f"x{i:02d}", f"y{i:02d}")
        if g is None:
            raise ValueError(f"Couldn't find g{i} = AND(x{i:02d}, y{i:02d}).")

        p_term = lookup("AND", t, carry_in)
        if p_term is None:
            p("!!!", f"missing gate: AND({t}, {carry_in})")

            used_t, used_sum_out, used_and_out = find_partner_of_carry(fanout, carry_in)
            if used_t is not None and used_t != t:
                swapped_wires.extend([used_t, t])
                out_to_gate[used_t], out_to_gate[t] = (
                    out_to_gate[t],
                    out_to_gate[used_t],
                )
                rebuild_indices()

                t = lookup("XOR", f"x{i:02d}", f"y{i:02d}")
                p_term = lookup("AND", t, carry_in)

            if p_term is None:
                p("!!!", "still missing AND(t, carry); stopping")
                break

        carry_out = lookup("OR", g, p_term)
        if carry_out is None:
            p("!!!", f"missing gate: OR({g}, {p_term}); stopping")
            break

        carry_in = carry_out

    print()
    p("z45", out_to_gate.get("z45"))

    return ",".join(sorted(swapped_wires))


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    wires, gates, out_to_gate = extract_wires_and_gates()
    gate_lookup = build_gate_lookup(out_to_gate)

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
