from pathlib import Path
import time
import tracemalloc


def extract_secrets():
    script_dir = Path(__file__).parent
    input_path = script_dir / "input.txt"
    with open(input_path.resolve(), "r") as file:
        codes = map(int, file.read().splitlines())
        return codes


def mix(secret, val):
    return secret ^ val


def prune(num):
    return num % 16777216


def get_next_secret(secret):
    def first_step(secret):
        val = secret * 64
        secret = mix(secret, val)
        secret = prune(secret)
        return secret

    def second_step(secret):
        val = secret // 32
        secret = mix(secret, val)
        secret = prune(secret)
        return secret

    def third_step(secret):
        val = secret * 2048
        secret = mix(secret, val)
        secret = prune(secret)
        return secret

    secret = first_step(secret)
    secret = second_step(secret)
    secret = third_step(secret)
    return secret


def main():
    print("Processing input...")
    tracemalloc.start()
    start = time.perf_counter()

    secrets = extract_secrets()

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")

    tracemalloc.start()
    start = time.perf_counter()

    secrets_sum = 0
    for secret in secrets:
        next_secret = secret
        for _ in range(2000):
            next_secret = get_next_secret(next_secret)
        secrets_sum += next_secret

    print(f"Response part 1: {secrets_sum}")
    print(f"Response part 2: ")

    end = time.perf_counter()
    current, peak = tracemalloc.get_traced_memory()
    print(f"Elapsed time: {end - start: .6f} second(s)")
    print(
        f"Current memory usage: {current / 10**6:.6f} MB; Peak was {peak / 10**6:.6f} MB"
    )
    print("==================================")


main()
