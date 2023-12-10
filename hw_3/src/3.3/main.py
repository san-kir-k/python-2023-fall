import numpy as np
from typing import List
from functools import reduce, lru_cache


class HashMixin:
    def __eq__(self, other: 'Matrix') -> bool:
        return self._data == other._data

    def __neq__(self, other: 'Matrix') -> bool:
        return self._data != other._data

    def __hash__(self) -> int:
        """Hash function for 2D List that lies in Matrix

        Simple non-constant hash function that just calculate
        aggregative xor of all elements in 2D List.

        Returns:
            int: result of hash function
        """
        reduced_rows: List[int] = [reduce(lambda acc, v: acc ^ int(v), row, 0) for row in self._data]
        return reduce(lambda acc, v: acc ^ v, reduced_rows, 0)


class Matrix(HashMixin):
    def __init__(self, data: List[List]) -> None:
        if not (isinstance(data, list) and reduce(lambda acc, v: acc and isinstance(v, list), data, True)):
            raise ValueError("Initial data shoud be 2D List")

        self._rows: int = len(data)
        self._cols: int = len(data[0])
        self._data: List[List] = data

    def __str__(self) -> str:
        return '\n'.join('\t'.join(str(cell) for cell in row) for row in self._data)

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Matrix dimensions are not compatible for addition: ({self.rows}, {self.cols}) and ({other.rows}, {other.cols})"
            )

        result_data: List[List] = [
            [
                self._data[row][col] + other._data[row][col]
                for col in range(self.cols)
            ]
            for row in range(self.rows)
        ]
        return Matrix(result_data)

    def __mul__(self, other: 'Matrix') -> 'Matrix':
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError(
                f"Matrix dimensions are not compatible for per-element multiplication: ({self.rows}, {self.cols}) and ({other.rows}, {other.cols})"
            )

        result_data: List[List] = [
            [
                self._data[row][col] * other._data[row][col]
                for col in range(self.cols)
            ]
            for row in range(self.rows)
        ]
        return Matrix(result_data)

    @lru_cache(maxsize=None)
    def __matmul__(self, other: 'Matrix') -> 'Matrix':
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                raise ValueError(
                    f"Matrix dimensions are not compatible for matrix multiplication: ({self.rows}, {self.cols}) and ({other.rows}, {other.cols})"
                )
            result_data: List[List] = [
                [
                    sum(self._data[row][k] * other._data[k][col] for k in range(self.cols))
                    for col in range(other.cols)
                ]
                for row in range(self.rows)
            ]
            return Matrix(result_data)
        else:
            raise TypeError("Unsupported operand type for multiplication, should be Matrix.")

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    def tolist(self) -> List[List]:
        return self._data


if __name__ == "__main__":
    A: Matrix = Matrix(
        [[2, 2, 2, 2],
         [2, 2, 2, 2],
         [2, 2, 2, 2],
         [2, 2, 2, 2],]
    )
    B: Matrix = Matrix(
        [[2, 0, 0, 0],
         [0, 2, 0, 0],
         [0, 0, 2, 0],
         [0, 0, 0, 2],]
    )
    C: Matrix = Matrix(
        [[2, 3, 2, 3],
         [2, 3, 2, 3],
         [2, 3, 2, 3],
         [2, 3, 2, 3],]
    )
    D: Matrix = Matrix(
        [[2, 0, 0, 0],
         [0, 2, 0, 0],
         [0, 0, 2, 0],
         [0, 0, 0, 2],]
    )
    
    # Требование из условия
    assert((hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D))
    
    with open('../../artifacts/3.3/AB.txt', 'w') as output:
        res: Matrix = A @ B
        output.write(str(res))
    
    with open('../../artifacts/3.3/CD.txt', 'w') as output:
        res: Matrix = C @ D
        output.write(str(res))

    with open('../../artifacts/3.3/hash.txt', 'w') as output:
        output.write(f'{hash(A @ B)}\n{hash(C @ D)}\n')
