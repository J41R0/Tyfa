from Tyfa.fastbr.binary import BasicMatrixBR, TestorsBR


def find_tt(mb):
    my_bm = BasicMatrixBR()
    my_bm.load_bin(mb)
    tt_br = TestorsBR(my_bm)
    tts = tt_br.cal_typical_testors()
    return tt_br.analyzed_sets, tts
