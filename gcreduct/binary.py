from bitarray import bitarray


class BinaryGCreduct:
    def __init__(self):
        self.bm = []
        self.__bm_by_col = []
        self.__cum_mask = []
        self.analyzed_sets = 0

    def load_bm(self, bm, sort=True):
        # loading basic matrix
        # init self.bm
        for _ in bm:
            self.bm.append(bitarray())

        # init self.__bm_by_col
        for _ in bm[0]:
            self.__bm_by_col.append(bitarray())

        if sort:
            min_ones = bm[0].count(1)
            pos = 0
            for cur_pos, cur_row in enumerate(bm):
                cur_row_ones = cur_row.count(1)
                if cur_row_ones < min_ones:
                    min_ones = cur_row_ones
                    pos = cur_pos

            # sort basic matrix values setting at first place the lest ones row
            new_firs = bm[pos]
            bm.pop(pos)
            bm.insert(0, new_firs)
            # grouping the first row ones columns at the begin of the row
            for curr_bit_pos, curr_bit_val in enumerate(bm[0]):
                if curr_bit_val:
                    for curr_row_pos, curr_row in enumerate(bm):
                        self.bm[curr_row_pos].insert(0, curr_row[curr_bit_pos])
                else:
                    for curr_row_pos, curr_row in enumerate(bm):
                        self.bm[curr_row_pos].append(curr_row[curr_bit_pos])
        else:
            self.bm = bm.copy()

        # define values for self.__bm_by_col
        for curr_row in self.bm:
            for col_pos in range(len(self.__bm_by_col)):
                self.__bm_by_col[col_pos].append(curr_row[col_pos])

    def find_tt(self):
        self.analyzed_sets = 0
        tt = []
        B = []
        c = 0
        done = False
        # create reduct mask
        reduct_mask = bitarray()
        for _ in self.__bm_by_col[0]:
            reduct_mask.append(True)

        while not done:
            contributes = False
            is_super_reduct = False
            is_reduct = False

            B_mask, B_union_c_mask = self.__update_cm(B, c)

            if B_mask != B_union_c_mask:
                contributes = True
                if B_union_c_mask == reduct_mask:
                    is_super_reduct = True
                    is_reduct = self.__exclusion(B, c)
                    if is_reduct:
                        self.__cum_mask.pop()
                        res = B.copy()
                        res.append(c)
                        tt.append(res)
            self.analyzed_sets += 1
            B, c, done = self.__candidate_generator(B, c, contributes, is_super_reduct, is_reduct)
        return tt

    def __update_cm(self, B, c):
        # update cumulative mask
        c_mask = self.__bm_by_col[c]
        if len(B) == 0:
            B_mask = bitarray()
            for _ in self.__bm_by_col[0]:
                B_mask.append(False)
        else:
            B_mask = self.__cum_mask[-1]
            # B_mask = B_mask_arr[-1]
        B_union_c_mask = B_mask | c_mask
        self.__cum_mask.append(B_union_c_mask)
        return B_mask, B_union_c_mask

    def __exclusion(self, B, c):
        # determine if B union {c} is a reduct
        # define temp values
        B_union_c = B.copy()
        B_union_c.append(c)
        exc_mask = bitarray()
        cum_mask = bitarray()
        for _ in self.__bm_by_col[0]:
            cum_mask.append(False)
            exc_mask.append(False)

        # calc exclusion mask
        for x in B_union_c:
            not_cum_mask = cum_mask.copy()
            not_cum_mask.invert()
            not_cum_mask_x = self.__bm_by_col[x].copy()
            not_cum_mask_x.invert()
            cum_mask_x = self.__bm_by_col[x].copy()

            exc_mask = (exc_mask & not_cum_mask_x) | (not_cum_mask & cum_mask_x)
            cum_mask = cum_mask | cum_mask_x

        reduct = True

        zero_mask = bitarray()
        for _ in self.__bm_by_col[0]:
            zero_mask.append(False)

        # evaluate exclusionarity
        for x in B:
            cum_mask_x = self.__bm_by_col[x].copy()
            if (exc_mask & cum_mask_x) == zero_mask:
                reduct = False
                break
        return reduct

    def __candidate_generator(self, B, c, contributes, is_super_reduct, is_reduct):
        done = False
        if c == len(self.bm[0]) - 1:
            if is_reduct or not is_super_reduct:
                self.__eliminate_gap(B)
            c = B[-1] + 1
            B.remove(B[-1])
            while len(B) < len(self.__cum_mask):
                self.__cum_mask.pop()
        else:
            if not contributes or is_super_reduct:
                c += 1
                if not is_reduct:
                    self.__cum_mask.pop()
            else:
                B.append(c)
                c += 1
        if len(B) == 0 and not self.__bm_by_col[c][0]:
            done = True
        return B, c, done

    def __eliminate_gap(self, B):
        last = len(self.bm[0]) - 1
        while B[-1] == last:
            last = B[-1]
            B.remove(last)
            self.__cum_mask.pop()
            if len(B) == 1:
                break
