# QA report: Pahala WWTP

Generated 2026-11-10T19:56:07+00:00 by pid-to-kg 0.1.0.

**0 errors, 47 warnings, 182 info.**

Errors must be fixed in the page extraction files before the graph is trusted. Warnings are things to re-check on the drawing (the *Re-check* column names the tiles). Info items are for the record.

| Severity | Code | Count |
|---|---|---|
| warning | `component_not_connected` | 1 |
| warning | `duplicate_tag` | 26 |
| warning | `loop_no_final_element` | 3 |
| warning | `name_conflict` | 6 |
| warning | `possible_missed_tags` | 6 |
| warning | `unmatched_off_page` | 5 |
| info | `inferred_flow_direction` | 1 |
| info | `isolated_instrument` | 2 |
| info | `loop_no_sensor` | 3 |
| info | `low_confidence` | 4 |
| info | `non_isa_tag` | 172 |

## Details

| Severity | Page | Code | Item | Message | Re-check |
|---|---|---|---|---|---|
| warning |  | `loop_no_final_element` | LOOP:L-001 | control loop L-001 has a controller but no final element |  |
| warning |  | `loop_no_final_element` | LOOP:L-001#2 | control loop L-001#2 has a controller but no final element |  |
| warning |  | `loop_no_final_element` | LOOP:L-001#3 | control loop L-001#3 has a controller but no final element |  |
| warning | 9 | `duplicate_tag` | LAH-100.125#2 | tag 'LAH-100.125' is used by more than one item on this sheet; the copy 'LAH-100.125_MCP' was kept separate as 'LAH-100.125#2' | r1c2 |
| warning | 9 | `duplicate_tag` | LDAH-100.124#2 | tag 'LDAH-100.124' is used by more than one item on this sheet; the copy 'LDAH-100.124_MCP' was kept separate as 'LDAH-100.124#2' | r1c2 |
| warning | 9 | `duplicate_tag` | YI-100,#2 | tag 'YI-100,' is used by more than one item on this sheet; the copy 'YI-100_RUN' was kept separate as 'YI-100,#2' | r1c3 |
| warning | 9 | `name_conflict` | LCH-001 | 'LCH-001' is described as 'FLOW METER VAULT' on SHEET:P-101 and as 'HI LEVEL SP' on SHEET:P-401 | r1c1 |
| warning | 9 | `name_conflict` | LAH-001 | 'LAH-001' is described as 'HIGH INFLUENT FLOW' on SHEET:P-101 and as 'TANK LEVEL HI' on SHEET:P-401 | r1c1 |
| warning | 9 | `name_conflict` | LCL-001 | 'LCL-001' is described as 'INFLUENT FLOW TOTAL YSTDAY' on SHEET:P-101 and as 'LO LEVEL SP' on SHEET:P-401 | r1c1 |
| warning | 9 | `name_conflict` | LAL-001 | 'LAL-001' is described as 'INFLUENT TOTAL TODAY' on SHEET:P-101 and as 'TANK LEVEL LOW' on SHEET:P-401 | r1c1 |
| warning | 9 | `name_conflict` | YA-001 | 'YA-001' is described as 'INFLUENT FLOW TOTAL' on SHEET:P-101 and as 'XMTR FAULT' on SHEET:P-401 | r1c1 |
| warning | 9 | `name_conflict` | LI-001 | 'LI-001' is described as 'INFLUENT FLOW RATE' on SHEET:P-101 and as 'TANK LEVEL' on SHEET:P-401 | r1c1 |
| warning | 9 | `possible_missed_tags` |  | 1 tags found by text_layer are not in the graph: FIT-120V |  |
| warning | 10 | `possible_missed_tags` |  | 1 tags found by text_layer are not in the graph: SUITE-201 |  |
| warning | 10 | `unmatched_off_page` | P10.OPC1 | off-page connector 'A / EQUIPMENT GAL PS INFLUENT / REF SHT P208' (from P-208) has no matching connector or item | r2c1, r3c1 |
| warning | 10 | `unmatched_off_page` | P10.OPC3 | off-page connector 'A / pH ADJUSTMENT / REF SHT P207' (from P-207) has no matching connector or item | r2c1, r3c1 |
| warning | 11 | `possible_missed_tags` |  | 1 tags found by text_layer are not in the graph: SUITE-201 |  |
| warning | 12 | `component_not_connected` | P12.V10 | component manual valve is not on any line (add it to a line 'path') | r2c2, r2c3 |
| warning | 12 | `possible_missed_tags` |  | 1 tags found by text_layer are not in the graph: SUITE-201 |  |
| warning | 12 | `unmatched_off_page` | P12.OPC6 | off-page connector 'e / WAS TO WAS-01 / REF SHT P210' (to P-210) has no matching connector or item | r3c4 |
| warning | 12 | `unmatched_off_page` | P12.OPC1 | off-page connector 'A / ACID WASH / REF SHT P206' (from P-206) has no matching connector or item | r1c1, r2c1 |
| warning | 13 | `possible_missed_tags` |  | 1 tags found by text_layer are not in the graph: SUITE-201 |  |
| warning | 14 | `duplicate_tag` | YI-100101A#2 | tag 'YI-100101A' is used by more than one item on this sheet; the copy 'YI-100101A-HMI' was kept separate as 'YI-100101A#2' | r1c1 |
| warning | 14 | `duplicate_tag` | YI-100101B#2 | tag 'YI-100101B' is used by more than one item on this sheet; the copy 'YI-100101B-HMI' was kept separate as 'YI-100101B#2' | r1c1 |
| warning | 14 | `duplicate_tag` | YI-100101C#2 | tag 'YI-100101C' is used by more than one item on this sheet; the copy 'YI-100101C-HMI' was kept separate as 'YI-100101C#2' | r1c1 |
| warning | 14 | `duplicate_tag` | YI-100101D#2 | tag 'YI-100101D' is used by more than one item on this sheet; the copy 'YI-100101D-HMI' was kept separate as 'YI-100101D#2' | r1c1 |
| warning | 14 | `duplicate_tag` | YA-100101A#2 | tag 'YA-100101A' is used by more than one item on this sheet; the copy 'YA-100101A-HMI' was kept separate as 'YA-100101A#2' | r1c1 |
| warning | 14 | `duplicate_tag` | YA-100101B#2 | tag 'YA-100101B' is used by more than one item on this sheet; the copy 'YA-100101B-HMI' was kept separate as 'YA-100101B#2' | r1c1, r1c2 |
| warning | 14 | `duplicate_tag` | XC-100101A#2 | tag 'XC-100101A' is used by more than one item on this sheet; the copy 'XC-100101A-HMI' was kept separate as 'XC-100101A#2' | r1c1, r1c2 |
| warning | 14 | `duplicate_tag` | XC-100101B#2 | tag 'XC-100101B' is used by more than one item on this sheet; the copy 'XC-100101B-HMI' was kept separate as 'XC-100101B#2' | r1c2 |
| warning | 14 | `duplicate_tag` | XC-100101C#2 | tag 'XC-100101C' is used by more than one item on this sheet; the copy 'XC-100101C-HMI' was kept separate as 'XC-100101C#2' | r1c2 |
| warning | 14 | `duplicate_tag` | SC-100101#2 | tag 'SC-100101' is used by more than one item on this sheet; the copy 'SC-100101-HMI' was kept separate as 'SC-100101#2' | r1c2 |
| warning | 14 | `duplicate_tag` | FI-100101#2 | tag 'FI-100101' is used by more than one item on this sheet; the copy 'FI-100101-HMI' was kept separate as 'FI-100101#2' | r1c2 |
| warning | 14 | `possible_missed_tags` |  | 1 tags found by text_layer are not in the graph: SUITE-201 |  |
| warning | 14 | `unmatched_off_page` | P14.OPC-B | off-page connector 'PROCESS AIR FROM STD-BY BLR. REF SHT P-209' (from P-209) has no matching connector or item | r3c1 |
| warning | 21 | `duplicate_tag` | LCH-001#2 | tag 'LCH-001' is used by more than one item on this sheet; the copy 'LCH-001_LEAD' was kept separate as 'LCH-001#2' | r1c2 |
| warning | 21 | `duplicate_tag` | LCL-001#2 | tag 'LCL-001' is used by more than one item on this sheet; the copy 'LCL-001_LAG' was kept separate as 'LCL-001#2' | r1c2 |
| warning | 21 | `duplicate_tag` | LCL-001#3 | tag 'LCL-001' is used by more than one item on this sheet; the copy 'LCL-001_STOP' was kept separate as 'LCL-001#3' | r1c2 |
| warning | 21 | `duplicate_tag` | LAH-402#2 | tag 'LAH-402' is used by more than one item on this sheet; the copy 'LAH-402_PNL' was kept separate as 'LAH-402#2' | r1c2 |
| warning | 22 | `duplicate_tag` | YI-500,-101#2 | tag 'YI-500,-101' is used by more than one item on this sheet; the copy 'YI-500,101-S2' was kept separate as 'YI-500,-101#2' | r1c2 |
| warning | 22 | `duplicate_tag` | YI-500,-101#3 | tag 'YI-500,-101' is used by more than one item on this sheet; the copy 'YI-500,101-S3' was kept separate as 'YI-500,-101#3' | r1c2 |
| warning | 22 | `duplicate_tag` | ZIO-500,-101#2 | tag 'ZIO-500,-101' is used by more than one item on this sheet; the copy 'ZIO-500,101' was kept separate as 'ZIO-500,-101#2' | r1c1 |
| warning | 22 | `duplicate_tag` | ZIC-500,-101#2 | tag 'ZIC-500,-101' is used by more than one item on this sheet; the copy 'ZIC-500,101' was kept separate as 'ZIC-500,-101#2' | r1c1, r1c2 |
| warning | 22 | `duplicate_tag` | YA-500,-101#2 | tag 'YA-500,-101' is used by more than one item on this sheet; the copy 'YA-500,101' was kept separate as 'YA-500,-101#2' | r1c2 |
| warning | 22 | `duplicate_tag` | YI-500,-101#4 | tag 'YI-500,-101' is used by more than one item on this sheet; the copy 'YI-500,101' was kept separate as 'YI-500,-101#4' | r1c2 |
| warning | 22 | `duplicate_tag` | ZSO-500,-201#2 | tag 'ZSO-500,-201' is used by more than one item on this sheet; the copy 'ZSO-500,201-Z4' was kept separate as 'ZSO-500,-201#2' | r3c2, r3c3 |
| warning | 22 | `duplicate_tag` | ZSC-500,-201#2 | tag 'ZSC-500,-201' is used by more than one item on this sheet; the copy 'ZSC-500,201-Z4' was kept separate as 'ZSC-500,-201#2' | r3c3 |
| info |  | `inferred_flow_direction` |  | 156 flow edges have inferred (not drawn) direction |  |
| info |  | `loop_no_sensor` | LOOP:L-001 | control loop L-001 has a controller but no sensor |  |
| info |  | `loop_no_sensor` | LOOP:L-001#2 | control loop L-001#2 has a controller but no sensor |  |
| info |  | `loop_no_sensor` | LOOP:L-001#3 | control loop L-001#3 has a controller but no sensor |  |
| info | 9 | `non_isa_tag` | FI-100.002 | instrument tag 'FI 100.002' does not parse as ISA-5.1 | r1c1 |
| info | 9 | `non_isa_tag` | FIT-100,-002 | instrument tag 'FIT 100, 002' does not parse as ISA-5.1 | r2c1 |
| info | 9 | `non_isa_tag` | LAH-100.125 | instrument tag 'LAH 100.125' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LDAH-100.124 | instrument tag 'LDAH 100.124' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LDAH-100.115 | instrument tag 'LDAH 100.115' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LAH-100.125 | instrument tag 'LAH 100.125' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LDAH-100.124 | instrument tag 'LDAH 100.124' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LDAH-100.. | instrument tag 'LDAH 100..' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LI-100,-124A | instrument tag 'LI 100, 124A' does not parse as ISA-5.1 | r1c2 |
| info | 9 | `non_isa_tag` | LI-100,-124B | instrument tag 'LI 100, 124B' does not parse as ISA-5.1 | r1c2, r1c3 |
| info | 9 | `non_isa_tag` | LDI-100.124 | instrument tag 'LDI 100.124' does not parse as ISA-5.1 | r1c2, r1c3 |
| info | 9 | `non_isa_tag` | YI-100, | instrument tag 'YI 100,' does not parse as ISA-5.1 | r1c3 |
| info | 9 | `non_isa_tag` | YI-100, | instrument tag 'YI 100,' does not parse as ISA-5.1 | r1c3 |
| info | 9 | `non_isa_tag` | LAH-100, | instrument tag 'LAH 100,' does not parse as ISA-5.1 | r1c3 |
| info | 9 | `non_isa_tag` | LSH-100, | instrument tag 'LSH 100,' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 9 | `non_isa_tag` | VCP-100, | instrument tag 'VCP 100,' does not parse as ISA-5.1 | r2c2 |
| info | 9 | `non_isa_tag` | LSH-100,-115 | instrument tag 'LSH 100, 115' does not parse as ISA-5.1 | r2c2 |
| info | 9 | `non_isa_tag` | LIT-100,-114A | instrument tag 'LIT 100, 114A' does not parse as ISA-5.1 | r2c2 |
| info | 9 | `non_isa_tag` | LIT-100,-114B | instrument tag 'LIT 100, 114B' does not parse as ISA-5.1 | r2c2, r2c3 |
| info | 10 | `low_confidence` | BOUNDARY:UNLABELLED LINE END BEYOND VALVE ON BASIN LOW-LEVEL OUTLET | Unlabelled line end beyond valve on basin low-level outlet was read with confidence 0.50 | r2c3, r2c4 |
| info | 10 | `non_isa_tag` | YI-040111A | instrument tag 'YI-040111A' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 10 | `non_isa_tag` | YC-040111 | instrument tag 'YC-040111' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | YI-040111B | instrument tag 'YI-040111B' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | TAH-040111 | instrument tag 'TAH-040111' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | MAH-040111 | instrument tag 'MAH-040111' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | ZA-040101 | instrument tag 'ZA-040101' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | LAL-040102 | instrument tag 'LAL-040102' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | LAH-040103 | instrument tag 'LAH-040103' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | LIR-040101 | instrument tag 'LIR-040101' does not parse as ISA-5.1 | r1c2 |
| info | 10 | `non_isa_tag` | LAH-040101 | instrument tag 'LAH-040101' does not parse as ISA-5.1 | r1c2, r1c3 |
| info | 10 | `non_isa_tag` | LAL-040101 | instrument tag 'LAL-040101' does not parse as ISA-5.1 | r1c2, r1c3 |
| info | 10 | `non_isa_tag` | FIC-040121 | instrument tag 'FIC-040121' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | YI-040121A | instrument tag 'YI-040121A' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | YC-040121 | instrument tag 'YC-040121' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | YI-040121B | instrument tag 'YI-040121B' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | TAH-040121 | instrument tag 'TAH-040121' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | MAH-040121 | instrument tag 'MAH-040121' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | ZA-040121 | instrument tag 'ZA-040121' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | FIR-040141 | instrument tag 'FIR-040141' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | FAL-040141 | instrument tag 'FAL-040141' does not parse as ISA-5.1 | r1c3 |
| info | 10 | `non_isa_tag` | JS-040111 | instrument tag 'JS-040111' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 10 | `non_isa_tag` | HS-040111 | instrument tag 'HS-040111' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 10 | `non_isa_tag` | TY-040111 | instrument tag 'TY-040111' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 10 | `non_isa_tag` | SS-040121 | instrument tag 'SS-040121' does not parse as ISA-5.1 | r1c2, r1c3 |
| info | 10 | `non_isa_tag` | VFD-040121 | instrument tag 'VFD-040121' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 10 | `non_isa_tag` | HS-040121 | instrument tag 'HS-040121' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 10 | `non_isa_tag` | TY-040121 | instrument tag 'TY-040121' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 10 | `non_isa_tag` | MY-040111 | instrument tag 'MY-040111' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 10 | `non_isa_tag` | MS-040111 | instrument tag 'MS-040111' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 10 | `non_isa_tag` | MY-040121 | instrument tag 'MY-040121' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 10 | `non_isa_tag` | MS-040121 | instrument tag 'MS-040121' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 10 | `non_isa_tag` | TSH-040111 | instrument tag 'TSH-040111' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 10 | `non_isa_tag` | ME-040111 | instrument tag 'ME-040111' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 10 | `non_isa_tag` | LSL-040102 | instrument tag 'LSL-040102' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 10 | `non_isa_tag` | LSH-040103 | instrument tag 'LSH-040103' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 10 | `non_isa_tag` | LT-040101 | instrument tag 'LT-040101' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 10 | `non_isa_tag` | LE-040101 | instrument tag 'LE-040101' does not parse as ISA-5.1 | r3c2 |
| info | 10 | `non_isa_tag` | TSH-040121 | instrument tag 'TSH-040121' does not parse as ISA-5.1 | r2c2, r2c3 |
| info | 10 | `non_isa_tag` | ME-040121 | instrument tag 'ME-040121' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 10 | `non_isa_tag` | TSH-040122 | instrument tag 'TSH-040122' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 10 | `non_isa_tag` | ME-040122 | instrument tag 'ME-040122' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 10 | `non_isa_tag` | FIT-040141 | instrument tag 'FIT-040141' does not parse as ISA-5.1 | r2c3 |
| info | 10 | `non_isa_tag` | FE-040141 | instrument tag 'FE-040141' does not parse as ISA-5.1 | r2c3 |
| info | 11 | `low_confidence` | BOUNDARY:UNLABELLED LINE END BEYOND VALVE V-120122 ON BASIN LOW-LEVEL OUTLET | Unlabelled line end beyond valve V-120122 on basin low-level outlet was read with confidence 0.50 | r2c3, r2c4 |
| info | 11 | `non_isa_tag` | AE-050101 | instrument tag 'AE-050101' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 11 | `non_isa_tag` | AIT-050101 | instrument tag 'AIT-050101' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 11 | `non_isa_tag` | AIR-050101 | instrument tag 'AIR-050101' does not parse as ISA-5.1 | r1c3 |
| info | 11 | `non_isa_tag` | AE-050102 | instrument tag 'AE-050102' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 11 | `non_isa_tag` | TIT-050102 | instrument tag 'TIT-050102' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 11 | `non_isa_tag` | AIT-050102 | instrument tag 'AIT-050102' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 11 | `non_isa_tag` | TIR-050102 | instrument tag 'TIR-050102' does not parse as ISA-5.1 | r1c3 |
| info | 11 | `non_isa_tag` | AIR-050102 | instrument tag 'AIR-050102' does not parse as ISA-5.1 | r1c3 |
| info | 11 | `non_isa_tag` | TAL-050102 | instrument tag 'TAL-050102' does not parse as ISA-5.1 | r1c3 |
| info | 11 | `non_isa_tag` | AAL-050102 | instrument tag 'AAL-050102' does not parse as ISA-5.1 | r1c3 |
| info | 12 | `low_confidence` | P12.V10 | manual valve was read with confidence 0.50 | r2c2, r2c3 |
| info | 12 | `low_confidence` | BOUNDARY:UNLABELLED LINE END BEYOND VALVE ON BASIN BOTTOM OUTLET | Unlabelled line end beyond valve on basin bottom outlet was read with confidence 0.50 | r2c1, r3c1 |
| info | 12 | `non_isa_tag` | ZA-070181 | instrument tag 'ZA-070181' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 12 | `non_isa_tag` | ZIC-070181 | instrument tag 'ZIC-070181' does not parse as ISA-5.1 | r1c2 |
| info | 12 | `non_isa_tag` | ZIO-070181 | instrument tag 'ZIO-070181' does not parse as ISA-5.1 | r1c2 |
| info | 12 | `non_isa_tag` | YC-070181 | instrument tag 'YC-070181' does not parse as ISA-5.1 | r1c2 |
| info | 12 | `non_isa_tag` | YI-070181 | instrument tag 'YI-070181' does not parse as ISA-5.1 | r1c2 |
| info | 12 | `non_isa_tag` | HS-070181 | instrument tag 'HS-070181' does not parse as ISA-5.1 | r1c2 |
| info | 12 | `non_isa_tag` | ZSO-070181 | instrument tag 'ZSO-070181' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 12 | `non_isa_tag` | ZSC-070181 | instrument tag 'ZSC-070181' does not parse as ISA-5.1 | r2c2 |
| info | 12 | `non_isa_tag` | LAL-070101 | instrument tag 'LAL-070101' does not parse as ISA-5.1 | r1c3 |
| info | 12 | `non_isa_tag` | LAH-070102 | instrument tag 'LAH-070102' does not parse as ISA-5.1 | r1c3 |
| info | 12 | `non_isa_tag` | LSL-070101 | instrument tag 'LSL-070101' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 12 | `non_isa_tag` | LSH-070102 | instrument tag 'LSH-070102' does not parse as ISA-5.1 | r2c3, r3c3 |
| info | 12 | `non_isa_tag` | FIR-070186 | instrument tag 'FIR-070186' does not parse as ISA-5.1 | r1c3 |
| info | 12 | `non_isa_tag` | FAL-070186 | instrument tag 'FAL-070186' does not parse as ISA-5.1 | r1c3 |
| info | 12 | `non_isa_tag` | FIT-070186 | instrument tag 'FIT-070186' does not parse as ISA-5.1 | r2c3, r2c4 |
| info | 12 | `non_isa_tag` | FE-070186 | instrument tag 'FE-070186' does not parse as ISA-5.1 | r3c3, r3c4 |
| info | 13 | `non_isa_tag` | XC-080111 | instrument tag 'XC-080111' does not parse as ISA-5.1 | r1c1 |
| info | 13 | `non_isa_tag` | YI-080111 | instrument tag 'YI-080111' does not parse as ISA-5.1 | r1c1 |
| info | 13 | `non_isa_tag` | PIR-080121 | instrument tag 'PIR-080121' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 13 | `non_isa_tag` | PAH-080121 | instrument tag 'PAH-080121' does not parse as ISA-5.1 | r1c2 |
| info | 13 | `non_isa_tag` | YI-080101A | instrument tag 'YI-080101A' does not parse as ISA-5.1 | r1c2 |
| info | 13 | `non_isa_tag` | YC-080101 | instrument tag 'YC-080101' does not parse as ISA-5.1 | r1c2 |
| info | 13 | `non_isa_tag` | YI-080101B | instrument tag 'YI-080101B' does not parse as ISA-5.1 | r1c2 |
| info | 13 | `non_isa_tag` | ZA-080101 | instrument tag 'ZA-080101' does not parse as ISA-5.1 | r1c2 |
| info | 13 | `non_isa_tag` | XC-080112 | instrument tag 'XC-080112' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | YI-080112 | instrument tag 'YI-080112' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | FQIR-080141 | instrument tag 'FQIR-080141' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | AAH-080001 | instrument tag 'AAH-080001' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | AIR-080001 | instrument tag 'AIR-080001' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | ZA-080132 | instrument tag 'ZA-080132' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | FC-080132 | instrument tag 'FC-080132' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | ZIC-080132 | instrument tag 'ZIC-080132' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | HS-080111 | instrument tag 'HS-080111' does not parse as ISA-5.1 | r1c1 |
| info | 13 | `non_isa_tag` | HS-080112 | instrument tag 'HS-080112' does not parse as ISA-5.1 | r1c3 |
| info | 13 | `non_isa_tag` | HS-080101 | instrument tag 'HS-080101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 13 | `non_isa_tag` | JS-080101 | instrument tag 'JS-080101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 13 | `non_isa_tag` | PT-080121 | instrument tag 'PT-080121' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 13 | `non_isa_tag` | PG-080101A | instrument tag 'PG-080101A' does not parse as ISA-5.1 | r2c2 |
| info | 13 | `non_isa_tag` | PG-080101B | instrument tag 'PG-080101B' does not parse as ISA-5.1 | r2c2, r2c3 |
| info | 13 | `non_isa_tag` | FE-080141 | instrument tag 'FE-080141' does not parse as ISA-5.1 | r2c3 |
| info | 13 | `non_isa_tag` | FIT-080141 | instrument tag 'FIT-080141' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 13 | `non_isa_tag` | AE-080001 | instrument tag 'AE-080001' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 13 | `non_isa_tag` | AIT-080001 | instrument tag 'AIT-080001' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 13 | `non_isa_tag` | ZSC-080132 | instrument tag 'ZSC-080132' does not parse as ISA-5.1 | r1c3, r2c3 |
| info | 14 | `isolated_instrument` | P14.OIT-100101 | OIT (untagged) has no connections at all | r1c1, r2c1 |
| info | 14 | `isolated_instrument` | P14.OIT-090101 | OIT (untagged) has no connections at all | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | VFD-100101 | instrument tag 'VFD-100101' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101A | instrument tag 'YI-100101A' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101B | instrument tag 'YI-100101B' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101C | instrument tag 'YI-100101C' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101D | instrument tag 'YI-100101D' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YA-100101A | instrument tag 'YA-100101A' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YA-100101B | instrument tag 'YA-100101B' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 14 | `non_isa_tag` | XC-100101A | instrument tag 'XC-100101A' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 14 | `non_isa_tag` | XC-100101B | instrument tag 'XC-100101B' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | XC-100101C | instrument tag 'XC-100101C' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | SC-100101 | instrument tag 'SC-100101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | FI-100101 | instrument tag 'FI-100101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | VFD-090101 | instrument tag 'VFD-090101' does not parse as ISA-5.1 | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | YI-090101A | instrument tag 'YI-090101A' does not parse as ISA-5.1 | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | YI-090101B | instrument tag 'YI-090101B' does not parse as ISA-5.1 | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | YI-090101C | instrument tag 'YI-090101C' does not parse as ISA-5.1 | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | YI-090101D | instrument tag 'YI-090101D' does not parse as ISA-5.1 | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | YA-090101A | instrument tag 'YA-090101A' does not parse as ISA-5.1 | r2c1, r3c1 |
| info | 14 | `non_isa_tag` | YA-090101B | instrument tag 'YA-090101B' does not parse as ISA-5.1 | r2c1, r2c2 |
| info | 14 | `non_isa_tag` | XC-090101A | instrument tag 'XC-090101A' does not parse as ISA-5.1 | r2c1, r2c2 |
| info | 14 | `non_isa_tag` | XC-090101B | instrument tag 'XC-090101B' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 14 | `non_isa_tag` | XC-090101C | instrument tag 'XC-090101C' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 14 | `non_isa_tag` | SC-090101 | instrument tag 'SC-090101' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 14 | `non_isa_tag` | FI-090101 | instrument tag 'FI-090101' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 14 | `non_isa_tag` | YI-100101A | instrument tag 'YI-100101A' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101B | instrument tag 'YI-100101B' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101C | instrument tag 'YI-100101C' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YI-100101D | instrument tag 'YI-100101D' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YA-100101A | instrument tag 'YA-100101A' does not parse as ISA-5.1 | r1c1, r2c1 |
| info | 14 | `non_isa_tag` | YA-100101B | instrument tag 'YA-100101B' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 14 | `non_isa_tag` | XC-100101A | instrument tag 'XC-100101A' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 14 | `non_isa_tag` | XC-100101B | instrument tag 'XC-100101B' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | XC-100101C | instrument tag 'XC-100101C' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | SC-100101 | instrument tag 'SC-100101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 14 | `non_isa_tag` | FI-100101 | instrument tag 'FI-100101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 22 | `non_isa_tag` | ZIO-500,-101 | instrument tag 'ZIO 500, 101' does not parse as ISA-5.1 | r1c1 |
| info | 22 | `non_isa_tag` | ZIC-500,-101 | instrument tag 'ZIC 500, 101' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 22 | `non_isa_tag` | YA-500,-101 | instrument tag 'YA 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | YI-500,-101 | instrument tag 'YI 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | YI-500,-101 | instrument tag 'YI 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | YI-500,-101 | instrument tag 'YI 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | ZIO-500,-101 | instrument tag 'ZIO 500, 101' does not parse as ISA-5.1 | r1c1 |
| info | 22 | `non_isa_tag` | ZIC-500,-101 | instrument tag 'ZIC 500, 101' does not parse as ISA-5.1 | r1c1, r1c2 |
| info | 22 | `non_isa_tag` | YA-500,-101 | instrument tag 'YA 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | YI-500,-101 | instrument tag 'YI 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | ZCO-500,-101 | instrument tag 'ZCO 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | ZCC-500,-101 | instrument tag 'ZCC 500, 101' does not parse as ISA-5.1 | r1c2 |
| info | 22 | `non_isa_tag` | HS-500,-101 | instrument tag 'HS 500, 101' does not parse as ISA-5.1 | r1c2, r2c2 |
| info | 22 | `non_isa_tag` | ZSO-500,-101 | instrument tag 'ZSO 500, 101' does not parse as ISA-5.1 | r2c2 |
| info | 22 | `non_isa_tag` | ZSC-500,-101 | instrument tag 'ZSC 500, 101' does not parse as ISA-5.1 | r2c2 |
| info | 22 | `non_isa_tag` | ZSO-500,-201 | instrument tag 'ZSO 500, 201' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 22 | `non_isa_tag` | ZSC-500,-201 | instrument tag 'ZSC 500, 201' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 22 | `non_isa_tag` | ZSO-500,-301 | instrument tag 'ZSO 500, 301' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 22 | `non_isa_tag` | ZSC-500,-301 | instrument tag 'ZSC 500, 301' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 22 | `non_isa_tag` | ZSO-500,-201 | instrument tag 'ZSO 500, 201' does not parse as ISA-5.1 | r2c2, r3c2 |
| info | 22 | `non_isa_tag` | ZSC-500,-201 | instrument tag 'ZSC 500, 201' does not parse as ISA-5.1 | r2c2, r3c2 |
