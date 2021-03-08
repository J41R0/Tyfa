from Tyfa.gcreduct.binary import BinaryGCreduct


def find_tt(mb):
    finder = BinaryGCreduct()
    finder.load_bm(mb)
    tts = finder.find_tt()
    return finder.analyzed_sets, tts
