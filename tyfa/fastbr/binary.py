#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bitarray import bitarray


class BinaryMatrix:
    def __init__(self, _n=0, _m=0):
        self.n = _n
        self.m = _m
        self.M = []
        for x in range(_m):
            self.M.append(bitarray('0' * _n))

    def print(self):
        for row in self.M:
            print(row)

    def gen_random(self):
        from random import getrandbits
        from random import seed
        seed(1)
        for i in range(self.m):
            cur = bin(getrandbits(self.n))[2:]
            if len(cur) < self.n:
                cur = '0' * (self.n - len(cur)) + cur
            self.M[i] = bitarray(cur)

    def load(self, _dir):
        f = open(_dir)
        lines = f.readlines()
        f.close()
        self.n = int(lines[0])
        self.m = int(lines[1])
        self.M = []
        for _ in range(self.m):
            self.M.append(bitarray('0' * self.n))
        for i in range(self.n):
            row = lines[i + 2].strip().replace(' ', '')
            for j in range(len(row)):
                self.M[j][i] = int(row[j])
        return self

    def load_bin(self, M):
        self.n = len(M)
        self.m = len(M[0])
        self.M = []
        for _ in range(self.m):
            self.M.append(bitarray('0' * self.n))
        for i in range(self.n):
            row = M[i]
            for j in range(len(row)):
                self.M[j][i] = int(row[j])
        return self

    def save(self, _dir):
        f = open(_dir, 'w')
        f.write(str(self.n) + '\n')
        f.write(str(self.m) + '\n')
        for x in self.M:
            f.write(x.to01() + '\n')
        f.close()

    def col(self, _i):
        return self.M[_i]

    def row(self, _i):
        a = bitarray()
        for x in range(self.m):
            a.append(self.M[x][_i])
        return a

    def swap_cols(self, _i, _j):
        assert (_i < self.m and _j < self.m)
        self.M[_i], self.M[_j] = self.M[_j], self.M[_i]

    def swap_rows(self, _i, _j):
        assert (_i < self.n and _j < self.n)
        for x in range(self.m):
            self.M[x][_i], self.M[x][_j] = self.M[x][_j], self.M[x][_i]

    def drop_col(self, _i):
        assert (_i < self.m and self.m > 0)
        self.m -= 1
        del self.M[_i]

    def drop_row(self, _i):
        assert (_i < self.n)
        self.n -= 1
        for x in range(self.m):
            del self.M[x][_i]


class BasicMatrix(BinaryMatrix):
    def __init__(self, _n=0, _m=0):
        BinaryMatrix.__init__(self, _n, _m)

    def _is_sub_row(self, _i, _j):
        fi = self.row(_i)
        fj = self.row(_j)
        if fi & fj == fi:
            return True
        else:
            return False

    def create_basic_matrix(self):
        srows = set([])
        drows = []
        for _j in range(self.n):
            for _i in range(_j + 1, self.n):
                if self.row(_i) == self.row(_j):
                    drows.append(_j)
                    break
        drows = list(reversed(drows))
        for fil in drows:
            self.drop_row(fil)

        for _j in range(self.n):
            for _i in range(self.n):
                if _i != _j and self._is_sub_row(_i, _j):
                    srows.add(_j)
                    break
        srows = list(reversed(sorted(srows)))
        for x in srows:
            self.drop_row(x)


class BasicMatrixBR(BasicMatrix):
    def __init__(self, _n=0, _m=0):
        BasicMatrix.__init__(self, _n, _m)
        self.grouped = {}
        self.orig = {}

    def compare_rows(self, _i, _j):
        fila_i = self.row(_i)
        fila_j = self.row(_j)
        f1 = fila_i.count()
        f2 = fila_j.count()
        if f1 < f2:
            return -1
        elif f1 > f2:
            return 1
        else:
            c1, c2 = 0, 0
            for x in range(self.m):
                if fila_i[x] == True:
                    c1 += self.col(x).count()
                if fila_j[x] == True:
                    c2 += self.col(x).count()
            if c1 > c2:
                return -1
            elif c1 < c2:
                return 1
        return 0

    def compare_cols(self, _i, _j):
        ci, cj = 0, 0
        # fila_0=self.obtenerFila(0)
        if self.M[_i][0] == True:
            ci = 1
        if self.M[_j][0] == True:
            cj = 1
        if ci > cj:
            return 1
        elif ci < cj:
            return -1
        elif self.col(_i).count() > self.col(_j).count():
            return 1
        elif self.col(_i).count() < self.col(_j).count():
            return -1
        else:
            return 0

    def _sort_rows(self):
        for x in range(self.n):
            for y in range(x + 1, self.n):
                if self.compare_rows(x, y) == 1:
                    self.swap_rows(y, x)

    def _sort_cols(self):
        for x in range(self.m):
            for y in range(x + 1, self.m):
                if self.compare_cols(x, y) == -1:
                    self.swap_cols(y, x)
                    self.orig[x], self.orig[y] = self.orig[y], self.orig[x]

    def preprocess(self):
        self._sort_rows()
        for i in range(self.m):
            self.orig[i] = i
        self._sort_cols()
        self.groups_cols()

    def groups_cols(self):
        d = {}
        do = {}
        rr = 0
        for x in range(self.m - 1, -1, -1):
            col = ''.join(['1' if i == 1 else '0' for i in self.col(x)])  # fix for pypy3
            # col = self.col(x).to01()
            # print col
            if col in d:
                d[col].append(x)
                self.drop_col(x)
            else:
                d[col] = [x]
                do[col] = rr
                rr += 1
        # print(d)
        self.grouped = dict([(len(d) - do[k] - 1, [self.orig[o] for o in x]) for k, x in d.items()])
        # print(self.grouped)


class TestorsBR():
    def __init__(self, _mat, _debug=False):
        self.mat = _mat

        self.debug = _debug

    def reduce_cols(self):
        self.mat.groups_cols()

    def sort_row_col(self):
        self.mat.sort_matrix()

    def mascaraDeAceptacion(self, listaDeRasgos):
        ma = bitarray('0' * self.mat.n)
        for x in listaDeRasgos:
            ma |= self.mat.M[x]
        return ma

    def _mascaraDeAceptacion(self, _mascara, _rasgo):
        return _mascara | self.mat.M[_rasgo]

    def mascaraDeCompatibilidad(self, listaDeRasgos):
        ma = bitarray('0' * self.mat.n)
        mc = bitarray('0' * self.mat.n)
        for x in listaDeRasgos:
            mc = (mc & ~self.mat.M[x]) | (
                    ~ma & self.mat.M[x])
            ma |= self.mat.M[x]
        return mc

    def _mascaraDeCompatibilidad(self, _mascara_a, _mascara_c, _rasgo):
        c_rasgo = self.mat.M[_rasgo]
        return (_mascara_c & ~c_rasgo) | (~_mascara_a & c_rasgo)

    def _rasgoExcluyente(self, _rasgo, L):
        assert (_rasgo not in L)
        ma_l = self.mascaraDeAceptacion(L)
        ma_l_rasgo = self._mascaraDeAceptacion(ma_l, _rasgo)
        ma_c_l_rasgo = self.mascaraDeCompatibilidad(L + [_rasgo])
        if ma_l == ma_l_rasgo:  # No aporta filas tipicas
            return True
        tupla_0 = bitarray('0' * self.mat.n)
        for l_rasgo in L:
            tuplabinaria = self.mat.M[l_rasgo]
            if ma_c_l_rasgo & tuplabinaria == tupla_0:
                return True
        return False

    def noExcluyenteMasTestores(self, _lista, L):
        no_excl, testores = [], []
        ma_l = self.mascaraDeAceptacion(L)
        mc_l = self.mascaraDeCompatibilidad(L)
        tupla_0 = bitarray('0' * self.mat.n)
        tupla_1 = bitarray('1' * self.mat.n)
        for x in _lista:
            assert (x not in L)
            ma_l_rasgo = self._mascaraDeAceptacion(ma_l, x)
            # No es testor y no aporta ninguna fila
            condicion1 = (ma_l == ma_l_rasgo)  # El rasgo es excluyente
            # Le quita la tipicida a alguna fila.
            condicion2 = False
            mc_c_l_X = self._mascaraDeCompatibilidad(ma_l, mc_l, x)
            for rasgo in L:
                mc_X = self.mat.M[rasgo]
                d = mc_c_l_X & mc_X
                if mc_c_l_X & mc_X == tupla_0:
                    condicion2 = True
                    break
                    # No forman ningun testor
            condicion3 = (ma_l_rasgo != tupla_1)
            if not (condicion1 or condicion2):
                if condicion3:
                    no_excl.append(x)
                else:
                    testores.append(L + [x])
        return no_excl, testores

    # Simple Brute Recursive algorithm
    def brec(self, ift, cft, cur, ttr):
        if cur.count() == self.mat.n:
            # we have a testor, remains to check if typical
            left = [bitarray('0' * self.mat.n)]
            n = len(cft)
            for i in range(1, n):
                left.append(left[i - 1] | self.mat.M[cft[i - 1]])
            right = bitarray('0' * self.mat.n)
            for i in range(n, 0, -1):
                if (left[i - 1] | right).count() == self.mat.n:
                    return
                right = right | self.mat.M[cft[i - 1]]
            # print(cft, cur, self.mat.n)
            ttr.append(cft[:])
        else:
            if ift == self.mat.m:  # finished search
                return
            if len(cft) == 0 and not self.mat.M[ift][0]:  # ordered columns warranty this cut
                return

            self.brec(ift + 1, cft, cur, ttr)
            cft.append(ift)
            self.brec(ift + 1, cft, cur | self.mat.M[ift], ttr)
            cft.pop()

    # recursive fast br algorithm
    def frec(self, toadd, cft, ttr):
        self.analyzed_sets += 1
        if len(toadd) == 0: return 1
        ift = toadd[-1]
        if len(cft) == 0:
            # ordered columns cut
            if self.mat.M[ift][0] is False:
                return 0
            # typical testor of one feature
            if self.mat.M[ift].count() == self.mat.n:
                ttr.append([ift])
                toadd.pop()
                self.frec(toadd, cft, ttr)
                return 0
        toadd.pop()
        cft.append(ift)
        ntoadd, tts = self.noExcluyenteMasTestores(toadd, cft)
        ttr += tts
        ret = self.frec(ntoadd, cft, ttr)
        cft.pop()
        # hole cut
        if ret == len(toadd) + 1:
            if self.debug: self.cuts += 1
            return ret + 1
        self.frec(toadd, cft, ttr)
        return 0

    def cal_pseudotestors(self):
        self.mat.preprocess()
        ttr = []
        # self.brec(0, [], bitarray('0' * self.mat.n), ttr)
        if self.debug: self.cuts = 0
        self.frec([self.mat.m - 1 - i for i in range(self.mat.m)], [], ttr)
        if self.debug: print(self.cuts)

        mm = sorted([i for i in self.mat.grouped.keys()])
        self.ttr = []
        for t in ttr:
            self.ttr.append([mm[i] for i in t])
        if self.debug: print(self.ttr)

    def expand_pseudotestors(self):
        if self.debug: print(self.mat.grouped)
        self.ttr = [[self.mat.grouped[i][0] for i in t] for t in self.ttr]
        for key in self.mat.grouped.keys():
            if len(self.mat.grouped[key]) <= 1: continue
            for k in self.mat.grouped[key][1:]:
                for t in self.ttr:
                    if self.mat.grouped[key][0] in t:
                        nt = list(t)
                        i = nt.index(self.mat.grouped[key][0])
                        nt[i] = k
                        self.ttr.append(nt)

    def cal_typical_testors(self):
        self.analyzed_sets = 0
        self.cal_pseudotestors()
        self.expand_pseudotestors()
        return self.ttr




def main(args):
    bb = BasicMatrixBR(10, 10)
    bb.gen_random()
    print(bb.M)
    bb.create_basic_matrix()
    print(bb.M)
    tt_br = TestorsBR(bb, True)
    tts = tt_br.cal_typical_testors()
    print(tts)
    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
