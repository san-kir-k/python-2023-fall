import numpy as np
from typing import List
from functools import reduce
from numpy.lib.mixins import NDArrayOperatorsMixin
from numbers import Number


class FileWriterMixin:
    def save(self, filename: str) -> None:
        with open(filename, 'w') as output:
            output.write(str(self))


class StringMixin:
    def __str__(self) -> str:
        return '\n'.join('\t'.join(str(cell) for cell in row) for row in self.data)


class GettersSettersMixin:
    @property
    def rows(self) -> int:
        return self._rows
    
    @rows.setter
    def rows(self, rows: int) -> None:
        self._rows = rows

    @property
    def cols(self) -> int:
        return self._cols

    @cols.setter
    def cols(self, cols: int) -> None:
        self._cols = cols

    @property
    def data(self) -> List[List]:
        return self._data

    @data.setter
    def data(self, data: List[List]) -> None:
        if not (isinstance(data, list) and reduce(lambda acc, v: acc and isinstance(v, list), data, True)):
            raise ValueError("Data shoud be 2D List")
        
        self._data = data


class Matrix(GettersSettersMixin, StringMixin, FileWriterMixin, NDArrayOperatorsMixin):
    def __init__(self, data: List[List]) -> None:
        self.data: List[List] = data
        self.rows: int = len(data)
        self.cols: int = len(data[0])

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        if method == '__call__':
            for input in inputs:
                if not isinstance(input, (Matrix, Number, np.ndarray,)):
                    return NotImplemented
            inputs = tuple(x.data if isinstance(x, Matrix) else x for x in inputs)
            result = getattr(ufunc, method)(*inputs, **kwargs)
            if isinstance(result, list):
                return Matrix(result)
            elif isinstance(result, np.ndarray):
                return Matrix(result.tolist())
            elif isinstance(result, Number):
                return result
            else:
                return NotImplemented
        else:
            return NotImplemented


if __name__ == "__main__":
    np_lhs: np.ndarray = np.random.randint(0, 10, (10, 10))
    np_rhs: np.ndarray = np.random.randint(0, 10, (10, 10))

    lhs: Matrix = Matrix(np_lhs.tolist())
    rhs: Matrix = Matrix(np_rhs.tolist())

    np_res_add: np.ndarray = np_lhs + np_rhs
    res_add: Matrix = lhs + rhs
    assert (np_res_add.tolist() == res_add.data)
    res_add.save('../../artifacts/3.2/matrix+.txt')

    np_res_mul: np.ndarray = np_lhs * np_rhs
    res_mul: Matrix = lhs * rhs
    assert (np_res_mul.tolist() == res_mul.data)
    res_mul.save('../../artifacts/3.2/matrix*.txt')

    np_res_mmul: np.ndarray = np_lhs @ np_rhs
    res_mmul: Matrix = lhs @ rhs
    assert (np_res_mmul.tolist() == res_mmul.data)
    res_mmul.save('../../artifacts/3.2/matrix@.txt')
