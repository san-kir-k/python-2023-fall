import argparse


def refresh_stats(line: str, stat: dict):
    stat['lines'] += 1
    stat['words'] += len(line.split())
    for letter in line:
        stat['bytes'] += len(letter.encode('utf8'))


def print_stats(stat: dict, name: str = ''):
    print(f"{stat['lines']:>8}{stat['words']:>8}{stat['bytes']:>8} {name}")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='simple wc'
    )
    parser.add_argument(
        'files',
        nargs='*',
        help='filename(s)'
    )
    args = parser.parse_args()

    if not args.files:
        statistic: dict = {'lines': 0, 'words': 0, 'bytes': 0}
        try:
            while True:
                line: str = input()
                line += '\n'
                refresh_stats(line, statistic)
        except:
            print_stats(statistic)
    else:
        total_stat: dict = {'lines': 0, 'words': 0, 'bytes': 0}
        for f in args.files:
            statistic: dict = {'lines': 0, 'words': 0, 'bytes': 0}
            try:
                with open(f, 'r') as input:
                    for line in input:
                        refresh_stats(line, statistic)
                print_stats(statistic, f)
                total_stat['lines'] += statistic['lines']
                total_stat['words'] += statistic['words']
                total_stat['bytes'] += statistic['bytes']
            except FileNotFoundError:
                print(f'wc: {f}: open: No such file or directory')
        if len(args.files) > 1:
            print_stats(total_stat, 'total')