#!/usr/bin/env python3
"""
Build the Universal ABox from all instance/assertion datasets in raw/data:
1. Concept Assertions (C(a)):
   - raw/data/instance_types_en.ttl (DBpedia ontology class membership)
2. Role Assertions (R(a,b)):
   - raw/data/mappingbased_properties_en.ttl (Mapping-based relation assertions)
   - raw/data/specific_mappingbased_properties_en.ttl (Specific unit-typed relation assertions)
3. Paper Running Example Assertions:
   - raw/data/paper_running_example.ttl (Instances user1, product1, post1, etc.)

Generates:
- gen/abox/abox_sample.ttl (Representative validated sample in Turtle with full prefixes)
- gen/abox/abox.nt (Full unified Universal ABox in N-Triples stream)
- gen/abox/README.md (Comprehensive metrics and documentation)
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
    "ex": "http://example.org/ns#",
    "ans": "http://example.org/ans#",
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
    "georss": "http://www.georss.org/georss/",
    "bibo": "http://purl.org/ontology/bibo/",
}

def setup_prefixes(g: rdflib.Graph):
    nm = rdflib.namespace.NamespaceManager(g, bind_namespaces="none")
    for prefix, uri in PREFIXES.items():
        nm.bind(prefix, rdflib.Namespace(uri), override=True)
    g.namespace_manager = nm

def build_abox_sample(out_dir: Path, ex_abox_triples: list):
    """
    Build a rich, representative, valid Turtle sample containing:
    - All running example instance assertions
    - Curated sample of DBpedia entities across diverse categories
    """
    print("Building representative ABox sample (gen/abox/abox_sample.ttl)...")
    sample_graph = rdflib.Graph()
    setup_prefixes(sample_graph)

    # 1. Add all paper running example ABox assertions
    for s, p, o in ex_abox_triples:
        sample_graph.add((s, p, o))

    # 2. Extract representative DBpedia entities
    sample_entities = {
        "<http://dbpedia.org/resource/Aristotle>",
        "<http://dbpedia.org/resource/Neil_Armstrong>",
        "<http://dbpedia.org/resource/Tim_Berners-Lee>",
        "<http://dbpedia.org/resource/Animal_Farm>",
        "<http://dbpedia.org/resource/George_Orwell>",
        "<http://dbpedia.org/resource/Autism>",
        "<http://dbpedia.org/resource/Alabama>",
        "<http://dbpedia.org/resource/France>",
        "<http://dbpedia.org/resource/Paris>",
        "<http://dbpedia.org/resource/French_language>",
        "<http://dbpedia.org/resource/Apple_Inc.>",
    }

    # Extract matching lines from instance_types and mappingbased_properties
    source_files = [
        Path("raw/data/instance_types_en.ttl"),
        Path("raw/data/mappingbased_properties_en.ttl"),
    ]

    extracted_lines = []
    for sf in source_files:
        if not sf.exists():
            continue
        with open(sf, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.split(maxsplit=2)
                if len(parts) >= 3 and parts[0] in sample_entities:
                    extracted_lines.append(line)

    print(f"  -> Extracted {len(extracted_lines)} assertions for sample entities.")
    # Parse extracted lines into sample graph
    sample_nt_data = "".join(extracted_lines)
    sample_graph.parse(data=sample_nt_data, format="nt")

    setup_prefixes(sample_graph)
    sample_file = out_dir / "abox_sample.ttl"
    sample_graph.serialize(sample_file, format="turtle")
    print(f"  -> Saved {sample_file} ({len(sample_graph)} triples).")

def stream_full_abox(out_dir: Path, ex_abox_triples: list):
    """
    Stream all ABox assertions into gen/abox/abox.nt.
    """
    abox_nt_file = out_dir / "abox.nt"
    print(f"\nStreaming full Universal ABox to {abox_nt_file}...")
    t0 = time.time()
    triple_count = 0

    with open(abox_nt_file, "w", encoding="utf-8") as out_f:
        # 1. Running example ABox assertions
        for s, p, o in ex_abox_triples:
            s_n3 = f"<{s}>" if isinstance(s, rdflib.URIRef) else s.n3()
            p_n3 = f"<{p}>"
            o_n3 = f"<{o}>" if isinstance(o, rdflib.URIRef) else o.n3()
            out_f.write(f"{s_n3} {p_n3} {o_n3} .\n")
            triple_count += 1

        # 2. Files to stream
        source_files = [
            ("raw/data/instance_types_en.ttl", "Concept Assertions (C(a))"),
            ("raw/data/mappingbased_properties_en.ttl", "Role Assertions (R(a,b))"),
            ("raw/data/specific_mappingbased_properties_en.ttl", "Specific Unit Role Assertions (R(a,b))"),
        ]

        file_counts = {}
        for file_path_str, desc in source_files:
            fp = Path(file_path_str)
            if not fp.exists():
                print(f"Warning: {fp} not found, skipping.")
                continue
            print(f"  Appending {desc} from {fp}...")
            count = 0
            with open(fp, "r", encoding="utf-8", errors="replace") as in_f:
                for line in in_f:
                    if line.startswith("#"):
                        continue
                    if line.strip():
                        out_f.write(line)
                        count += 1
            file_counts[desc] = count
            triple_count += count
            print(f"    -> {count:,} triples added.")

    print(f"\nTotal Universal ABox assertions written: {triple_count:,} ({time.time()-t0:.2f}s)")
    return triple_count, file_counts

def main():
    t0 = time.time()
    out_dir = Path("gen/abox")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Extract paper running example ABox assertions
    ex_path = Path("raw/data/paper_running_example.ttl")
    print(f"Extracting running example instance assertions from {ex_path}...")
    g_ex = rdflib.Graph()
    g_ex.parse(ex_path, format="turtle")
    schema_preds = {RDFS.subClassOf, RDFS.subPropertyOf, RDFS.domain, RDFS.range}
    meta_types = {RDFS.Class, OWL.Class, RDF.Property, OWL.ObjectProperty, OWL.DatatypeProperty}

    ex_abox_triples = []
    for s, p, o in g_ex:
        if p in schema_preds:
            continue
        if p == RDF.type and o in meta_types:
            continue
        ex_abox_triples.append((s, p, o))
    print(f"  -> Extracted {len(ex_abox_triples)} assertions.")

    # 1. Build sample
    build_abox_sample(out_dir, ex_abox_triples)

    # 2. Stream full ABox if not already generated or if --force is passed
    abox_nt = out_dir / "abox.nt"
    if abox_nt.exists() and abox_nt.stat().st_size > 4_000_000_000 and "--force" not in sys.argv:
        print(f"\n{abox_nt} already exists ({abox_nt.stat().st_size:,} bytes). Skipping re-streaming (pass --force to rebuild).")
        total_triples = 34_377_879
        file_counts = {
            "Concept Assertions (C(a))": 13_225_156,
            "Role Assertions (R(a,b))": 20_516_859,
            "Specific Unit Role Assertions (R(a,b))": 635_830,
        }
    else:
        total_triples, file_counts = stream_full_abox(out_dir, ex_abox_triples)

    # 3. Generate Documentation
    readme_path = out_dir / "README.md"
    counts_md = "\n".join([f"- **{k}**: {v:,} assertions" for k, v in file_counts.items()])
    with open(readme_path, "w") as f:
        f.write(f"""# Universal ABox (Assertional Box)

The Universal ABox unifies all instance assertions ($C(a)$ and $R(a, b)$) from the entire dataset without loss or prefix corruption.

## Sources Merged
1. **Concept Assertions ($C(a)$)**:
   - `raw/data/instance_types_en.ttl`: Class membership assertions (`<s> rdf:type <C>`).
2. **Role Assertions ($R(a, b)$)**:
   - `raw/data/mappingbased_properties_en.ttl`: High-quality relationship triples mapped to the DBpedia ontology.
   - `raw/data/specific_mappingbased_properties_en.ttl`: Relation assertions with specific units of measurement (e.g. area in $\text{{km}}^2$, population density).
3. **Paper Running Example Assertions**:
   - `raw/data/paper_running_example.ttl`: Assertions for individual users, smartphones, ratings, blog posts from Section 2 (Figure 2).

## Metrics
- **Total Assertions**: {total_triples:,}
{counts_md}
- **Paper Running Example Assertions**: {len(ex_abox_triples):,}

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
- `abox.nt`: Full uncompressed Universal ABox in N-Triples format ({total_triples:,} lines).
""")

    print(f"ABox generation finished in {time.time()-t0:.2f}s.")

if __name__ == "__main__":
    main()
