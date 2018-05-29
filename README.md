# About  

Synapse detection and characterization are important for elucidating underlying mechanisms for many tasks perfomed by and diseases inflicted upon the central nervous system. However, current methods of detecting synapses and tracking their changes are limited to manually annotating them or generating a probability map, as described in [Probabilistic fluorescence-based synapse detection](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005493). 

The LIDS pipeline will use two-photon microscopy images of mouse cerebral cortex and autonomously detect and characterize excitatory synapses located at dendritic spines expressing AMPA receptors. 


# Requirements

The LIDS pipeline is easily built using Anaconda. We ran this with Anaconda 3 and Python 3.6 but it is possible lower versions of Python will work. If you have not done so, please install [Anaconda Python 3.6 version from here](https://www.anaconda.com/what-is-anaconda/)

# Usage

To access our demo, clone our repository by running the **git clone <link to repo>** command in terminal or download the repository. 

### Windows specific commands:
If you are using a Windows OS, please install Ubuntu and run the following commands in Ubuntu terminal 
```
./setup.sh
```

to set up a LIDS conda environment. Change into the LIDS conda environment by 

```
source activate LIDS
```

and run a Jupyter Notebook server

```

jupyter notebook
```

and navigate to the *demo notebook* and run it! **Note, the path to imported files in the demo notebook are relative to our folder structure. Please, change the paths to match your folder structure.** 

### Mac specific commands:
Run the following commands in terminal:

First, create an evironment to run the notebook:
```
conda create -n <NAME OF ENV> numpy pandas matplotlib seaborn scikit-image pip scipy scikit-learn tifffile trackpy nb_conda -c conda-forge

```

Activate your environment:

```
source activate <NAME OF ENV>

```
We will need another package in our environment:

```
pip install matplotlib-scalebar

```
Run Jupyter Notebook

```
jupyter notebook

```
and navigate to the *demo notebook* and run it! **Note, the path to imported files in the demo notebook are relative to our folder structure. Please, change the paths to match your folder structure.** 

The demo notebook **must run in the correct environment**. Even after the creation of your environment, if you are **unable to locate the environment in Jupyter Notebook's kernel**, do the following:


