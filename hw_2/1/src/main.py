from typing import List, Any
from functools import reduce


def generate_latex_table(content: List[List[Any]]) -> str:
    header: str = "\\documentclass{article}\n\\usepackage{tabularx}\n\\begin{document}\n"
    footer: str = "\\end{document}\n"

    if len(content) == 0:
        return header + footer

    columns_fmt: str = '| X ' * len(content[0]) + '|'
    table_rows: str = map(lambda row: ' & '.join(map(str, row)) + ' \\\\\n', content)
    table_content: str = reduce(lambda acc, row: acc + row + ' \\hline\n', table_rows, ' \\hline\n')
    table: str = f"\\begin{{tabularx}}{{\\textwidth}} {{{columns_fmt}}}\n"
    table += table_content
    table += "\end{tabularx}\n"
    
    return header + table + footer


if __name__ == "__main__":
    content = [
        [11, 12, 13, 14],
        [21, 22, 23, 24],
        [31, 32, 33, 34],
    ]

    with open("../artifacts/table.tex", "w") as output:
        output.write(generate_latex_table(content))
