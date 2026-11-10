# Pahala WWTP: process knowledge graph summary

Built from `pahala.pdf` (8 sheets) by pid-to-kg 0.1.0 on 2026-11-10. The graph has 495 nodes and 597 edges; this summary covers equipment-level flow, instruments and control loops. Query `graph.duckdb` or `graph.json` for pipe-segment and valve detail.

| Equipment | Instruments | Valves & fittings | Pipe segments | Control loops | Off-page links |
|---|---|---|---|---|---|
| 22 | 205 | 76 | 140 | 6 | 23 |

## Sheets

| Page | Drawing | Title | Type |
|---|---|---|---|
| 9 | P-101 | HEADWORKS FACILITY P&ID | pid |
| 10 | P-201 | P&IDS ANOXIC BASIN | pid |
| 11 | P-202 | P&IDS PRE-AERATION BASIN | pid |
| 12 | P-203 | P&IDS MEMBRANE BIOREACTOR BASIN | pid |
| 13 | P-204 | P&IDS PERMEATE COLLECTION | pid |
| 14 | P-205 | P&IDS PRE-AERATION AND MEMBRANE BIOREACTOR TOWERS | pid |
| 21 | P-401 | P&IDS IRRIGATION EQUALIZATION TANK P&ID | pid |
| 22 | P-501 | SUBSURFACE DRIP EFFLUENT DISPOSAL P&ID | pid |

## Process flow (equipment to equipment)

Each line reads *upstream → downstream*, with the pipe lines and in-line items between them. Pipes, valves and instruments are collapsed; use `kg_query.py path` for the full route.

- **3W UTILITY WATER** → **FINE SCREEN**: through solenoid valve
- **3W UTILITY WATER** → **OTHER USES**
- **FINE SCREEN** → **BAG OR CONTAINER**
- **RS FROM PAHALA** → **MANUAL BAR RACK**: through Flume (open-channel flow element symbol, unlabelled), OVERFLOW WEIR, BAR RACK SLIDE GATE
- **RS FROM PAHALA** → **Screen channel (open channel with HWWL mark; no tag or label printed)**: through Flume (open-channel flow element symbol, unlabelled)
- **MANUAL BAR RACK** → **GRIT REMOVAL TANK**: through BAR RACK SLIDE GATE
- **Screen channel (open channel with HWWL mark; no tag or label printed)** → **GRIT REMOVAL TANK**
- **Screen channel (open channel with HWWL mark; no tag or label printed)** → **MANUAL BAR RACK**: through OVERFLOW WEIR, BAR RACK SLIDE GATE
- **GRIT REMOVAL TANK** → **AX-01** (ANOXIC BASIN): crosses sheets
- **AX-01** (ANOXIC BASIN) → **Unlabelled line end beyond valve on basin low-level outlet**: through manual valve
- **AX-01** (ANOXIC BASIN) → **Submersible recycle pump (no tag drawn; instruments numbered 040122)**
- **AX-01** (ANOXIC BASIN) → **Submersible recycle pump (no tag drawn; instruments numbered 040121)**
- **Submersible recycle pump (no tag drawn; instruments numbered 040122)** → **PA-01** (PRE-AERATION BASIN): through reducer, check valve, manual valve, reducer, FE-040141, reducer, manual valve; crosses sheets
- **Submersible recycle pump (no tag drawn; instruments numbered 040121)** → **PA-01** (PRE-AERATION BASIN): through reducer, check valve, manual valve, reducer, FE-040141, reducer, manual valve; crosses sheets
- **PA-01** (PRE-AERATION BASIN) → **Unlabelled line end beyond valve V-120122 on basin low-level outlet**: through V-120122
- **PA-01** (PRE-AERATION BASIN) → **MB-01** (MEMBRANE BIOREACTOR BASIN): through WE-050121; crosses sheets
- **MB-01** (MEMBRANE BIOREACTOR BASIN) → **Unlabelled line end beyond valve on basin bottom outlet**: through manual valve
- **HYPOCHLORITE SOLUTION** → **CONTACT BASIN**
- **CONTACT BASIN** → **TANK**
- **TANK** → **DRIP ZONE 3**: through FE-403, motor operated valve; crosses sheets
- **TANK** → **DRIP ZONE 2**: through FE-403, motor operated valve; crosses sheets
- **TANK** → **DRIP ZONE 1**: through FE-403, motor operated valve; crosses sheets
- **TANK** → **DRIP ZONE 4**: through FE-403, motor operated valve; crosses sheets
- **filter** → **BLR-100101** (PRE-AERATION BLOWER 1)
- **BLR-100101** (PRE-AERATION BLOWER 1) → **FBD-050111** (FBD (diffuser symbol on basin floor, fed by process air)): through check valve, butterfly valve, reducer, TP-01; crosses sheets
- **filter** → **BLR-090101** (MEMBRANE BIOREACTOR BLOWER 1)
- **BLR-090101** (MEMBRANE BIOREACTOR BLOWER 1) → **SMU** (SMU- (FUTURE MEMBRANES)): lines 3"-A; through check valve, butterfly valve, reducer, butterfly valve, expansion joint; crosses sheets
- **BLR-090101** (MEMBRANE BIOREACTOR BLOWER 1) → **SMU-070121** (Submerged membrane unit (two stacked cassette blocks over a diffuser)): through check valve, butterfly valve, reducer, butterfly valve, expansion joint; crosses sheets
- **BLR-090101** (MEMBRANE BIOREACTOR BLOWER 1) → **SMU-070111** (Submerged membrane unit (two stacked cassette blocks over a diffuser)): through check valve, butterfly valve, reducer, butterfly valve, expansion joint; crosses sheets
- **SMU** (SMU- (FUTURE MEMBRANES)) → **PMP-080101** (Permeate pump (no descriptive name printed)): through ball valve, butterfly valve, butterfly valve, expansion joint, reducer; crosses sheets
- **SMU** (SMU- (FUTURE MEMBRANES)) → **CONTACT BASIN**: through ball valve, butterfly valve, check valve, FE-080141, reducer, FCV-080132, reducer, reducer, reducer; crosses sheets
- **SMU** (SMU- (FUTURE MEMBRANES)) → **MB-01** (MEMBRANE BIOREACTOR BASIN): lines 3"-A; through manual valve, XV-070181
- **SMU-070121** (Submerged membrane unit (two stacked cassette blocks over a diffuser)) → **PMP-080101** (Permeate pump (no descriptive name printed)): through ball valve, butterfly valve, butterfly valve, expansion joint, reducer; crosses sheets
- **SMU-070121** (Submerged membrane unit (two stacked cassette blocks over a diffuser)) → **CONTACT BASIN**: through ball valve, butterfly valve, check valve, FE-080141, reducer, FCV-080132, reducer, reducer, reducer; crosses sheets
- **SMU-070121** (Submerged membrane unit (two stacked cassette blocks over a diffuser)) → **MB-01** (MEMBRANE BIOREACTOR BASIN): through manual valve, XV-070181
- **SMU-070111** (Submerged membrane unit (two stacked cassette blocks over a diffuser)) → **PMP-080101** (Permeate pump (no descriptive name printed)): through ball valve, butterfly valve, butterfly valve, expansion joint, reducer; crosses sheets
- **SMU-070111** (Submerged membrane unit (two stacked cassette blocks over a diffuser)) → **CONTACT BASIN**: through ball valve, butterfly valve, check valve, FE-080141, reducer, FCV-080132, reducer, reducer, reducer; crosses sheets
- **SMU-070111** (Submerged membrane unit (two stacked cassette blocks over a diffuser)) → **MB-01** (MEMBRANE BIOREACTOR BASIN): through manual valve, XV-070181
- **PMP-080101** (Permeate pump (no descriptive name printed)) → **CONTACT BASIN**: through reducer, expansion joint, check valve, butterfly valve, FE-080141, reducer, FCV-080132, reducer, reducer, reducer; crosses sheets

Drains, vents and overflows (not process flow):
- DRAIN ← PMP-080101, SMU, SMU-070111, SMU-070121
- Open end above XV-080112 (unlabelled; VENT TO ATMOSPHERE note at XV-080111 is marked TYP) ← PMP-080101, SMU, SMU-070111, SMU-070121
- VENT TO ATMOSPHERE (TYP) ← SMU, SMU-070111, SMU-070121

## Equipment

| Tag | Kind | Description | Fed by | Feeds | Status | Sheets |
|---|---|---|---|---|---|---|
| AX-01 | tank | ANOXIC BASIN | GRIT REMOVAL TANK | Submersible recycle pump (no tag drawn; instruments numbered 040121), Submersible recycle pump (no tag drawn; instruments numbered 040122), Unlabelled line end beyond valve on basin low-level outlet |  | P-201 |
| BAG OR CONTAINER | bin | BAG OR CONTAINER | FINE SCREEN |  |  | P-101 |
| BLR-090101 | blower | MEMBRANE BIOREACTOR BLOWER 1 | filter | SMU, SMU-070111, SMU-070121 |  | P-205 |
| BLR-100101 | blower | PRE-AERATION BLOWER 1 | filter | FBD-050111 |  | P-205 |
| CONTACT BASIN | tank | CONTACT BASIN | HYPOCHLORITE SOLUTION, PMP-080101, SMU, SMU-070111, SMU-070121 | TANK |  | P-401 |
| FBD-050111 | other | FBD (diffuser symbol on basin floor, fed by process air) | BLR-100101 |  |  | P-202 |
| FINE SCREEN | screen | FINE SCREEN | 3W UTILITY WATER | BAG OR CONTAINER |  | P-101 |
| GRIT REMOVAL TANK | tank | GRIT REMOVAL TANK | MANUAL BAR RACK, Screen channel (open channel with HWWL mark; no tag or label printed) | AX-01 |  | P-101 |
| MANUAL BAR RACK | screen | MANUAL BAR RACK | RS FROM PAHALA, Screen channel (open channel with HWWL mark; no tag or label printed) | GRIT REMOVAL TANK |  | P-101 |
| MB-01 | tank | MEMBRANE BIOREACTOR BASIN | PA-01, SMU, SMU-070111, SMU-070121 | Unlabelled line end beyond valve on basin bottom outlet |  | P-203 |
| MXR-040111 | mixer | Submersible mixer |  |  |  | P-201 |
| PA-01 | tank | PRE-AERATION BASIN | Submersible recycle pump (no tag drawn; instruments numbered 040121), Submersible recycle pump (no tag drawn; instruments numbered 040122) | MB-01, Unlabelled line end beyond valve V-120122 on basin low-level outlet |  | P-202 |
| PMP-080101 | centrifugal_pump | Permeate pump (no descriptive name printed) | SMU, SMU-070111, SMU-070121 | CONTACT BASIN, DRAIN, Open end above XV-080112 (unlabelled; VENT TO ATMOSPHERE note at XV-080111 is marked TYP) |  | P-204 |
| SMU | membrane_filter | SMU- (FUTURE MEMBRANES) | BLR-090101 | CONTACT BASIN, DRAIN, MB-01, Open end above XV-080112 (unlabelled; VENT TO ATMOSPHERE note at XV-080111 is marked TYP), PMP-080101, VENT TO ATMOSPHERE (TYP) | future | P-203 |
| SMU-070111 | membrane_filter | Submerged membrane unit (two stacked cassette blocks over a diffuser) | BLR-090101 | CONTACT BASIN, DRAIN, MB-01, Open end above XV-080112 (unlabelled; VENT TO ATMOSPHERE note at XV-080111 is marked TYP), PMP-080101, VENT TO ATMOSPHERE (TYP) |  | P-203 |
| SMU-070121 | membrane_filter | Submerged membrane unit (two stacked cassette blocks over a diffuser) | BLR-090101 | CONTACT BASIN, DRAIN, MB-01, Open end above XV-080112 (unlabelled; VENT TO ATMOSPHERE note at XV-080111 is marked TYP), PMP-080101, VENT TO ATMOSPHERE (TYP) |  | P-203 |
| Screen channel (open channel with HWWL mark; no tag or label printed) | other | Screen channel (open channel with HWWL mark; no tag or label printed) | RS FROM PAHALA | GRIT REMOVAL TANK, MANUAL BAR RACK |  | P-101 |
| Submersible recycle pump (no tag drawn; instruments numbered 040121) | sump_pump | Submersible recycle pump (no tag drawn; instruments numbered 040121) | AX-01 | PA-01 |  | P-201 |
| Submersible recycle pump (no tag drawn; instruments numbered 040122) | sump_pump | Submersible recycle pump (no tag drawn; instruments numbered 040122) | AX-01 | PA-01 |  | P-201 |
| TANK | tank | TANK | CONTACT BASIN | DRIP ZONE 1, DRIP ZONE 2, DRIP ZONE 3, DRIP ZONE 4 |  | P-401 |
| filter | filter |  |  | BLR-100101 |  | P-205 |
| filter | filter |  |  | BLR-090101 |  | P-205 |

## Instruments

Location is where the instrument senses the process. Pipe locations read `line (upstream item -> downstream item)`.

| Tag | Variable | Function | Mounted | Senses | Loop |
|---|---|---|---|---|---|
| AAH-080001 |  | other | scada |  |  |
| AAL-050102 |  | other | scada |  |  |
| AE-050101 |  | other | field | PA-01 |  |
| AE-050102 |  | other | field | PA-01 |  |
| AE-080001 |  | other | field | line (manual valve -> DRAIN) |  |
| AI (untagged) | analysis | indicator | plc |  |  |
| AIR-050101 |  | other | scada |  |  |
| AIR-050102 |  | other | scada |  |  |
| AIR-080001 |  | other | scada |  |  |
| AIT-050101 |  | other | field |  |  |
| AIT-050102 |  | other | field | PA-01 |  |
| AIT-080001 |  | other | field |  |  |
| AO (untagged) | analysis | other | plc |  |  |
| DI (untagged) | density | indicator | plc |  |  |
| DI (untagged) | density | indicator | plc |  |  |
| DI (untagged) | density | indicator | plc |  |  |
| DI (untagged) | density | indicator | plc |  |  |
| DI (untagged) | density | indicator | plc |  |  |
| DI (untagged) | density | indicator | plc |  |  |
| DO (untagged) | density | other | plc |  |  |
| DO (untagged) | density | other | plc |  |  |
| DO (untagged) | density | other | plc |  |  |
| FAL-040141 |  | other | scada |  |  |
| FAL-070186 |  | other | scada |  |  |
| FC-080132 |  | other | scada |  |  |
| FE-040141 |  | other | field | in-line on line (reducer -> reducer) |  |
| FE-070186 |  | other | field | in-line on 3"-WAS (Untagged square body on the line with a dome (diaphragm-type) actuator on a stem -> manual valve) |  |
| FE-080141 |  | other | field | in-line on line (check valve -> reducer) |  |
| FE-403 | flow | element | field | in-line on line (TANK -> TO EFFLUENT DISPOSAL / REF SHT P-501) | F-403 |
| FI-090101 |  | other | behind_panel | BLR-090101 |  |
| FI-100.002 |  | other | dcs |  |  |
| FI-100101 |  | other | behind_panel | BLR-100101 |  |
| FI-100101#2 |  | other | scada |  |  |
| FIC-040121 |  | other | scada |  |  |
| FIR-040141 |  | other | scada |  |  |
| FIR-070186 |  | other | scada |  |  |
| FIR-403 | flow | indicator | scada |  | F-403 |
| FIT-040141 |  | other | field |  |  |
| FIT-070186 |  | other | field |  |  |
| FIT-080141 |  | other | field |  |  |
| FIT-100,-002 |  | other | field | Flume (open-channel flow element symbol, unlabelled) |  |
| FIT-403 | flow | transmitter | field | in-line on line (TANK -> TO EFFLUENT DISPOSAL / REF SHT P-501) | F-403 |
| FQIR-080141 |  | other | scada |  |  |
| HS-040111 |  | other | local_panel |  |  |
| HS-040121 |  | other | local_panel |  |  |
| HS-070181 |  | other | main_panel |  |  |
| HS-080101 |  | other | local_panel |  |  |
| HS-080111 |  | other | plc |  |  |
| HS-080112 |  | other | plc |  |  |
| HS-500,-101 |  | other | field |  |  |
| I (untagged) | current | other | unknown |  |  |
| JS-040111 |  | other | local_panel |  |  |
| JS-080101 |  | other | local_panel |  |  |
| LAH-001 | level | alarm | scada |  | L-001 |
| LAH-040101 |  | other | scada |  |  |
| LAH-040103 |  | other | scada |  |  |
| LAH-070102 |  | other | scada |  |  |
| LAH-100, |  | other | dcs |  |  |
| LAH-100.125 |  | other | scada |  |  |
| LAH-100.125#2 |  | other | dcs |  |  |
| LAH-402 | level | alarm | scada |  | L-402 |
| LAH-402#2 | level | alarm | dcs |  |  |
| LAL-001 | level | alarm | scada |  | L-001 |
| LAL-040101 |  | other | scada |  |  |
| LAL-040102 |  | other | scada |  |  |
| LAL-070101 |  | other | scada |  |  |
| LCH-001 | level | controller | scada |  | L-001 |
| LCH-001#2 | level | controller | scada |  | L-001#2 |
| LCL-001 | level | controller | scada |  | L-001 |
| LCL-001#2 | level | controller | scada |  | L-001#2 |
| LCL-001#3 | level | controller | scada |  | L-001#3 |
| LDAH-100.. |  | other | dcs |  |  |
| LDAH-100.115 |  | other | scada |  |  |
| LDAH-100.124 |  | other | scada |  |  |
| LDAH-100.124#2 |  | other | dcs |  |  |
| LDI-100.124 |  | other | scada |  |  |
| LE-040101 |  | other | field | AX-01 |  |
| LE-401 | level | element | field | TANK | L-401 |
| LI-001 | level | indicator | scada |  | L-001 |
| LI-100,-124A |  | other | scada |  |  |
| LI-100,-124B |  | other | scada |  |  |
| LI-401 | level | indicator | dcs |  | L-401 |
| LI-402 | level | indicator | main_panel |  | L-402 |
| LIR-040101 |  | other | scada |  |  |
| LIT-100,-114A |  | other | field | Screen channel (open channel with HWWL mark; no tag or label printed) |  |
| LIT-100,-114B |  | other | field | Screen channel (open channel with HWWL mark; no tag or label printed) |  |
| LSH-040103 |  | other | field | AX-01 |  |
| LSH-070102 |  | other | field | MB-01 |  |
| LSH-100, |  | other | field | MANUAL BAR RACK |  |
| LSH-100,-115 |  | other | field | Screen channel (open channel with HWWL mark; no tag or label printed) |  |
| LSH-402 | level | switch | field | TANK | L-402 |
| LSL-040102 |  | other | field | AX-01 |  |
| LSL-070101 |  | other | field | MB-01 |  |
| LT-040101 |  | other | field | AX-01 |  |
| MAH-040111 |  | other | scada |  |  |
| MAH-040121 |  | other | scada |  |  |
| ME-040111 |  | other | field | MXR-040111 |  |
| ME-040121 |  | other | field | Submersible recycle pump (no tag drawn; instruments numbered 040121) |  |
| ME-040122 |  | other | field | Submersible recycle pump (no tag drawn; instruments numbered 040122) |  |
| MS-040111 |  | other | local_panel |  |  |
| MS-040121 |  | other | local_panel |  |  |
| MY-040111 |  | other | local_panel |  |  |
| MY-040121 |  | other | local_panel |  |  |
| OIT (untagged) | user-defined | transmitter | local_panel |  |  |
| OIT (untagged) | user-defined | transmitter | local_panel |  |  |
| PAH-080121 |  | other | scada |  |  |
| PG-080101A |  | other | field | line (butterfly valve -> expansion joint) |  |
| PG-080101B |  | other | field | line (expansion joint -> check valve) |  |
| PIR-080121 |  | other | scada |  |  |
| PT-080121 |  | other | field | line (B / UPPER PERMEATE FROM MB-01 / REF SHT P203 -> check valve) |  |
| SC-090101 |  | other | behind_panel | BLR-090101 |  |
| SC-100101 |  | other | behind_panel | BLR-100101 |  |
| SC-100101#2 |  | other | scada |  |  |
| SS-040121 |  | other | local_panel |  |  |
| TAH-040111 |  | other | scada |  |  |
| TAH-040121 |  | other | scada |  |  |
| TAL-050102 |  | other | scada |  |  |
| TIR-050102 |  | other | scada |  |  |
| TIT-050102 |  | other | field |  |  |
| TSH-040111 |  | other | field | MXR-040111 |  |
| TSH-040121 |  | other | field | Submersible recycle pump (no tag drawn; instruments numbered 040121) |  |
| TSH-040122 |  | other | field | Submersible recycle pump (no tag drawn; instruments numbered 040122) |  |
| TY-040111 |  | other | local_panel |  |  |
| TY-040121 |  | other | local_panel |  |  |
| VCP-100, |  | other | local_panel |  |  |
| VFD-040121 |  | other | local_panel |  |  |
| VFD-090101 |  | other | behind_panel |  |  |
| VFD-100101 |  | other | behind_panel |  |  |
| XC-080111 |  | other | scada |  |  |
| XC-080112 |  | other | scada |  |  |
| XC-090101A |  | other | behind_panel | BLR-090101 |  |
| XC-090101B |  | other | behind_panel | BLR-090101 |  |
| XC-090101C |  | other | behind_panel | BLR-090101 |  |
| XC-100101A |  | other | behind_panel | BLR-100101 |  |
| XC-100101A#2 |  | other | scada |  |  |
| XC-100101B |  | other | behind_panel | BLR-100101 |  |
| XC-100101B#2 |  | other | scada |  |  |
| XC-100101C |  | other | behind_panel | BLR-100101 |  |
| XC-100101C#2 |  | other | scada |  |  |
| YA-001 | event/state | alarm | scada |  |  |
| YA-007 | event/state | alarm | scada |  |  |
| YA-090101A |  | other | behind_panel | BLR-090101 |  |
| YA-090101B |  | other | behind_panel | BLR-090101 |  |
| YA-100101A |  | other | behind_panel | BLR-100101 |  |
| YA-100101A#2 |  | other | scada |  |  |
| YA-100101B |  | other | behind_panel | BLR-100101 |  |
| YA-100101B#2 |  | other | scada |  |  |
| YA-500,-101 |  | other | scada |  |  |
| YA-500,-101#2 |  | other | dcs |  |  |
| YC-040111 |  | other | scada |  |  |
| YC-040121 |  | other | scada |  |  |
| YC-070181 |  | other | scada |  |  |
| YC-080101 |  | other | scada |  |  |
| YI-040111A |  | other | scada |  |  |
| YI-040111B |  | other | scada |  |  |
| YI-040121A |  | other | scada |  |  |
| YI-040121B |  | other | scada |  |  |
| YI-070181 |  | other | scada |  |  |
| YI-080101A |  | other | scada |  |  |
| YI-080101B |  | other | scada |  |  |
| YI-080111 |  | other | scada |  |  |
| YI-080112 |  | other | scada |  |  |
| YI-090101A |  | other | behind_panel | BLR-090101 |  |
| YI-090101B |  | other | behind_panel | BLR-090101 |  |
| YI-090101C |  | other | behind_panel | BLR-090101 |  |
| YI-090101D |  | other | behind_panel | BLR-090101 |  |
| YI-100, |  | other | scada |  |  |
| YI-100,#2 |  | other | scada |  |  |
| YI-100101A |  | other | behind_panel | BLR-100101 |  |
| YI-100101A#2 |  | other | scada |  |  |
| YI-100101B |  | other | behind_panel | BLR-100101 |  |
| YI-100101B#2 |  | other | scada |  |  |
| YI-100101C |  | other | behind_panel | BLR-100101 |  |
| YI-100101C#2 |  | other | scada |  |  |
| YI-100101D |  | other | behind_panel | BLR-100101 |  |
| YI-100101D#2 |  | other | scada |  |  |
| YI-500,-101 |  | other | scada |  |  |
| YI-500,-101#2 |  | other | scada |  |  |
| YI-500,-101#3 |  | other | scada |  |  |
| YI-500,-101#4 |  | other | dcs |  |  |
| ZA-040101 |  | other | scada |  |  |
| ZA-040121 |  | other | scada |  |  |
| ZA-070181 |  | other | scada |  |  |
| ZA-080101 |  | other | scada |  |  |
| ZA-080132 |  | other | scada |  |  |
| ZCC-500,-101 |  | other | dcs |  |  |
| ZCO-500,-101 |  | other | dcs |  |  |
| ZIC-070181 |  | other | scada |  |  |
| ZIC-080132 |  | other | scada |  |  |
| ZIC-500,-101 |  | other | scada |  |  |
| ZIC-500,-101#2 |  | other | dcs |  |  |
| ZIO-070181 |  | other | scada |  |  |
| ZIO-500,-101 |  | other | scada |  |  |
| ZIO-500,-101#2 |  | other | dcs |  |  |
| ZSC-070181 |  | other | field | XV-070181 |  |
| ZSC-080132 |  | other | field | FCV-080132 |  |
| ZSC-500,-101 |  | other | field | motor operated valve |  |
| ZSC-500,-201 |  | other | field | motor operated valve |  |
| ZSC-500,-201#2 |  | other | field | motor operated valve |  |
| ZSC-500,-301 |  | other | field | motor operated valve |  |
| ZSO-070181 |  | other | field | XV-070181 |  |
| ZSO-500,-101 |  | other | field | motor operated valve |  |
| ZSO-500,-201 |  | other | field | motor operated valve |  |
| ZSO-500,-201#2 |  | other | field | motor operated valve |  |
| ZSO-500,-301 |  | other | field | motor operated valve |  |

## Control loops

| Loop | Type | Sensor(s) | Controller(s) | Final element(s) | Description |
|---|---|---|---|---|---|
| F-403 | monitoring | FIT-403, FE-403 |  |  | Monitoring loop F-403 (flow). Sensed by FIT-403, FE-403 (in-line on line (TANK -> TO EFFLUENT DISPOSAL / REF SHT P-501)). |
| L-001 | control |  | LCH-001, LCL-001 |  | Control loop L-001 (level). Controlled by LCH-001, LCL-001 (scada). |
| L-001#2 | control |  | LCH-001#2, LCL-001#2 |  | Control loop L-001#2 (level). Controlled by LCH-001#2, LCL-001#2 (scada). |
| L-001#3 | control |  | LCL-001#3 |  | Control loop L-001#3 (level). Controlled by LCL-001#3 (scada). |
| L-401 | monitoring | LE-401 |  |  | Monitoring loop L-401 (level). Sensed by LE-401 (TANK). |
| L-402 | monitoring | LSH-402 |  |  | Monitoring loop L-402 (level). Sensed by LSH-402 (TANK). |

## Off-page connections

| Sheet | Connector | Direction | Other drawing | Linked to |
|---|---|---|---|---|
| P-101 | TO MBR | out |  | A / SCREENED INFLT. FROM HEADWORKS / REF SHT P101 (P-201) |
| P-201 | A / EQUIPMENT GAL PS INFLUENT / REF SHT P208 | in | P-208 | unmatched |
| P-201 | A / SCREENED INFLT. FROM HEADWORKS / REF SHT P101 | in | P-101 | TO MBR (P-101) |
| P-201 | A / pH ADJUSTMENT / REF SHT P207 | in | P-207 | unmatched |
| P-201 | b / RECYCLE TO PA-01 / REF SHT P202 | out | P-202 | B / RECYCLE FROM AX-01 / REF SHT P201 (P-202) |
| P-202 | A / PROCESS AIR FROM BLOWERS / REF SHT P205 | in | P-205 | PROCESS AIR TO PA-01 REF SHT P-202 (P-205) |
| P-202 | B / RECYCLE FROM AX-01 / REF SHT P201 | in | P-201 | b / RECYCLE TO PA-01 / REF SHT P202 (P-201) |
| P-202 | a / OVERFLOW TO MBR BASIN / REF SHT P203 | out | P-203 | A / OVERFLOW FROM PRE-AERATION BASIN / REF SHT P202 (P-203) |
| P-203 | A / ACID WASH / REF SHT P206 | in | P-206 | unmatched |
| P-203 | C / PROCESS AIR FROM BLOWERS / REF SHT P205 | in | P-205 | PROCESS AIR TO MB-01 REF SHT P-203 (P-205) |
| P-203 | b / UPPER PERMEATE TO COLLECTION / REF SHT P204 | out | P-204 | B / UPPER PERMEATE FROM MB-01 / REF SHT P203 (P-204) |
| P-203 | c / LOWER PERMEATE TO COLLECTION / REF SHT P204 | out | P-204 | C / LOWER PERMEATE FROM MB-01 / REF SHT P203 (P-204) |
| P-203 | A / OVERFLOW FROM PRE-AERATION BASIN / REF SHT P202 | in | P-202 | a / OVERFLOW TO MBR BASIN / REF SHT P203 (P-202) |
| P-203 | e / WAS TO WAS-01 / REF SHT P210 | out | P-210 | unmatched |
| P-204 | B / UPPER PERMEATE FROM MB-01 / REF SHT P203 | in | P-203 | b / UPPER PERMEATE TO COLLECTION / REF SHT P204 (P-203) |
| P-204 | C / LOWER PERMEATE FROM MB-01 / REF SHT P203 | in | P-203 | c / LOWER PERMEATE TO COLLECTION / REF SHT P204 (P-203) |
| P-204 | a / PERMEATE TO DISINFECTION | out |  | FROM PERMEATE COLLECTION / REF SHT P-204 (P-401) |
| P-205 | PROCESS AIR FROM STD-BY BLR. REF SHT P-209 | in | P-209 | unmatched |
| P-205 | PROCESS AIR TO MB-01 REF SHT P-203 | out | P-203 | C / PROCESS AIR FROM BLOWERS / REF SHT P205 (P-203) |
| P-205 | PROCESS AIR TO PA-01 REF SHT P-202 | out | P-202 | A / PROCESS AIR FROM BLOWERS / REF SHT P205 (P-202) |
| P-401 | FROM PERMEATE COLLECTION / REF SHT P-204 | in | P-204 | a / PERMEATE TO DISINFECTION (P-204) |
| P-401 | TO EFFLUENT DISPOSAL / REF SHT P-501 | out | P-501 | IRRIGATION EQUALIZATION TANK (P-501) |
| P-501 | IRRIGATION EQUALIZATION TANK | in |  | TO EFFLUENT DISPOSAL / REF SHT P-501 (P-401) |

## Data quality

0 errors, 47 warnings and 182 informational items; see `qa_report.md`. Every node carries `confidence` and the sheet region it was read from (`provenance`). This graph was machine-extracted from drawings and must be verified by a qualified engineer before use in design, operations or safety work.
