# LSFM 3D Morphable Model construction pipeline

This repository contains the code used to produce the Large Scale Facial Model (LSFM) presented in:

> [**Large scale 3D Morphable Models**
J. Booth, A. Roussos, A. Ponniah, D. Dunaway, S. Zafeiriou.
*International Journal of Computer Vision (IJCV), April 2017*](https://link.springer.com/article/10.1007/s11263-017-1009-7)

> [**A 3D Morphable Model learnt from 10,000 faces**
J. Booth, A. Roussos, S. Zafeiriou, A. Ponniah, D. Dunaway.
*Proceedings of IEEE Int’l Conf. on Computer Vision and Pattern Recognition (CVPR), June 2016*](http://ibug.doc.ic.ac.uk/media/uploads/documents/0002.pdf)


## Installation

We strongly advocate the use of Anaconda for the installation of this code.
LSFM has complex dependencies which will be installed trivially if you use `conda`.


Follow the conda installation instructions from the [Menpo website](http://www.menpo.org/installation/conda.html). Then run:
```
> conda create -n lsfm -c menpo python=3.5 lsfm
```
which:
- creates a new Python 3.5 environment called `lsfm` (`create -n lsfm`, `python=3.5`)
- which uses the `menpo` conda channel... (`-c menpo`)
- ...to install the `lsfm` package along with all it's dependencies. (the final `lsfm`)

LSFM can be used on Windows, macOS and Linux. However, presently **only Linux comes with suitesparse** which **hugely increases the performance of the code**. Because of this, **we strongly recommend you use Linux** for building large models - performance will be 5x-10x faster than it is on Windows or macOS.

If you want to help get suitesparse working on macOS or Windows feel free to raise isses/PRs against our [conda-suitesparse](https://github.com/menpo/conda-suitesparse) repository.

Also note that LSFM requires the Basel Face Model in order to prepare the facial template we use for building the model. Presently the user needs to have access to the BFM. The first time you run `lsfm` you will be asked to provide the `01_MorphableModel.mat` file from Basel so LSFM's template can be initialized. This only has to be done once.

## Usage
To use the code, first activate the `lsfm` environment you made in the previous command
```
> source activate lsfm
```
and then use the `lsfm` command line tool
```
(lsfm) > lsfm --help
```

LSFM takes a given a folder of **textured facial meshes** in any format supported by `menpo3d` (`.obj`, `.ply`, etc) and automatically:

1. Landmarks every mesh with the `ibug68` annotation scheme
2. Brings all meshes into correspondence with a template
3. Builds an initial PCA model
4. Automatically detects and discards correspondence failure cases
5. Outputs a final PCA model in the same format the LSFM models are provided in

The input mesh directory , which is specified by the `-i` flag, should contain meshes in a single folder level that are uniquely identified by their file name stem:

```
./input_dir/
    0001.obj
    0001.jpg
    another_mesh.obj
    another_mesh.jpg
    ...
```

All output (registered meshes, visualizations and graphs, and the PCA models) is saved in an output directory specified by the `-o` flag. A basic invocation of the tool would therefore be:

```
> lsfm -i ./input_dir -o ./ouput_dir
```


#### Resuming a build

Processing large collections of meshes takes a long time, so commonly you may need to interrupt `lsfm` for some reason. `lsfm` will resume computation if you just run the same command again - already completed work will be skipped.

Furthermore, if you have already run `lsfm` once, you need not provide the input directory on future invocations - the output directory contains a list of all mesh paths for processing in the `settings.json` file, and `lsfm` will just continue with all these meshes:

```
> lsfm -o ./ouput_dir
```

If you provide an input directory for an existing output directory already exists, LSFM checks if the input directory contains the same meshes or a superset of the already catalogued meshes. If it does, the `settings.json` file will be updated with the new superset of mesh paths and processing will continue. If the input directory is missing some of the meshes in `settings.json`, an error is raised.

#### Parallelizing the build

It takes around 1 minute to process a single mesh on Linux (where `suitesparse` is available - more like 5-10minutes on other platforms). LSFM can use multiple cores to parallelize this process - just provide the `-j` flag with a number of cores

```
> lsfm -i ./input_dir -o ./ouput_dir -j6
```

Note that logging is more difficult to follow with parallel builds. If you wish to better understand errors, we recommend temporarily disabiling multi-process building.
