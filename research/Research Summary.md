# **MSC Precision Functional Mapping: Directed Network Analysis**

**Project Focus:** Individual-specific neural network topographies

**Dataset:** Midnight Scan Club (MSC) \- Natural Viewing Task

## **Objective**

The primary aim of this analysis was to move beyond static, group-averaged brain parcellations to reconstruct individual-specific directed neural pathways. By analyzing BOLD signal time-lags across thousands of voxels, we sought to map the causal flow of information between visual processing regions and medial temporal memory systems.

## **Methodology**

* **Data Engineering:** Extracted high-resolution CIFTI surface data utilizing R (ciftiTools) and the RU\_KONG parcellation scheme (Kong et al. 2021).  
* **Cluster Stability:** Implemented agglomerative hierarchical clustering with bootstrap validation. Functional sub-regions were identified based on stability metrics, ensuring Jaccard similarity coefficients remained \> 0.7 across independent sessions.  
* **Computational Scale:** Developed a custom parallelized correlation engine in Python to bypass the memory bottlenecks associated with 30k+ vertex-to-matrix calculations on the Rutgers Amarel HPC Cluster.  
* **Network Reconstruction:** Constructed Directed Acyclic Graphs (DAGs) using cross-correlation peak-lag analysis (![][image1]) to define weights and infer information precedence between nodes.

## **Results and Analysis**

* **Pathway Identification:** Confirmed robust information flow from visual cortices to the medial temporal lobe during task-positive states.  
* **Functional Integrity:** Analysis demonstrated that precision functional mapping reveals network fingerprints that are typically obscured by traditional spatial averaging or group-level templates.  
* **Reliability:** Remarkable consistency was observed between sessions MSC06 and MSC08 despite the high degrees of freedom inherent in voxel-wise clustering.

## **Repository Contents**

* [**Source Code**](https://www.google.com/search?q=../src/)**:** Parallelized correlation orchestrators and R-based data extraction utilities.  
* [**Analysis Notebooks**](https://www.google.com/search?q=../notebooks/)**:** Voxel clustering pipelines and statistical result sweeps.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGcAAAAeCAYAAAAxbADwAAAD1klEQVR4Xu2aS2jUUBSG61hfqKBoKc40k+nMaOuICI5CERVRcSH4ogsXFlrRnau6EVxIQcUHIqKCgkuhCiKiiC4KRSvoSqvgRqggbkpVaF1YUJH6n869evybZApO26Tkg0OSc/5755ycPK6pVVUxMTExMTExMUIGpNPpQl1dXQqHCcdxktlsdgV8G1krQN5UX1+/OZ/Pz2loaFjouu5a1oQN5LwIdW1C3i4OEzU1NQtwnEPuG1grQN8I24JzslrqlK2fdkJBEj344REvY63AGj9dmECOpznnoNzh/8U6P+2kgCa1SgK4Y55yjIHuJ+wD7AjHwow8JeyJxu5cjmug6TPaCxybdFTiQxzT4BafB80w+6OCbQ4ea+s4pjENbGX/VFFtE08mk0s5aMGddQZ2gv1RwdYIa+aYBe+mHYg/Yf+UYhPHFbOXYxaJsy9KqOZc5JgllDWqxM9zzDzO3qdSqSUcixKqxhccE+DvlJUa+6cclfgtjiHhsxJjf9RQNfZzzDzOwlmjTRzvlI8UmgH/D9hK8kcO1PDJ1ukRE/8h9ocCJDbolbgUVG7pGRVQy12fGrtRY6P2hQok+Mon8TFXWVRBAy5FskYkeJUSl+X1y6CldeiLItCc/dwc7F/Bo3yb1mmM/ib7iQQ7KgoSbNGJYzuMYnpYZ5FVDTSD7A8zuVzOUTXKu/Qt7DPrLPI4Fy3OTZFjGvn+xr6KIh80KfHv+NHlrLMg8Q5o7rE/5IzWZepcZraHWWRBbCvsC3Znckwz4c2pUl8J3NJd47kIwFV0W+4oo+uGdWWz2TTrNBizHWPuQ7uPYwx0e6B7yH4voHsk87I/CMnX1uj6rEDhP25039zSu7gLNexinSWoORjbmyl9u3wOuwO7DDsJeyNfvVnvi0labuPrHNNAc0p07PfDzjueMVaHgto4pkG83Wodx9nNcT/k85MZ95pjzHjyFfyag7zWy9b8eWXMIgQ1HNS+QGyxtbW18zmmsXcO+/2w845njNX5FWzJlN55o1rsZzjuh7mKR/AYX8MxxiPfhPyuh7WxDxfBYozfKYPk4sH+OztJsVicZfJu+jt1GTBgAHaD/Yw5KZFaDFjMSXvGfkb+KOfRHE/KXUiYpxd2QB3Lo61TayqGac5Rs9+HTTVJIg+u6nOuWvCgqat0XBPUHMzRzE2W40KhMNvsj95dFUMmt8tLbI9xfDqA5jyAtZv9Ngr/Q1BzMuYfvtpnj+W/BcgjTsf+G0zeL3cMGnONY9MFnPA8ahyCPc6U+bQT1ByMH+TvlfB9hQ1g3g7tj5kApJHsi4mJiYn5w28BuE17G5GsSwAAAABJRU5ErkJggg==>