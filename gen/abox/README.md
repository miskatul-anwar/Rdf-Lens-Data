# Universal ABox (Assertional Box)

The Universal ABox unifies all instance assertions ($C(a)$ and $R(a, b)$) from the entire dataset without loss or prefix corruption.

## Sources Merged
1. **Concept Assertions ($C(a)$)**:
   - `raw/data/instance_types_en.ttl`: Class membership assertions (`<s> rdf:type <C>`).
2. **Role Assertions ($R(a, b)$)**:
   - `raw/data/mappingbased_properties_en.ttl`: High-quality relationship triples mapped to the DBpedia ontology.
   - `raw/data/specific_mappingbased_properties_en.ttl`: Relation assertions with specific units of measurement (e.g. area in $	ext{km}^2$, population density).
3. **Paper Running Example Assertions**:
   - `raw/data/paper_running_example.ttl`: Assertions for individual users, smartphones, ratings, blog posts from Section 2 (Figure 2).

## Metrics
- **Total Assertions**: 34,377,879
- **Concept Assertions (C(a))**: 13,225,156 assertions
- **Role Assertions (R(a,b))**: 20,516,859 assertions
- **Specific Unit Role Assertions (R(a,b))**: 635,830 assertions
- **Paper Running Example Assertions**: 34

## Standard Prefixes Used
```turtle
@prefix dbo:     <http://dbpedia.org/ontology/> .
@prefix dbp:     <http://dbpedia.org/property/> .
@prefix dbr:     <http://dbpedia.org/resource/> .
@prefix dt:      <http://dbpedia.org/datatype/> .
@prefix ex:      <http://example.org/ns#> .
@prefix ans:     <http://example.org/ans#> .
@prefix owl:     <http://www.w3.org/2002/07/owl#> .
@prefix rdf:     <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
@prefix schema:  <http://schema.org/> .
@prefix foaf:    <http://xmlns.com/foaf/0.1/> .
```

## Available Files
- [`abox_sample.ttl`](./abox_sample.ttl): Representative sample in Turtle format with verified standard prefixes (tracked in git).
- `abox.nt`: Full uncompressed Universal ABox in N-Triples format (34,377,879 lines).
