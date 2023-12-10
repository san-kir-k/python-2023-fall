import math, time, multiprocessing, datetime, logging
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
from threading import Lock


logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def integrate(f, a, b, *, n_jobs=1, n_iter=1000000):
    task_logs = []
    task_logs.append(f'Trying to integrate function with n_jobs={n_jobs}')

    step = (b - a) / n_iter
    iters_per_worker = n_iter // n_jobs
    lock = Lock()

    def worker(idx):
        with lock:
            task_logs.append(f'[{datetime.datetime.now()}] : Task {idx} started')
        partial_acc = 0
        for i in range(idx * iters_per_worker, min(n_iter, (idx + 1) * iters_per_worker)):
            partial_acc += f(a + i * step) * step
        return partial_acc

    with ThreadPoolExecutor(max_workers=n_jobs) as executor:
        futures = [executor.submit(worker, i) for i in range(n_jobs)]
        wait(futures, return_when=ALL_COMPLETED)
        task_logs.append(f'[{datetime.datetime.now()}] : All tasks done!')

    for log in task_logs:
        logger.info(log)

    return sum(future.result() for future in futures)


if __name__ == "__main__":
    for cpu_num in range(1, 2 * multiprocessing.cpu_count() + 1):
        start = time.time()
        result = integrate(math.cos, 0, math.pi / 2, n_jobs=cpu_num)
        end = time.time()
        logger.info(f"Result is {result}")
        logger.info(f'Total time n_jobs={cpu_num}: {end - start}\n')
