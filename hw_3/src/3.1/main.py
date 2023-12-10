import numpy as np
from typing import List
from functools import reduce


class Matrix:
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
    np_lhs: np.ndarray = np.random.randint(0, 10, (10, 10))
    np_rhs: np.ndarray = np.random.randint(0, 10, (10, 10))

    lhs: Matrix = Matrix(np_lhs.tolist())
    rhs: Matrix = Matrix(np_rhs.tolist())
    
    with open('../../artifacts/3.1/matrix+.txt', 'w') as output:
        np_res: np.ndarray = np_lhs + np_rhs
        res: Matrix = lhs + rhs
        assert (np_res.tolist() == res.tolist())
        output.write(str(res))
    
    with open('../../artifacts/3.1/matrix*.txt', 'w') as output:
        np_res: np.ndarray = np_lhs * np_rhs
        res: Matrix = lhs * rhs
        assert (np_res.tolist() == res.tolist())
        output.write(str(res))

    with open('../../artifacts/3.1/matrix@.txt', 'w') as output:
        np_res: np.ndarray = np_lhs @ np_rhs
        res: Matrix = lhs @ rhs
        assert (np_res.tolist() == res.tolist())
        output.write(str(res))
