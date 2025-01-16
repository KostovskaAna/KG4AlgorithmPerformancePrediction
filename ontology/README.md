# Extension of OPTION for Representing Modular Optimization Algorithms

The OPTION ontology has been enhanced to include vocabulary specifically designed for the semantic representation of modular optimization algorithms, such as modular CMA-ES (modCMA-ES) and modular Differential Evolution (modDE). This extension enables more structured and semantic modeling of modular algorithm components and their configurations.

### Ontologies

This folder contains the following resources:

- **OPTION.owl**: The original OPTION ontology.  
- **OPTION-modAlgo.owl**: An ontology module that extends OPTION with additional vocabulary tailored for modular optimization algorithms.  
- **OPTION-inferred.owl** and **OPTION-modAlgo-inferred.owl**: Versions generated using the **OWLMicroReasoner**, enabling reasoning across the different taxonomies.


### Knowledge Base

To empirically evaluate the proposed ontology module for the semantic representation of modular optimization algorithms, we have created a knowledge base that includes:

- **Annotations for modular algorithms**: **324 modCMA-ES** and **567 modDE** algorithm instances along with their configurations.
- **ELA features**: Descriptions for the **24 noiseless single-objective COCO benchmark problems** in **5D and 30D**, across the first five instances.
- **Performance data**: Results of the modular algorithms on these benchmark problems under various fixed-budget scenarios.

The raw RDF annotations can be downloaded [here](https://www.dropbox.com/scl/fo/3eotdd8d674r06kxj2nvu/AODEHsy7gD8_Dnikv8XTCFU?rlkey=ffrl8d48nbj5ll7ewa6wjmqy5&dl=0) and used to create a local RDF database, allowing you to explore the annotated data further.

#### RDF Files:
- **modular_algo_annotations.rdf**: Contains annotations for **324 `modCMA-ES`** and **567 `modDE`** algorithm instances with various configurations.
- **ela_features.rdf**: Provides ELA (Exploratory Landscape Analysis) features for the 24 noiseless single-objective COCO benchmark problems in **5D and 30D**, across the first five instances.
- **Performance Annotations**:
  - performance_annotations_modCMA-ES_5D.rdf
  - performance_annotations_modCMA-ES_30D.rdf
  - performance_annotations_modDE_5D.rdf
  - performance_annotations_modDE_30D.rdf

---

## SPARQL Endpoint

For those who do not wish to set up their own local RDF database, we provide a publicly accessible SPARQL endpoint for querying the knowledge base.  

The SPARQL endpoint for querying our knowledge base is available at:  
**[http://semanticannotations.ijs.si:8890/sparql](http://semanticannotations.ijs.si:8890/sparql)**

The knowledge base (KB) includes all RDF annotations as well as the inferred versions of the ontologies, enabling advanced reasoning and exploration.

### How to Explore the Knowledge Base:
1. Open the SPARQL query editor at the provided endpoint.
2. Set `http://semanticannotations.ijs.si:8890/modularAlgos` as the **Default Data Set Name (Graph IRI)**.
3. Enter your SPARQL query in the **"Query text"** input field.
4. Execute the query to retrieve results from the KB.

You can also create custom SPARQL queries to explore the data further and generate your own insights from the knowledge base.

---

## Example SPARQL Queries

Below are three example SPARQL queries you can copy-paste directly into the endpoint.  

### 1. List the ELA features for the 5D COCO problems calculated on a sample size of 5000
```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX option: <http://w3id.org/ontoopt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?problem_instance ?ela_feature_label ?ela_feature_group_label ?sampling_technique_label ?ela_feature_value 
WHERE {
  ?problem_class rdfs:subClassOf option:benchmark_problem . 
  ?problem_instance rdf:type ?problem_class .
  ?problem_instance option:has_dimensionality "5"^^xsd:int .
  ?ela_feature <http://purl.obolibrary.org/obo/IAO_0000136> ?problem_instance .
  ?ela_feature option:calculated_on_sample_size "5000"^^xsd:int .
  ?ela_feature rdf:type ?ela_feature_class .
  ?ela_feature_class rdfs:subClassOf ?ela_feature_group .
  ?ela_feature_group rdfs:subClassOf option:ELA_feature .
  ?ela_feature option:has_value ?ela_feature_value .
  ?ela_feature <http://scai.fraunhofer.de/HuPSON#SCAIVPH_00000787> ?sampling_technique .
  
  # Exclude cases where the class is a subclass of itself
  FILTER(?ela_feature_class != ?ela_feature_group)
  
  # Exclude cases where the group is ELA_feature itself
  FILTER(?ela_feature_group != option:ELA_feature)

  # Extract the label from the URI
  BIND(STRAFTER(STR(?ela_feature_group), STR(option:)) AS ?ela_feature_group_label)
  BIND(STRAFTER(STR(?ela_feature_class), STR(option:)) AS ?ela_feature_label)
  BIND(STRAFTER(STR(?sampling_technique), STR(option:)) AS ?sampling_technique_label)
} 
ORDER BY ?ela_feature_label ?problem_instance
```

### 2. Show configuration details of "modCMA-ES_conf_1"

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX option_modular: <http://w3id.org/ontoopt/OPTION_>
PREFIX option: <http://w3id.org/ontoopt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT
       ?mod_cmaes_instance_label
       ?mod_cmaes_execution_part_label
       ?parameter
       ?value
WHERE {
  ?mod_cmaes_instance rdf:type option_modular:00000017 .
  ?mod_cmaes_instance rdfs:label "modCMA-ES_conf_1" .
  ?mod_cmaes_instance rdfs:label ?mod_cmaes_instance_label .
  ?mod_cmaes_implementation <http://purl.obolibrary.org/obo/OBI_0000294> ?mod_cmaes_instance .
  ?mod_cmaes_execution <http://purl.obolibrary.org/obo/OBI_0000308> ?mod_cmaes_implementation .

  ?mod_cmaes_execution <http://purl.obolibrary.org/obo/BFO_0000051> ?mod_cmaes_execution_part .
  ?mod_cmaes_execution_part rdf:type ?mod_cmaes_execution_part_class .
  ?mod_cmaes_execution_part_class rdfs:label ?mod_cmaes_execution_part_label .
  {
    ?mod_cmaes_execution_part option_modular:00000013 ?parameter_instance .
    ?parameter_instance rdf:type ?parameter_class .
    ?parameter_class rdfs:label ?parameter_label .

    ?parameter_instance option:has_value ?value .
    BIND(?parameter_label AS ?parameter)
  }
  UNION
  {
    ?mod_cmaes_execution_part option_modular:00000013 ?parameter_instance .
    ?parameter_instance rdf:type ?parameter_class .
    ?parameter_class rdfs:label ?parameter_label .

    ?parameter_instance <http://purl.obolibrary.org/obo/RO_0002351> ?parameter_member .
    ?parameter_member rdf:type ?parameter_member_class .
    ?parameter_member_class rdfs:label ?parameter_member_label .
    ?parameter_member option:has_value ?value .
    BIND(CONCAT(?parameter_label, " / ", ?parameter_member_label) AS ?parameter)
  }
}
ORDER BY ?mod_cmaes_instance ?mod_cmaes_execution_part_label ?parameter
```

### 3. Show performance data of "modCMA-ES_conf_1" on the 24 COCO problems in 5D in a fixed-budget scenario with 1500 function evaluations

```sparql
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX option_modular: <http://w3id.org/ontoopt/OPTION_>
PREFIX option: <http://w3id.org/ontoopt/>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT DISTINCT ?mod_cmaes_instance_label ?problem_instance ?precision_value
WHERE {
  ?mod_cmaes_instance rdf:type option_modular:00000017 .
  ?mod_cmaes_instance rdfs:label "modCMA-ES_conf_1" .
  ?mod_cmaes_instance rdfs:label ?mod_cmaes_instance_label .
  ?mod_cmaes_implementation <http://purl.obolibrary.org/obo/OBI_0000294> ?mod_cmaes_instance .
  ?mod_cmaes_execution <http://purl.obolibrary.org/obo/OBI_0000308> ?mod_cmaes_implementation .
  ?benchmark_execution <http://purl.obolibrary.org/obo/BFO_0000051> ?mod_cmaes_execution .
  ?benchmark_execution <http://purl.obolibrary.org/obo/BFO_0000051> ?benchmark_execution_on_problem_instance .
  ?benchmark_execution_on_problem_instance <http://purl.obolibrary.org/obo/OBI_0000293> ?problem_instance .
  ?problem_instance option:has_dimensionality "5"^^xsd:int .
  ?benchmark_execution_on_problem_instance <http://purl.obolibrary.org/obo/OBI_0000299> ?precision .
  ?precision <http://w3id.org/ontoopt/at_fixed_buget> "1500"^^xsd:int .
  ?precision option:has_value ?precision_value .
}
```
