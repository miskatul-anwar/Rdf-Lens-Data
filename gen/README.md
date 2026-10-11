# Universal Knowledge Base: TBox & ABox

This directory contains the deterministically generated Universal Knowledge Base constructed from the entire corpus of datasets associated with the paper:

> **RDF Analytics: Lenses over Semantic Graphs**  
> *Dario Colazzo, François Goasdoué, Ioana Manolescu, Alexandra Roatiș*  
> Proceedings of the 23rd International World Wide Web Conference (WWW 2014), pp. 467–478.  
> HAL ID: [hal-00960609](https://inria.hal.science/hal-00960609/) | DOI: [10.1145/2566486.2567982](https://doi.org/10.1145/2566486.2567982)

---

## Directory Organization

```
gen/
├── tbox/
│   ├── README.md           # TBox documentation and schema metrics
│   ├── tbox.ttl            # Universal TBox in Turtle format (106,476 axioms)
│   ├── tbox.nt             # Universal TBox in N-Triples format
│   └── tbox.owl            # Universal TBox in OWL/XML format
├── abox/
│   ├── README.md           # ABox documentation and instance assertion metrics
│   ├── abox_sample.ttl     # Representative, valid Turtle sample with standard prefixes
│   └── abox.nt             # Full uncompressed Universal ABox (34,377,879 assertions)
└── README.md               # This architecture overview
```

---

## Knowledge Base Architecture

The Knowledge Base is cleanly partitioned into its terminological component ($\mathcal{T}$, the TBox) and assertional component ($\mathcal{A}$, the ABox) according to description logic principles:

### 1. Universal TBox (`gen/tbox/`)
Unifies all ontology schemas, class hierarchies, property definitions, and analytical lens signatures without loss or duplication.
- **DBpedia 3.8 OWL Ontology DL**: Core class and property taxonomy.
- **Wikipedia Infobox Property Definitions**: Full coverage for 48,302 attribute/predicate declarations.
- **Analytical Schema ($\text{AnS}$)**: 8 analytical classes and 10 analytical properties formalizing the analytical lenses from Section 4 and Table 7.1.
- **Paper Running Example Schema**: Class and property definitions from Section 2 (Figure 3).
- **Total Axioms**: **106,476 triples**
  - **Classes**: 367
  - **Properties**: 50,077
  - **Subclass Axioms**: 372
  - **Domain Axioms**: 1,522
  - **Range Axioms**: 1,570

### 2. Universal ABox (`gen/abox/`)
Unifies all concept assertions ($C(a)$) and role assertions ($R(a, b)$) from all dataset sources:
- **Concept Assertions ($C(a)$)**: 13,225,156 class membership triples (`raw/data/instance_types_en.ttl`).
- **Role Assertions ($R(a, b)$)**: 20,516,859 mapped relationship triples (`raw/data/mappingbased_properties_en.ttl`).
- **Specific Unit Role Assertions ($R(a, b)$)**: 635,830 unit-typed triples (`raw/data/specific_mappingbased_properties_en.ttl`).
- **Paper Running Example Assertions**: 34 instance assertions (`raw/data/paper_running_example.ttl`).
- **Total Assertions**: **34,377,879 triples** (4.74 GB).

---

## Standard Prefixes

All generated artifacts enforce consistent, standard W3C and domain prefixes with zero corruption:

| Prefix | Namespace IRI | Description |
|:---|:---|:---|
| `dbo:` | `http://dbpedia.org/ontology/` | DBpedia Ontology |
| `dbp:` | `http://dbpedia.org/property/` | DBpedia Infobox Properties |
| `dbr:` | `http://dbpedia.org/resource/` | DBpedia Entities / Instances |
| `dt:` | `http://dbpedia.org/datatype/` | DBpedia Datatypes |
| `ans:` | `http://example.org/ans#` | Paper Analytical Schema |
| `ex:` | `http://example.org/ns#` | Paper Running Example |
| `owl:` | `http://www.w3.org/2002/07/owl#` | Web Ontology Language |
| `rdf:` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | RDF Syntax |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` | RDF Schema |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` | XML Schema Datatypes |
| `schema:` | `http://schema.org/` | Schema.org |
| `foaf:` | `http://xmlns.com/foaf/0.1/` | Friend of a Friend |
| `geo:` | `http://www.w3.org/2003/01/geo/wgs84_pos#` | WGS84 Geo Positioning |
| `georss:` | `http://www.georss.org/georss/` | GeoRSS Simple |
| `bibo:` | `http://purl.org/ontology/bibo/` | Bibliographic Ontology |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` | Simple Knowledge Organization |

---

## Reproducibility & Build Scripts

The generation is 100% automated and deterministic via the scripts in `scripts/`:

```bash
# Build Universal TBox (tbox.ttl, tbox.owl, tbox.nt)
python3 scripts/build_tbox.py

# Build Universal ABox (abox.nt, abox_sample.ttl)
python3 scripts/build_abox.py

# Validate syntax with Apache Jena RIOT
riot --validate gen/tbox/tbox.ttl
riot --validate gen/abox/abox_sample.ttl
```
