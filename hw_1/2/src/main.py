import argparse
from collections import deque
from typing import TextIO, List


def get_last_ten_lines(file: TextIO):
    lines: List[str] = []
    start_seek_pos: int = 1

    while len(lines) < 10:
        try:
            file.seek(-start_seek_pos, 2)
        except IOError:
            file.seek(0)
            break
        finally:
            lines = list(file)
        
        start_seek_pos *= 2
            
    return lines[-10:]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='simple tail'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='filename(s)'
    )
    args = parser.parse_args()
    q = deque()

    if not args.files:
        try:
            while True:
                line: str = input()
                q.append(line)
                if len(q) > 10:
                    q.popleft()
        except:
            for line in q:
                print(line)
    else:
        for f in args.files:
            try:
                with open(f, 'r') as input:
                    q.extend(get_last_ten_lines(input))

                    if len(args.files) > 1:
                        print(f'==> {f} <==')

                    for line in q:
                        print(line, end='')
                    
                    if f is not args.files[-1]:
                        print()

                    q.clear()
            except FileNotFoundError:
                print(f'tail: {f}: No such file or directory')
