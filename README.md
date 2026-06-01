# fMRI State Dynamics Archive

This repository is an exploratory research-code archive preserved for provenance.

It contains code, notebooks, intermediate outputs, and analysis fragments from an academic research project on dynamic fMRI connectivity. It is not intended to represent production-quality software.

A cleaned and reproducible portfolio version of selected analysis components will be developed separately.

--------------------------------------------------------------------------
# **fmri-state-dynamics: High-Performance Network Connectivity Pipeline**

## **Overview**

This repository contains a modular processing pipeline developed to characterize individual-specific functional brain network topographies using the Midnight Scan Club (MSC) dataset.

The project addresses the computational bottleneck of voxel-wise analysis by utilizing a parallelized correlation engine to process high-resolution cortical surface data. By moving beyond group-averaged templates, this workflow identifies unique "functional fingerprints" and reconstructs directed information flow between task-relevant regions of interest.

## **Core Engineering Highlights**

### **High-Performance Connectivity Engine**

* **Voxel-Wise Parallelization:** Implemented a custom Python multiprocessing framework to calculate Pearson correlations across \>30,000 vertices, successfully bypassing the memory constraints of standard serial processing.  
* **Polyglot Workflow:** Architected a seamless data handoff between R (ciftiTools) for specialized neuroimaging signal extraction and Python (NumPy, SciPy) for matrix-heavy statistical operations.

### **Precision Functional Mapping**

* **Stability-Checked Clustering:** Developed a hierarchical agglomerative clustering pipeline with bootstrap validation (Jaccard similarity coefficients \> 0.7) to identify functionally homogenous sub-regions within individual subjects.  
* **Non-Averaged Signal Integrity:** Employed a first-principles approach to maintain raw signal variance, avoiding the spatial "bleeding" effects inherent in traditional group-level anatomical templates.

### **Directed Network Reconstruction**

* **Peak-Lag Analysis:** Developed logic to infer information precedence by analyzing temporal shifts (![][image1]) between visual and medial temporal nodes.  
* **Graph Modeling:** Reconstructed directed neural pathways using Directed Acyclic Graphs (DAGs) to visualize the hierarchy of information flow during task-positive states.

## **Infrastructure**

* **Rutgers Amarel HPC Cluster:** Large-scale 4D tensor processing and parallel map-reduce tasks were optimized for distributed execution across high-performance computing nodes.

## **Repository Structure**

* **/src**: Modular software components including the correlation engine, parcel extractors, and cluster orchestrators.  
* **/notebooks**: Documented research narrative covering ROI selection, clustering stability, and final result sweeps.  
* **/research**: Academic summary of the project objectives, methodology, and findings.  
* **/archive**: Iterative history of the project, including legacy scripts and environment migration tools.

## **Tech Stack**

* **Languages:** Python (Multiprocessing, SciPy, Pandas), R (ciftiTools, fpc)  
* **Mathematics:** Graph Theory, Hierarchical Clustering, Peak-Lag Cross-Correlation  
* **Systems:** Linux/Windows Path Orchestration, HPC Slurm Job Management

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGcAAAAeCAYAAAAxbADwAAAD1klEQVR4Xu2aS2jUUBSG61hfqKBoKc40k+nMaOuICI5CERVRcSH4ogsXFlrRnau6EVxIQcUHIqKCgkuhCiKiiC4KRSvoSqvgRqggbkpVaF1YUJH6n869evybZApO26Tkg0OSc/5755ycPK6pVVUxMTExMTExMUIGpNPpQl1dXQqHCcdxktlsdgV8G1krQN5UX1+/OZ/Pz2loaFjouu5a1oQN5LwIdW1C3i4OEzU1NQtwnEPuG1grQN8I24JzslrqlK2fdkJBEj344REvY63AGj9dmECOpznnoNzh/8U6P+2kgCa1SgK4Y55yjIHuJ+wD7AjHwow8JeyJxu5cjmug6TPaCxybdFTiQxzT4BafB80w+6OCbQ4ea+s4pjENbGX/VFFtE08mk0s5aMGddQZ2gv1RwdYIa+aYBe+mHYg/Yf+UYhPHFbOXYxaJsy9KqOZc5JgllDWqxM9zzDzO3qdSqSUcixKqxhccE+DvlJUa+6cclfgtjiHhsxJjf9RQNfZzzDzOwlmjTRzvlI8UmgH/D9hK8kcO1PDJ1ukRE/8h9ocCJDbolbgUVG7pGRVQy12fGrtRY6P2hQok+Mon8TFXWVRBAy5FskYkeJUSl+X1y6CldeiLItCc/dwc7F/Bo3yb1mmM/ib7iQQ7KgoSbNGJYzuMYnpYZ5FVDTSD7A8zuVzOUTXKu/Qt7DPrLPI4Fy3OTZFjGvn+xr6KIh80KfHv+NHlrLMg8Q5o7rE/5IzWZepcZraHWWRBbCvsC3Znckwz4c2pUl8J3NJd47kIwFV0W+4oo+uGdWWz2TTrNBizHWPuQ7uPYwx0e6B7yH4voHsk87I/CMnX1uj6rEDhP25039zSu7gLNexinSWoORjbmyl9u3wOuwO7DDsJeyNfvVnvi0labuPrHNNAc0p07PfDzjueMVaHgto4pkG83Wodx9nNcT/k85MZ95pjzHjyFfyag7zWy9b8eWXMIgQ1HNS+QGyxtbW18zmmsXcO+/2w845njNX5FWzJlN55o1rsZzjuh7mKR/AYX8MxxiPfhPyuh7WxDxfBYozfKYPk4sH+OztJsVicZfJu+jt1GTBgAHaD/Yw5KZFaDFjMSXvGfkb+KOfRHE/KXUiYpxd2QB3Lo61TayqGac5Rs9+HTTVJIg+u6nOuWvCgqat0XBPUHMzRzE2W40KhMNvsj95dFUMmt8tLbI9xfDqA5jyAtZv9Ngr/Q1BzMuYfvtpnj+W/BcgjTsf+G0zeL3cMGnONY9MFnPA8ahyCPc6U+bQT1ByMH+TvlfB9hQ1g3g7tj5kApJHsi4mJiYn5w28BuE17G5GsSwAAAABJRU5ErkJggg==>
