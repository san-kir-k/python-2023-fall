import multiprocessing, time, codecs, datetime, threading

plock = multiprocessing.Lock()

def process_A(queue, pipe_b):
    while True:
        message: str = queue.get()
        with plock:
            print(f'[A   ] : [{datetime.datetime.now()}] : String "{message}" received from main process')
        if message is None:
            pipe_b.send(None)
            break
        message_lower: str = message.lower()
        time.sleep(5)
        pipe_b.send(message_lower)
        with plock:
            print(f'[A   ] : [{datetime.datetime.now()}] : String "{message_lower}" sent to B process')


def process_B(pipe_a, pipe_main):
    while True:
        message_lower = pipe_a.recv()
        with plock:
            print(f'[B   ] : [{datetime.datetime.now()}] : String "{message_lower}" received from A process')
        if message_lower is None:
            break
        encoded_message = codecs.encode(message_lower, 'rot_13')
        pipe_main.send(encoded_message)
        with plock:
            print(f'[B   ] : [{datetime.datetime.now()}] : String "{encoded_message}" sent to main process')


def writer(pipe):
    while True:
        encoded_s = pipe.recv()
        with plock:
            print(f'[MAIN] : [{datetime.datetime.now()}] : Encodded string rceived: "{encoded_s}"')    

if __name__ == '__main__':
    queue = multiprocessing.Queue()
    pipe_ab_parent, pipe_ab_child = multiprocessing.Pipe()
    pipe_bm_parent, pipe_bm_child = multiprocessing.Pipe()

    process_a = multiprocessing.Process(target=process_A, args=(queue, pipe_ab_child))
    process_b = multiprocessing.Process(target=process_B, args=(pipe_ab_parent, pipe_bm_child))
    process_a.start()
    process_b.start()
    
    writer_t = threading.Thread(target=writer, args=(pipe_bm_parent,), daemon=True)
    writer_t.start()

    try:
        while True:
            s: str = input()
            queue.put(s)
    except:
        queue.put(None)
        process_a.join()
        process_b.join()
