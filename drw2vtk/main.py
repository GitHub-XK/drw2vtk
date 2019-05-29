from sys import argv
from .tovtk import tovtk, tovtu
from .tocsv import csv


def main():
    assert len(argv) == 3
    f_in = argv[1]
    f_ou = argv[2]

    if 'vtm' in f_ou:
        tovtk(f_in, f_ou)
    elif 'vtu' in f_ou:
        tovtu(f_in, f_ou)
    elif 'csv' in f_ou:
        csv(f_in, f_ou)
    else:
        raise NotImplementedError('Unknown output format')
