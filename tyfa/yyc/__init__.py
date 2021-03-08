from tyfa.yyc.binary import BinaryYYC


def find_tt(mb):
    finder = BinaryYYC()
    finder.load_mb(mb)
    tts = finder.find_tt()
    return finder.analyzed_sets, tts
