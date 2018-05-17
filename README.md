# About  

Synapse detection and characterization are important for elucidating underlying mechanisms for many tasks perfomed by and diseases inflicted upon the central nervous system. However, current methods of detecting synapses and tracking their changes are limited to manually annotating them or generating a probability map, as described in [Probabilistic fluorescence-based synapse detection](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005493). 

The LIDS pipeline will use two-photon microscopy images of mouse cerebral cortex and autonomously detect and characterize excitatory synapses located at dendritic spines expressing AMPA receptors. 


# Usage

First, `git clone` or download the repository. 

Then, run 
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

and navigate to the demo notebook. 
