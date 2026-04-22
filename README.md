fMRI State Dynamics: High-Performance Network Analysis

Overview
	This repository contains the infrastructure and analytical pipelines developed to characterize functional brain network dynamics using the Midnight Scan Club (MSC) dataset. This project addresses the "Ball of Yarn" problem in high-dimensional neuroimaging through parallelized signal extraction and Bayesian state-transition modeling.

Core Engineering Highlights
1. High-Performance Connectivity Engine
	Voxel-Wise Parallelization: Implemented custom Python multiprocessing pools to calculate Pearson correlations across >30,000 voxels, reducing processing latency by an order of magnitude.
	Polyglot Workflow: Integrated R-based CIFTI/NIfTI extraction pipelines with Python-based matrix operations for optimized data ingestion.
2. Bayesian State Detection
	Phase Transition Modeling: Developed a high-throughput wrapper for Bayesian Changepoint Detection (BOCD) to identify discrete "phase transitions" in neural time-series.
	Distributed Execution: Parallelized the offline BOCD algorithm to process multiple subjects and sessions concurrently across a scientific computing cluster.
3. Voxel-Wise Manifold Discovery
	Stability-Checked Clustering: Implemented hierarchical agglomerative clustering (Jaccard similarity > 0.7) to decompose traditional brain parcels into functionally distinct sub-regions.
	Non-Averaged Integrity: Utilized a first-principles approach to maintain signal integrity by avoiding the "bleeding" effects of spatial averaging.

Infrastructure
	Rutgers Amarel HPC: Large-scale 4D tensor processing and optimization trials were executed on the Rutgers Amarel Scientific Computing Cluster.

Tech Stack
	Languages: Python (PyTorch, SciPy, Multiprocessing), R (ciftiTools, Mclust).
	Mathematics: Bayesian Inference, Graph Theory, Hierarchical Clustering.
