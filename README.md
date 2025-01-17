# Using Knowledge Graphs for Algorithm Performance Prediction

This repository contains the code and resources developed for the publication:

**Kostovska, Ana, et al.** *"Using Knowledge Graphs for Performance Prediction of Modular Optimization Algorithms"* Presented at **EvoStar 2023**. 

[Read the full paper on arXiv](https://arxiv.org/pdf/2301.09876)



### Paper Contributions

The paper has two main contributions:

1. **Extension of the OPTION Ontology**:  
  The [OPTION (OPTImization Benchmarking Ontology)](https://doi.org/10.1109/TEVC.2022.3232844) was originally developed to represent performance data for optimization algorithms derived from benchmarking studies. In this work, we extend the ontology to include vocabulary for the semantic representation of modular optimization algorithms, their components, parameters, and configuration details.

   - The original OPTION ontology, the extended ontology module, and related ontology files can be found in the `ontology` folder.  
   - As a proof of concept, we created a RDF knowledge base (KB) containing annotations for modular algorithms and developed a SPARQL query endpoint for easy querying.  
   - For more details on how to use the KB, refer to the `ontology` folder.

2. **Using Knowledge Graph (KG) Structures for Predicting Missing Performance Links**:  
   This study investigates the use of KG structures to predict missing performance links between optimization problems and optimization algorithms.  
   - A link labeled as `'solved'` between a problem and an algorithm instance indicates that the algorithm successfully solved the problem within a predefined precision threshold and a fixed budget of function evaluations. Conversely, links labeled as `'not-solved'` indicate that the algorithm failed to achieve the required precision threshold.  
   - While the RDF annotations comprising the knowledge base (KB) can be viewed as KGs, they are highly detailed and verbose, making them unsuitable for effective link prediction tasks. Instead, we use the ontology as a conceptual framework for domain knowledge, enabling the creation of simplified KGs optimized for this study. The KG nodes are "grounded" with ontology terms, ensuring semantic consistency while maintaining practicality for prediction tasks.



---
### Citation

If you use this repository, ontology, or knowledge base in your research, please cite the following publication:

```bibtex
@inproceedings{kostovska2023using,
  title={Using knowledge graphs for performance prediction of modular optimization algorithms},
  author={Kostovska, Ana and Vermetten, Diederick and D{\v{z}}eroski, Sa{\v{s}}o and Panov, Pan{\v{c}}e and Eftimov, Tome and Doerr, Carola},
  booktitle={International Conference on the Applications of Evolutionary Computation (Part of EvoStar)},
  pages={253--268},
  year={2023},
  organization={Springer}
}
