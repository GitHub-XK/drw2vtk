# Convert drw to vtk, to be read by ParaView

# Bsed on sandbox/_vtk
import vtk
from .reader import read_drw


def wrapStr(s, name=None):
    """
    Wrap string s into a VTK string array.
    """
    a = vtk.vtkStringArray()
    a.SetNumberOfTuples(1)
    a.SetValue(0, s)
    if name:
        a.SetName(name)
    return a


def _2ugrid(e, ugrid=None):
    """
    Convert element e to an unstructured grid
    """
    # n, g, idx -- name, group and index in the group
    # p -- array (Ns, Np, 3) of points
    (n, g, idx), p = e

    Ns, Np, _ = p.shape

    if ugrid is None:
        # Points
        pl = vtk.vtkPoints()
        # Grid
        ug = vtk.vtkUnstructuredGrid()
        # ug.Allocate(Ns - 1, 1)
        ug.SetPoints(pl)
        i0 = 0
    else:
        ug = ugrid
        pl = ug.GetPoints()
        i0 = pl.GetNumberOfPoints()

    i = 0
    for Is in range(Ns):
        for Ip in range(Np):
            pl.InsertPoint(i0 + i, p[Is, Ip, :])
            i += 1

    # Ns - 1 elements of the grid
    for Is in range(Ns - 1):
        ps = vtk.vtkConvexPointSet()
        pids = ps.GetPointIds()
        for i in range(2*Np):
            pids.InsertId(i, i0 + Is*Np + i)
        ug.InsertNextCell(ps.GetCellType(), pids)

    # Name and group to the Fields
    if ugrid is None:
        f = ug.GetFieldData()
        f.AddArray(wrapStr(n, 'name'))
        f.AddArray(wrapStr(g, 'group'))

    return ug


def tovtk(fdrw, fvtk):
    """
    Reads drw file ``fvtk`` and writes ``fvtk``.
    """
    # All separate ugirds represetning each element are collected together with
    # the data group filter
    gf = vtk.vtkMultiBlockDataGroupFilter()
    for e in read_drw(open(fdrw, 'r')):
        ug = _2ugrid(e)
        gf.AddInputData(ug)

    # Save to file
    w = vtk.vtkXMLMultiBlockDataWriter()
    w.SetFileName(fvtk)
    w.SetInputConnection(gf.GetOutputPort())
    w.Update()
    return


def tovtu(fdrw, fvtk):
    """
    Convert to single unstructured grid.
    """
    u = None
    for e in read_drw(open(fdrw, 'r')):
        u = _2ugrid(e, ugrid=u)
    # Save to file
    w = vtk.vtkXMLUnstructuredGridWriter()
    w.SetFileName(fvtk)
    w.SetInputData(u)
    w.Update()
    return


if __name__ == '__main__':
    from sys import argv
    f_in = argv[1]
    f_ou = argv[2]
    if 'vtm' in f_ou:
        tovtk(f_in, f_ou)
    elif 'vtu' in f_ou:
        tovtu(f_in, f_ou)
