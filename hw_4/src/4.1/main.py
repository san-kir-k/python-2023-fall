import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, wait, ALL_COMPLETED


def fib(n: int) -> int:    
    prev, curr = 0, 1
    for _ in range(n):
        prev, curr = curr, prev + curr
    return prev


if __name__ == "__main__":
    n: int = 200000

    start = time.time()
    for _ in range(10):
        fib(n)
    end = time.time()
    print(f'Synchronous run (10 times): {end - start}')

    with ThreadPoolExecutor(max_workers=10) as executor:
        start = time.time()
        futures = [executor.submit(fib, n) for _ in range(10)]
        wait(futures, return_when=ALL_COMPLETED)
        end = time.time()
        print(f'Multithreading run (10 threads, 10 times): {end - start}')

    with ProcessPoolExecutor(max_workers=10) as executor:
        start = time.time()
        futures = [executor.submit(fib, n) for _ in range(10)]
        wait(futures, return_when=ALL_COMPLETED)
        end = time.time()
        print(f'Multiprocessing run (10 processes, 10 times): {end - start}')    
