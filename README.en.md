# random-walks-numpy
**Efficient Vectorization Implementation丨Support arbitrary dimensions丨Extensibility Framework**  
**NumPy implementation**: with NumPy's performance and vectorization operations, the code is far more efficient than native Python.  
**Arbitrary dimension D ∈ N**: random walks from 1 to any dimension can be realized by simply changing the input parameters.  
**Expandable framework**: easily supports unbiased/biased, discrete/continuous walk types.

## Environment
**The development environment for this project is as follows**：  
    python = 3.12.9  
    numpy = 2.0.1  
    matplotlib = 3.10.0  

## Current Functions
Multiple arbitrary-dimensional lattice-type discrete-step unbiased free random walks have been realized, i.e., multiple walks in unbounded arbitrary-dimensional space, with each walk randomly selecting a dimension and randomly moving a distance of 1 or -1.  
Calculate partial statistical values of the simulated random walks, such as the average minimum arrival time.  
Draw a road map of the three-dimensional random walk.

## Illustrative Figure
![Example diagram of a 3D random walk](https://github.com/Reclubbit/random-walks-numpy/blob/main/random_walks_images/3d_walk_highres.png)

## Introduction to the Documents
**random_walks.ipynb**：The main jupyter file used in the development facilitates the reader's initial attempts to simulate the random walk feature.  
**random_walks.py**：Integration of python files with current developed functionality is even better.

## Future goals
Develop other random walk types such as diagonal, continuous step, biased walks.  
Compute other relevant statistics and visualize them.  
Draw 1-dimensional and 2-dimensional random walk roadmaps.  
Optimize code logic and countermeasures for unexpected situations.

## Contribute to the Project & Contact Me
If you find any bugs or have suggestions for new features, and any technical issues, you are welcome to raise an Issue or submit a PR.

- Maintained by [@Reclubbit](https://github.com/Reclubbit)
- E-mail: reclubbit@163.com (if you have any suggestions, you can send an e-mail to this e-mail)
- WeChat: Reclubbit (welcome to learn and chat, add friends with “Random Walk”)

## Open source protocol
This project adopts MIT protocol open source, can be freely used, modified, released, including closed source and commercial, but should retain the author's signature and protocol statement.  
Details see the project root directory LICENSE file , the content of the agreement to the document shall prevail.
