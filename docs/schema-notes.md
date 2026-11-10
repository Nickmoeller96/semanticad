# Schema notes: what `pid-to-kg` produces

Read from `vendor/pid-to-kg/skills/pid-to-kg/references/ontology.md`, `references/schema/graph.schema.json` and `scripts/pidkg/models.py` and `store.py`.

## Node types

| Type | Id | Notes |
|---|---|---|
| `Plant` | `PLANT:<id>` | One per graph |
| `Sheet` | `SHEET:<drawing no.>` | Page, title, revision |
| `Equipment` | tag, else `Pnn.<local>` | `kind` from about 55 values |
| `PipeSegment` | `Pnn.<line>.<k>` | Pipes are nodes, split between in-line items |
| `Component` | tag, else `Pnn.<local>` | Valves and fittings, about 35 kinds |
| `Instrument` | tag | ISA variable, functions, role, location |
| `ControlLoop` | `LOOP:<key>` | Inferred from ISA tags and drawn signals |
| `OffPageConnector` | `Pnn.<local>` | Paired across sheets by the builder |
| `Boundary` | `BOUNDARY:<NAME>` | Source or sink outside the drawings |

Every node carries `label`, `sheets`, `confidence`, `dexpi_class` and a `provenance` list. Each provenance entry has `sheet`, `page`, `bbox`, `source` and `local_id`.

## Edge types

| Type | Meaning | Derived |
|---|---|---|
| `FLOWS_TO` | Physical flow between process items | no |
| `FEEDS` | Equipment-level flow, pipes collapsed | yes |
| `MEASURES` | Instrument to the item it senses | no |
| `SIGNAL_TO` | Drawn signal line | no |
| `ACTUATES` | Controller or switch to final element | yes |
| `MEMBER_OF` | Item to its control loop | yes |
| `CASCADES_TO` | Master loop to slave loop | yes |
| `TRIPS` | Interlock initiator to final element | yes |
| `PART_OF` | Sheet to plant, mounted equipment to parent | no |

## DuckDB layout (`graph.duckdb`)

- Tables: `plant`, `nodes`, `edges`, `issues`
- Views: `flow_edges`, `equipment`, `equipment_flow`, `instruments`, `loops`, `signals`
- Table macros: `upstream(id)`, `downstream(id)`

## What this means for the context layer

- **Join key.** Tagged items use the normalized tag as node id, so layers 2 to 4 can join on `nodes.id`. Untagged items (`Pnn.<local>`) have no stable key across re-extractions and cannot carry history or know-how reliably.
- **Citations.** `provenance.bbox` is a normalized box per item, estimated by the model while reading tiles. It is good enough to point at a region. It is not pixel-exact. Edges have no bbox of their own; a cited connection has to be shown through the boxes of its two end nodes and the segment between them.
- **Confidence.** Self-reported by the model on a fixed rubric (0.95, 0.85, 0.7, 0.5). It is not a measured accuracy.
- **QA flags.** The `issues` table holds them with a severity, a code and the node ids involved. `qa_flags(tag)` can read this table directly.
- **Isolation valves.** Not a concept in the upstream schema. It has to be computed in our layer: walk `FLOWS_TO` in both directions from the asset to the first valve-type `Component` on every branch.
- **Extraction is not a script.** Upstream ships no API call. The reading step is a Claude Code session following `SKILL.md`. `make graph` rebuilds the graph from committed page files; a fully unattended `make build` needs our own extraction runner (milestone M2 or M3).

## Findings from the first build (Pahala WWTP, 8 sheets)

- **Tag grammar.** Sheets P-201 to P-205 number instruments with six digits (`FIT-040141`, `LSH-120102`). Sheet P-101 uses `100.124` and `100, 114A`. The upstream builder does not parse either as ISA (172 `non_isa_tag` notes), so it infers no loops there. Only 6 loops were found, all on P-101 and P-401. A plant-specific tag scheme is needed before `control_loop(tag)` is useful.
- **Repeated SCADA tags.** `LCH-001`, `LCL-001` and similar appear on several sheets for different services. The builder keeps them apart as `#2`, `#3`. These need a sheet-scoped key.
- **Incomplete tags on the drawings.** Several bubbles are printed with a blank suffix (`LSH 100,`). They are recorded as drawn at lower confidence.
- **Untagged equipment.** The two anoxic recycle pumps, the contact basin and the irrigation tank have no printed tag. They get sheet-scoped ids and cannot be joined to history by tag.
- **Positions.** 340 of 495 nodes have a bounding box. Pipe segments, loops and boundaries have none.
- **Off-page connectors.** 18 of 23 paired. The 5 unpaired ones point to sheets outside the selection (P-206 to P-210).
