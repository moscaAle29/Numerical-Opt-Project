 #!/usr/bin/python3
import numpy as np


class Grid():
    def __init__(self, n_rows, n_cols):
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.disposition = np.zeros(
            (self.n_rows, self.n_cols),
            dtype=np.int16
        )

    def _move(self, col1, col2):
        parcel = self._take(col1) 
        self._locate(parcel, col=col2)

    def _take(self, col):
        # take the forst element of the col
        for row in range(0, self.n_rows):
            if self.disposition[row, col] != 0:
                parcel_idx = self.disposition[row, col]
                # set zero
                self.disposition[row, col] = 0
                # return it 
                return parcel_idx
        # the column is void, return 0
        return 0

    def _locate(self, parcel_idx, col):
        for row in range(self.n_rows - 1, -1, -1):
            # if the position is free
            if self.disposition[row, col] == 0:
                # insert the parcel there
                self.disposition[row, col] = parcel_idx
                return
        # the column is full, it is not possible to store it
        raise ValueError('Column is full')
