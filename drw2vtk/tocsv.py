import sys
from .reader import read_drw


def csv(f, f_ou=None):
    if f_ou is None:
        fou = sys.stdout
    else:
        fou = open(f_ou, 'w')
    fmt = '{}, ' * 6
    print(fmt.format(*'x y z name group idx'.split()),
          file=fou)
    for e in read_drw(open(f, 'r')):
        (n, g, idx), p = e
        for j in range(p.shape[0]):
            for i in range(p.shape[1]):
                print(fmt.format(p[j, i, 0], p[j, i, 1], p[j, i, 2],
                                 n, g, idx),
                      file=fou)


if __name__ == '__main__':
    from sys import argv
    for f in argv[1:]:
        csv(f)
