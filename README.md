# RDF-Lens-Data

Datasets, schemas, and Universal Knowledge Base (TBox and ABox) for the research paper:

> **RDF Analytics: Lenses over Semantic Graphs**  
> *Dario Colazzo, François Goasdoué, Ioana Manolescu, Alexandra Roatiș*  
> Proceedings of the 23rd International World Wide Web Conference (WWW 2014), pp. 467–478.  
> HAL ID: [hal-00960609](https://inria.hal.science/hal-00960609/) | DOI: [10.1145/2566486.2567982](https://doi.org/10.1145/2566486.2567982)

---

## Directory Organization

```
root/
├── raw/                      # Original source datasets, schemas, and paper
│   ├── data/                 # Raw DBpedia 3.8, infobox definitions, AnS & paper graphs
│   │   ├── analytical_schema.ttl / .nq
│   │   ├── paper_running_example.ttl / .nq
│   │   ├── dbpedia_3.8.owl
│   │   ├── infobox_property_definitions_en.ttl
│   │   ├── instance_types_en.ttl (and .bz2)
│   │   ├── mappingbased_properties_en.ttl (and .bz2)
│   │   ├── specific_mappingbased_properties_en.ttl (and .bz2)
│   │   └── README.md
│   ├── paper/
│   │   └── paper.pdf
│   └── README.md
├── gen/                      # Unified Universal Knowledge Base
│   ├── tbox/                 # Terminological Box (Schema, Axioms, Lens definitions)
│   │   ├── tbox.ttl          # 106,476 axioms in Turtle format
│   │   ├── tbox.nt           # N-Triples format
│   │   ├── tbox.owl          # OWL/XML format
│   │   └── README.md
│   ├── abox/                 # Assertional Box (Concept & Role assertions)
│   │   ├── abox_sample.ttl   # Validated sample in Turtle format with standard prefixes
│   │   ├── abox.nt           # 34,377,879 assertions in N-Triples format
│   │   └── README.md
│   └── README.md             # KB Architecture and schema documentation
└── scripts/                  # Automated build and validation pipeline
    ├── build_tbox.py         # Merges all TBox sources with verified prefix bindings
    └── build_abox.py         # Merges and streams all ABox assertions (34.3M triples)
```

---

## Universal Knowledge Base Summary

| Component | Format | Triples / Axioms | Description |
|:---|:---|:---:|:---|
| **Universal TBox** | `.ttl`, `.owl`, `.nt` | **106,476** | DBpedia 3.8 OWL + Infobox Properties + Analytical Schema (AnS) + Paper Example Schema |
| **Universal ABox** | `.nt` | **34,377,879** | Concept assertions ($C(a)$) + Mapping role assertions ($R(a,b)$) + Paper instances |
| **ABox Sample** | `.ttl` | **308** | Validated representative sample in Turtle format |

---

## Reproduction & Verification

```bash
# Validate TBox and ABox sample using Apache Jena RIOT:
riot --validate gen/tbox/tbox.ttl
riot --validate gen/abox/abox_sample.ttl

# Rebuild TBox:
python3 scripts/build_tbox.py

# Rebuild ABox:
python3 scripts/build_abox.py
```
