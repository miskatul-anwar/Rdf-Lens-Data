# Universal TBox (Terminological Box)

The Universal TBox unifies all terminological axioms, class definitions, property hierarchies, domain/range constraints, and schema mappings from the entire dataset without loss or prefix corruption.

## Sources Merged
1. **DBpedia 3.8 OWL Ontology** (`raw/data/dbpedia_3.8.owl`): Formal OWL 2 DL ontology for DBpedia.
2. **Infobox Property Definitions** (`raw/data/infobox_property_definitions_en.ttl`): All property and attribute declarations for raw Wikipedia infoboxes.
3. **Analytical Schema (AnS)** (`raw/data/analytical_schema.ttl`): 8 analytical classes and 10 analytical properties defining the analytical lenses from Section 4 and Table 7.1.
4. **Paper Running Example Schema** (`raw/data/paper_running_example.ttl`): Class and property hierarchy from Section 2 (Figure 3).

## Metrics
- **Total Triples / Axioms**: 106,476
- **Distinct Classes**: 367
- **Distinct Properties**: 50,077
  - Object Properties: 800
  - Datatype Properties: 975
  - Generic RDF Properties: 48,302
- **Subclass Axioms (`rdfs:subClassOf`)**: 372
- **Subproperty Axioms (`rdfs:subPropertyOf`)**: 2
- **Domain Axioms (`rdfs:domain`)**: 1,522
- **Range Axioms (`rdfs:range`)**: 1,570

## Standard Prefixes Defined
```turtle
@prefix dbo:     <http://dbpedia.org/ontology/> .
@prefix dbp:     <http://dbpedia.org/property/> .
@prefix dbr:     <http://dbpedia.org/resource/> .
@prefix dt:      <http://dbpedia.org/datatype/> .
@prefix ans:     <http://example.org/ans#> .
@prefix ex:      <http://example.org/ns#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix schema:  <http://schema.org/> .
@prefix foaf:    <http://xmlns.com/foaf/0.1/> .
@prefix dc:      <http://purl.org/dc/elements/1.1/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix skos:    <http://www.w3.org/2004/02/skos/core#> .
@prefix geo:     <http://www.w3.org/2003/01/geo/wgs84_pos#> .
@prefix bibo:    <http://purl.org/ontology/bibo/> .
```

## Available Formats
- [`tbox.ttl`](./tbox.ttl): Turtle format with verified prefixes (primary representation).
- [`tbox.owl`](./tbox.owl): OWL/XML standard ontology format.
- [`tbox.nt`](./tbox.nt): Line-oriented N-Triples format.
