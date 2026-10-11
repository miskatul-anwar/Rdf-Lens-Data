# Datasets and Knowledge Representation (RDF Analytics: Lenses over Semantic Graphs)

This directory contains all datasets, schemas, and knowledge representations used and referenced in the paper:

> **"RDF Analytics: Lenses over Semantic Graphs"**  
> *Dario Colazzo, François Goasdoué, Ioana Manolescu, Alexandra Roatiș*  
> Proceedings of the 23rd International World Wide Web Conference (WWW 2014), pp. 467–478.  
> HAL ID: hal-00960609  
> Associated Technical Report / Thesis: *Efficient Querying and Analytics of Semantic Web Data* (TEL ID: tel-01082065), BDA 2013 (HAL ID: hal-00868616, hal-00868670).

---

## 1. Experimental Datasets (DBpedia 3.8)

In Section 7.1 (Table 2: Dataset characteristics) and Section 6.1 of the extended report:
> *"Our experiments used triples from DBpedia, more specifically, three ontology infobox datasets and the RDFS schema from the version (http://dbpedia.org/Download38)."*

- **Original Graph ($G$)**: $3.4 \times 10^7$ triples (~4.4 GB uncompressed)
- **Ontology Schema**: $5.5 \times 10^3$ triples (746 KB)
- **Dictionary**: $7 \times 10^6$ entries
- **Saturated Graph ($G^\infty$)**: $3.8 \times 10^7$ triples

### Available Files in `data/`:
1. **DBpedia 3.8 Ontology (Schema)**:
   - `dbpedia_3.8.owl` (OWL / RDF-XML format, 793 KB): Formal ontology containing class/subclass, property/subproperty, domain, and range hierarchies used to derive implicit triples via saturation ($G^\infty$).

2. **The Three DBpedia 3.8 Ontology Infobox Datasets**:
   - **Ontology Infobox Types**:
     - `instance_types_en.ttl` (Turtle, 1.8 GB) & `instance_types_en.ttl.bz2` (60 MB)
     - `instance_types_en.nq` (N-Quads, 2.9 GB) & `instance_types_en.nq.bz2` (98 MB)
   - **Ontology Infobox Properties (Mapping-based)**:
     - `mappingbased_properties_en.ttl` (Turtle, 2.6 GB) & `mappingbased_properties_en.ttl.bz2` (175 MB)
     - `mappingbased_properties_en.nq` (N-Quads, 4.3 GB) & `mappingbased_properties_en.nq.bz2` (251 MB)
   - **Ontology Infobox Properties (Specific)**:
     - `specific_mappingbased_properties_en.ttl` (Turtle, 97 MB) & `specific_mappingbased_properties_en.ttl.bz2` (6.1 MB)
     - `specific_mappingbased_properties_en.nq` (N-Quads, 149 MB) & `specific_mappingbased_properties_en.nq.bz2` (11 MB)

3. **Auxiliary Infobox Definitions**:
   - `infobox_property_definitions_en.ttl` (Turtle, 12 MB) & `infobox_property_definitions_en.ttl.bz2` (643 KB)

---

## 2. Paper Running Example & Analytical Schema (AnS)

1. **Running Example Graph & RDFS Schema (Section 2, Figures 2 & 3)**:
   - `paper_running_example.ttl`: Turtle encoding of users, blogs, products, ratings, and RDFS hierarchy.
   - `paper_running_example.nq`: N-Quads encoding of the running example.

2. **Analytical Schema / Lens (Section 4, Figure 4, Table 7.1)**:
   - `analytical_schema.ttl`: Turtle encoding of the 8 AnS nodes and 10 AnS edges with the $\delta$ query definitions.
   - `analytical_schema.nq`: N-Quads encoding of the analytical schema graph.
