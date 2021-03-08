__author__ = 'Jairo & Humberto'


class BinaryYYC:
    def __init__(self):
        self.bm = []
        self.analyzed_sets = 0

    def load_mb(self, mb):
        def row_to_list(row_data):
            count = len(row_data)
            res = []
            for pos in range(count - 1, -1, -1):
                if row_data[pos] == 1:
                    res.append(count - 1 - pos)
            return res

        self.bm = []
        for curr_row in mb:
            self.bm.append(row_to_list(curr_row))

    def __find_compatible_set(self, t=set(), x=0, index_row=0):
        self.analyzed_sets += 1
        t_temp = t.copy()
        t_temp.add(x)

        ref_sm = []  # define ref_sm as the sub-matrix of BM defined by the columns of t UNION x, and the current read rows

        for row_bm in self.bm[0:index_row]:
            unitary_row = t_temp.intersection(row_bm)
            if len(unitary_row) == 1:
                ref_sm.append(unitary_row)

        if len(ref_sm) < len(t_temp):  # Condition1
            return False

        super_union = set()
        for current_row in ref_sm:
            super_union = super_union.union(current_row)

        if super_union != t_temp:  # Condition2
            return False

        return True

    def find_tt(self):
        """
            Compute the set of all typical testors of the basic matrix bm.
            :param bm: basic matrix, list of sets of integer numbers: bm = [{<row_1>}, ..., {<row_m>}]
            :return: list of sets of integers, set of of all typical testors of bm:
                     typical_testors = [{<tt_1>}, ..., {<tt_k>}]
            """
        self.analyzed_sets = 0
        if len(self.bm) == 0:
            return []
        row1 = self.bm[0]
        typical_testors = []

        # first row:
        l = list()
        for elem in row1:
            l.append(elem)
            typical_testors.append(set(l))
            l.clear()

        # each row of basic matrix bm, from second row to the last row
        index_row = 1
        while index_row < len(self.bm):
            row_i = self.bm[index_row]
            typical_testors_aux = []

            # each partial typical testor of typical_testors
            for curr_tt in typical_testors:
                if len(curr_tt.intersection(row_i)):  # this mean that it was found a value 1 in row_i in columns of
                    # curr_tt, this is, curr_tt is still a TT
                    typical_testors_aux.append(curr_tt)
                else:  # curr_tt is not typical testor
                    # each column of row_i, such as it is not member of
                    for elem in row_i:
                        if self.__find_compatible_set(curr_tt, elem, index_row + 1):
                            t_temp = curr_tt.copy()
                            t_temp.add(elem)
                            typical_testors_aux.append(t_temp)

            typical_testors = typical_testors_aux.copy()
            index_row += 1
        return typical_testors
