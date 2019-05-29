from distutils.core import setup
import drw2vtk

setup(name='drw2vtk',
      version=drw2vtk.__version__,
      description='Python converter drw (custom geometry format) to vtk',
      author='A. Travleev',
      author_email='anton.travleev@gmail.com',
      packages=['drw2vtk', ],
      entry_points={'console_scripts': ['drw2vtk = drw2vtk.main:main']},
      install_requires=['vtk', 'numpy'],
      )
