# read drw data
import numpy as np


def _convert(t):
    """
    In the original drw file point coordinates are presented as a table with
    Ns columns (Ns -- number of sections) and 3*Np lines (Np -- number of
    points representing each section). Argument ``t`` is a list of rows of
    this table.

    This function converts ``t`` to an array with the spahe (Ns, Np, 3).
    """
    # Remove optional number of sections and points from the 1-st line
    if len(t) % 3 == 1:
        t = t[1:]

    a = np.array(t)
    Ns = a.shape[1]
    Np = a.shape[0] // 3
    assert Np * 3 == a.shape[0]
    r = np.zeros((Ns, Np, 3))
    # a[i::Np, j] -- coordinates of the i-th point of the j-th section
    for j in range(Ns):
        for i in range(Np):
            r[j, i, :] = a[i::Np, j]
    return r


def _pd(flag, ttl, *args, **kwargs):
    """
    Print mdg if flag is True.
    """
    if flag:
        print(ttl)
        for a in args:
            print('    ', repr(a))
        for k, v in list(kwargs.items()):
            print('    ', k, repr(v))
    return


def read_drw(f, db=0):
    """
    Yield elements from the drw file f.
    debug -- additional output: 0 -- no output, 1 --
    """
    t_prv = None  # list, tokens from the previous line
    t_cur = None  # list, tokens from the current line
    state = None  # Current state of the cursor in the line.
    coordinates = []   # Lines with coordinates for the current element
    ename = []         # Element's name, group and index in the group
    for l in f:
        # From the previous information I know exactly possible meanings of the
        # current line. The actual meaning depends on the number of entries and
        # their format.
        _pd(4<db, 'Status at the current line',
            cline=l, t_prv=t_prv, state=state)

        t_cur = l.split()
        if not t_cur:
            # This is an emply line, simply skip it
            continue

        if t_prv is None:
            # This is the 1-st line of the file. It can be (1) number of
            # elements or (2) the beginning of the 1-st element
            if len(t_cur) == 1:
                state = 0  # t_prv will be Number of elements
            else:
                state = 1  # t_prv will be 1-st line of the element
            t_prv = t_cur
            continue

        if state == 0:
            # t_prv is the line with Number of elements. Next -- 1-st elements
            # line.
            state = 1
            t_prv = t_cur
            continue

        if state == 1:
            # t_prv -- 1-st elements line, next -- optional number of points
            # and sections

            # If there is previous element, yield it
            if coordinates:
                r = _convert(coordinates)
                yield (ename, r)

            # Place to store all lines with the point coordinates
            coordinates = []
            # Name of group of the current element
            ename = t_prv
            _pd(1<db, '1-st line of the new element', ename)

            # ELement's index in the group -- optional
            if len(ename) > 2:
                ename[2] = int(ename[2])
            else:
                ename.append(-1)

            state = 2  # t_prv will be line with coordinates or next element
            t_prv = t_cur
            continue

        if state == 2:
            # t_prv -- line with coordinates to store. t_cur can be the next
            # line with coordinates or the 1-st lineof the next element.
            coordinates.append(list(map(float, t_prv)))

            t_prv = t_cur
            state = 2
            try:
                float(t_cur[0])
            except ValueError:
                state = 1
            continue


if __name__ == '__main__':
    from sys import argv
    for f in argv[1:]:
        print('Elements from ', f)
        for name, points in read_drw(open(f, 'r'), db=0):
            print(name, points.shape[:-1])
