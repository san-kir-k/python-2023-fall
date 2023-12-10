import argparse


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='simple nl'
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='filename'
    )
    args = parser.parse_args()
    
    ln: int = 1
    try:
        if not args.file:
            while True:
                line: str = input()
                print(f'     {ln}\t{line}')
                ln += 1
        else:
            with open(args.file, 'r') as f:
                for line in f:
                    print(f'     {ln}\t{line}', end='')
                    ln += 1
    except FileNotFoundError:
        print(f'nl: {args.file}: No such file or directory')
    except:
        pass
