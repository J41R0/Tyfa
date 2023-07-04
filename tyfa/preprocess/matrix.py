from enum import Enum

import numpy as np
from numba import njit


@njit
def _find_relation(vector_a, vector_b) -> int:
    if len(vector_a) != len(vector_b):
        raise ValueError('Vectors must have the same length to be compared')
    last_relation = 0
    for i in range(len(vector_a)):
        if vector_a[i] > vector_b[i]:
            current_relation = 2
        elif vector_a[i] < vector_b[i]:
            current_relation = 3
        else:  # vector_a[i] == vector_b[i]
            current_relation = 1
        if (last_relation == 0
                or last_relation == 1):
            last_relation = current_relation
        elif current_relation != 1:
            if current_relation != last_relation:
                return 0
    if last_relation == 1:
        return 3
    return last_relation


class BasicMatrix:
    class Relation(Enum):
        NON_RELATION = 0
        EQUAL_RELATION = 1
        SUPER_RELATION = 2
        SUB_RELATION = 3

    def __init__(self):
        self._row_matrix = None
        self._col_matrix = None
        self._shape = None

    @staticmethod
    @njit
    def rm_sub_rows(matrix, new_row):
        mask = np.zeros((len(matrix)), dtype=np.int32) == 0
        for row_pos in range(len(matrix)):
            if _find_relation(matrix[row_pos], new_row) == 3:
                mask[row_pos] = False
        return matrix[mask]

    def add_row(self, new_row):
        if self._row_matrix is None or len(self._row_matrix) == 0:
            self._row_matrix = np.atleast_2d(new_row)
        else:
            self._row_matrix = BasicMatrix.rm_sub_rows(self._row_matrix, new_row)
            self._row_matrix = np.vstack((self._row_matrix, new_row))

    @staticmethod
    def get_relation(vector_a, vector_b) -> Relation:
        return BasicMatrix.Relation(_find_relation(vector_a, vector_b))

    @classmethod
    def from_row_list(cls, rows_mb):
        self = cls()
        first_row_len = len(rows_mb[0])
        for row in rows_mb:
            if len(row) != first_row_len:
                raise Exception('All rows must have the same length')
        list_mb = []
        for row in rows_mb:
            new_row = []
            for elem in row:
                if elem:
                    new_row.append(1)
                else:
                    new_row.append(0)
            list_mb.append(new_row)
        input_matrix = np.asarray(list_mb)
        for row in input_matrix:
            self.add_row(row)
        self._col_matrix = self._row_matrix.T
        self._shape = self._row_matrix.shape
        return self
