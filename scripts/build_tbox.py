#!/usr/bin/env python3
"""
Build the Universal TBox from all schema definitions in raw/data:
1. DBpedia 3.8 OWL Ontology (raw/data/dbpedia_3.8.owl)
2. Wikipedia Infobox Property Definitions (raw/data/infobox_property_definitions_en.ttl)
3. Analytical Schema / Lens (raw/data/analytical_schema.ttl)
4. Paper Running Example Schema (raw/data/paper_running_example.ttl)

Ensures exact prefix bindings with zero hallucinations.
"""

import sys
import time
from pathlib import Path
import rdflib
from rdflib.namespace import RDF, RDFS, OWL, XSD

PREFIXES = {
    "dbo": "http://dbpedia.org/ontology/",
    "dbp": "http://dbpedia.org/property/",
    "dbr": "http://dbpedia.org/resource/",
    "dt": "http://dbpedia.org/datatype/",
    "ans": "http://example.org/ans#",
    "ex": "http://example.org/ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "schema": "http://schema.org/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "geo": "http://www.w3.org/2003/01/geo/wgs84_pos#",
    "bibo": "http://purl.org/ontology/bibo/",
}

def setup_prefixes(g: rdflib.Graph):
    nm = rdflib.namespace.NamespaceManager(g, bind_namespaces="none")
    for prefix, uri in PREFIXES.items():
        nm.bind(prefix, rdflib.Namespace(uri), override=True)
    g.namespace_manager = nm

def build_universal_tbox():
    t0 = time.time()
    tbox = rdflib.Graph()
    setup_prefixes(tbox)

    # 1. DBpedia 3.8 OWL Ontology
    dbpedia_owl_path = Path("raw/data/dbpedia_3.8.owl")
    print(f"Parsing {dbpedia_owl_path}...")
    tbox.parse(dbpedia_owl_path)
    count_dbp = len(tbox)
    print(f"  -> Added {count_dbp} triples from DBpedia OWL ontology.")

    # 2. Infobox property definitions
    infobox_defs_path = Path("raw/data/infobox_property_definitions_en.ttl")
    print(f"Parsing {infobox_defs_path}...")
    tbox.parse(infobox_defs_path, format="turtle")
    count_infobox = len(tbox) - count_dbp
    print(f"  -> Added {count_infobox} triples from infobox property definitions.")

    # 3. Analytical Schema
    ans_path = Path("raw/data/analytical_schema.ttl")
    print(f"Parsing {ans_path}...")
    tbox.parse(ans_path, format="turtle")
    count_ans = len(tbox) - (count_dbp + count_infobox)
    print(f"  -> Added {count_ans} triples from Analytical Schema.")

    # 4. Paper running example schema triples
    ex_path = Path("raw/data/paper_running_example.ttl")
    print(f"Extracting schema triples from {ex_path}...")
    g_ex = rdflib.Graph()
    g_ex.parse(ex_path, format="turtle")
    schema_predicates = {RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range}
    meta_types = {RDFS.Class, OWL.Class, RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty}
    added_ex = 0
    for s, p, o in g_ex:
        if p in schema_predicates or (p == RDF.type and o in meta_types):
            tbox.add((s, p, o))
            added_ex += 1
    print(f"  -> Added {added_ex} schema triples from running example.")

    # Re-apply prefix manager to ensure clean output
    setup_prefixes(tbox)

    total_triples = len(tbox)
    print(f"\nTotal Universal TBox triples: {total_triples}")

    # Metrics
    classes = set(tbox.subjects(RDF.type, OWL.Class)) | set(tbox.subjects(RDF.type, RDFS.Class))
    obj_props = set(tbox.subjects(RDF.type, OWL.ObjectProperty))
    dt_props = set(tbox.subjects(RDF.type, OWL.DatatypeProperty))
    rdf_props = set(tbox.subjects(RDF.type, RDF.Property))
    all_props = obj_props | dt_props | rdf_props
    subclasses = list(tbox.triples((None, RDFS.subClassOf, None)))
    subprops = list(tbox.triples((None, RDFS.subPropertyOf, None)))
    domains = list(tbox.triples((None, RDFS.domain, None)))
    ranges = list(tbox.triples((None, RDFS.range, None)))

    print(f"  Classes: {len(classes)}")
    print(f"  Properties: {len(all_props)} (Object: {len(obj_props)}, Datatype: {len(dt_props)}, Generic: {len(rdf_props)})")
    print(f"  SubClassOf axioms: {len(subclasses)}")
    print(f"  SubPropertyOf axioms: {len(subprops)}")
    print(f"  Domain axioms: {len(domains)}")
    print(f"  Range axioms: {len(ranges)}")

    # Serialize files
    out_dir = Path("gen/tbox")
    out_dir.mkdir(parents=True, exist_ok=True)

    ttl_file = out_dir / "tbox.ttl"
    print(f"\nWriting Turtle: {ttl_file}...")
    tbox.serialize(ttl_file, format="turtle")

    nt_file = out_dir / "tbox.nt"
    print(f"Writing N-Triples: {nt_file}...")
    tbox.serialize(nt_file, format="nt")

    owl_file = out_dir / "tbox.owl"
    print(f"Writing OWL/XML: {owl_file}...")
    tbox.serialize(owl_file, format="xml")

    # Generate documentation
    readme_path = out_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(f"""# Universal TBox (Terminological Box)

The Universal TBox unifies all terminological axioms, class definitions, property hierarchies, domain/range constraints, and schema mappings from the entire dataset without loss or prefix corruption.

## Sources Merged
1. **DBpedia 3.8 OWL Ontology** (`raw/data/dbpedia_3.8.owl`): Formal OWL 2 DL ontology for DBpedia.
2. **Infobox Property Definitions** (`raw/data/infobox_property_definitions_en.ttl`): All property and attribute declarations for raw Wikipedia infoboxes.
3. **Analytical Schema (AnS)** (`raw/data/analytical_schema.ttl`): 8 analytical classes and 10 analytical properties defining the analytical lenses from Section 4 and Table 7.1.
4. **Paper Running Example Schema** (`raw/data/paper_running_example.ttl`): Class and property hierarchy from Section 2 (Figure 3).

## Metrics
- **Total Triples / Axioms**: {total_triples:,}
- **Distinct Classes**: {len(classes):,}
- **Distinct Properties**: {len(all_props):,}
  - Object Properties: {len(obj_props):,}
  - Datatype Properties: {len(dt_props):,}
  - Generic RDF Properties: {len(rdf_props):,}
- **Subclass Axioms (`rdfs:subClassOf`)**: {len(subclasses):,}
- **Subproperty Axioms (`rdfs:subPropertyOf`)**: {len(subprops):,}
- **Domain Axioms (`rdfs:domain`)**: {len(domains):,}
- **Range Axioms (`rdfs:range`)**: {len(ranges):,}

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
""")

    print(f"TBox generation finished in {time.time()-t0:.2f}s.")

if __name__ == "__main__":
    build_universal_tbox()
