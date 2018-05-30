# About  

Synapse detection and characterization are important for elucidating underlying mechanisms for many tasks perfomed by and diseases inflicted upon the central nervous system. However, current methods of detecting synapses and tracking their changes are limited to manually annotating them or generating a probability map, as described in [Probabilistic fluorescence-based synapse detection](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005493). 

The LIDS pipeline will use two-photon microscopy images of mouse cerebral cortex and autonomously detect and characterize excitatory synapses located at dendritic spines expressing AMPA receptors. 


# Requirements

The LIDS pipeline is easily built using Anaconda. We ran this with Anaconda 3 and Python 3.6 but it is possible lower versions of Python will work. If you have not done so, please install [Anaconda Python 3.6 version from here](https://www.anaconda.com/what-is-anaconda/)

# Usage

To access our demo, clone our repository by running the following command in terminal:

```
git clone https://github.com/NeuroDataDesign/LIDS.git

```

THE FOLLOWING COMMANDS MUST BE RUN IN THE TOP DIRECTORY OF LIDS REPOSITORY, use the next command to navigate to LIDS directory:

```
cd LIDS

```
if LIDS is not a sub-directory of your current folder, navigate to it by: 
```
cd <path to LIDS>
```

### Windows specific commands:
If you are using a Windows operating system (OS), please install Ubuntu and run the following commands in Ubuntu terminal 
```
./setup.sh
```

to set up a LIDS conda environment. Change into the LIDS conda environment by 

```
source activate LIDS
```

Run Jupyter Notebook server in activated environment

```

jupyter notebook
```

and navigate to the *tracking_demo notebook* in the *src/demo* folders and run it! 

**Note, the path to imported files in the demo notebook are relative to our folder structure. Please, change the paths to match your folder structure.** 

### Mac specific commands:
Run the following commands in terminal if you have a 64 bit Mac OS. If you do not have a 64 bit OS or were unable to run the next three commands, skip to *creating an environment from scratch* and beyond:

```
conda env create -f environment.yml
```
Activate LIDS:
```
source activate LIDS
```
Run Jupyter Notebook server in activated environment:
```
jupyter notebook
```
and navigate to the *tracking_demo notebook* in the *src/demo* folders and run it! 

**Note, the path to imported files in the demo notebook are relative to our folder structure. Please, change the paths to match your folder structure.** 



If you were unable to run the above commands, do the following:

Create an evironment from scratch to run the notebook:
```
conda create -n <NAME OF ENV> numpy pandas matplotlib seaborn scikit-image pip scipy scikit-learn tifffile trackpy nb_conda imageio -c conda-forge

```
When prompted with *Proceed ([y]/n)?* type *y*


Activate your environment:

```
source activate <NAME OF ENV>

```
We will need another package in our environment:

```
pip install matplotlib-scalebar

```
Run Jupyter Notebook:

```
jupyter notebook

```
and navigate to the *tracking_demo notebook* in the *src/demo* folders and run it! 

**Note, the path to imported files in the demo notebook are relative to our folder structure. Please, change the paths to match your folder structure.** 

The demo notebook **must run in the correct environment**. Even after the creation of your environment, if you are **unable to locate the environment in Jupyter Notebook's kernel**, do the following:

Check to make sure the environment was created:

```
conda info --envs
```
You should see a list of environments and an asterisk beside the active environment

If correct environment is not active, activate it:
```
source activate <NAME OF ENV>
```
If you need to display the name of environment in Jupyter Notebook kernel:

```
source activate <NAME OF ENV>

python -m ipykernel install --user --name <NAME OF ENV> --display-name "<DISPLAY NAME OF YOUR CHOICE>"
```
Environment should be listed under the *Kernel* tab's *Change kernel* option in the notebook. Select the correct kernel environment 




