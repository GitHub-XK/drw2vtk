# drw2vtk
Convertor custom geometry drw to vtk.

# INSTALLATION
This package relies on `numpy` and ``vtk``. Possibly the most simple way to get the required packages installed is to use the ``anaconda``
python distribution. The following commands were tested under Ubuntu-18.04.02 LTS with anaconda python 3.7.2:

```bash
# get the source files from this repo:
>git clone git@github.com:travleev/drw2vtk.git

# use the install script:
>cd drw2vtk
>./install.sh
```

# INVOCATION
When installed, the package provides `drw2vtk` scripjt. It takes two arguments: the 1-st one is the original `drw` file containing the custom geometry (extension does not matter) and
the 2-nd argument is the name of the output file. Here, the result depends on the 2-nd file extension, which currently can be one of `vtm`, `vtu` or `csv`.

Examples:
```bash
>drw2vtk model.drw model.vtm  
>drw2vtk model.drw model.vtu
>drw2vtk model.drw model.csv
```



