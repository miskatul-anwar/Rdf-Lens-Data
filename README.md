# RDF-Lens-Data

Datasets, schemas, and knowledge representations for the research paper:

> **RDF Analytics: Lenses over Semantic Graphs**  
> *Dario Colazzo, François Goasdoué, Ioana Manolescu, Alexandra Roatiș*  
> Proceedings of the 23rd International World Wide Web Conference (WWW 2014), pp. 467–478.  
> HAL ID: [hal-00960609](https://inria.hal.science/hal-00960609/) | DOI: [10.1145/2566486.2567982](https://doi.org/10.1145/2566486.2567982)

---

## Repository Structure

- **[`paper/`](./paper/)**: Contains the paper PDF (`paper.pdf`).
- **[`data/`](./data/)**: Contains schemas, running examples, and dataset definitions:
  - `dbpedia_3.8.owl`: DBpedia 3.8 OWL Ontology schema.
  - `analytical_schema.ttl` / `.nq`: Analytical Schema ($\mathcal{S} = \langle N, E, \lambda, \delta \rangle$) defined in the paper.
  - `paper_running_example.ttl` / `.nq`: Running example RDF graph $G$ and RDFS schema.
  - `infobox_property_definitions_en.ttl`: Wikipedia infobox property definitions.
  - `README.md`: Detailed dataset characteristics and sources matching Table 2 of the paper.
