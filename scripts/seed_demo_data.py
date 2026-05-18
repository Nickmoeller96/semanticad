"""
Seed 10 realistic engineering knowledge nodes into the SemantiCAD DB.
Run once after generating the demo STEP file:

    /Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python scripts/seed_demo_data.py
"""

import os
import sys

# Make the package importable when run as a script
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

STEP_FILE = os.path.join(ROOT, "data", "models", "pump_station.step")

from semanticad.data.database import init_db
from semanticad.data import repository as repo

# Part names must match exactly what generate_demo_step.py produces
SEED_KNOWLEDGE = [
    {
        "part": "Suction Flange P-101",
        "category": "Design Rationale",
        "content": (
            "Bei der Schweißnaht zwischen Pumpengehäuse und Saugflansch muss auf 150 °C "
            "vorgewärmt werden. Erfahrung aus Schadensfall S-2019-047: bei niedrigerer "
            "Vorwärmtemperatur trat Risswachstum im Wärmeeinflussbereich auf. Bericht von "
            "Müller unter Doc-ID 4711 im PLM."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "applies_to",
    },
    {
        "part": "Mechanical Seal P-101",
        "category": "Maintenance",
        "content": (
            "Gleitringdichtung alle 8.000 Betriebsstunden wechseln, spätestens nach 3 Jahren. "
            "Auf Leckage-Sensor VS-101 achten — Voralarm bei >0,1 ml/min. Ersatzteilnummer: "
            "GRD-4418-SiC. Niemals ohne neue O-Ringe (Viton, 80 Shore) einbauen."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "applies_to",
    },
    {
        "part": "Impeller P-101",
        "category": "Material Experience",
        "content": (
            "Laufrad aus Duplex-Stahl (1.4462) wegen Kavitationsgefahr bei niedrigem NPSH. "
            "In 2021 wurden zwei Laufräder aus Grauguss eingebaut — beide zeigten nach "
            "6 Monaten Kavitationsnarben. Rückkehr zu Duplex ist Pflicht. Gewicht: 4,2 kg."
        ),
        "author": "Schmidt, Klaus",
        "confidence": 0.9,
        "relation_type": "experience_with",
    },
    {
        "part": "Pump Housing P-101",
        "category": "Failure Mode",
        "content": (
            "Schadensfall 2018: Riss im Pumpengehäuse nach Frost. Ursache: stehendes Wasser "
            "bei Stillstand im Winter. Maßnahme: Entleerungsventil DN15 am tiefsten Punkt "
            "immer öffnen, wenn Stillstand >48 h bei T<5 °C. Protokoll im QM-System unter "
            "Ref. QM-2018-031."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "warning_for",
    },
    {
        "part": "Bearing Housing DE",
        "category": "Maintenance",
        "content": (
            "Antriebsseitiges Lagergehäuse: Fett-Nachschmierung alle 2.000 h mit Klüber "
            "Isoflex NBU 15. Lager SKF 6315-2RS ersetzen bei Schwingungs-RMS >4,5 mm/s "
            "(Sensor VS-101 Alarm). Achtung: Lagerdeckel mit max. 25 Nm anziehen."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "applies_to",
    },
    {
        "part": "Gate Valve GV-101",
        "category": "Operating Experience",
        "content": (
            "Absperrventil GV-101 NIEMALS schnell schließen — Druckstoßgefahr im System "
            "(berechnet: Δp_max = 12 bar bei t_close < 3 s). Mindest-Schließzeit 15 Sekunden. "
            "Bei Notabschaltung erst Pumpe stoppen, dann Ventil schließen."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "warning_for",
    },
    {
        "part": "Check Valve CV-101",
        "category": "Safety Note",
        "content": (
            "Rückschlagventil CV-101 schützt vor Rückströmung bei Pumpenstillstand. "
            "Funktion monatlich prüfen: Pumpe abschalten, Druckabfall auf Druckseite "
            "beobachten. Kein Druckabfall innerhalb 30 s = CV-101 defekt → sofort wechseln. "
            "Ersatz: Wafer-Typ DN65, PN16, Edelstahlscheibe."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "applies_to",
    },
    {
        "part": "Drive Shaft P-101",
        "category": "Design Rationale",
        "content": (
            "Wellenauslegung: kritische Drehzahl liegt bei 4.200 rpm — Betriebsdrehzahl "
            "1.480 rpm (Sicherheitsabstand 65 %). Wellenwerkstoff 1.4021 (martensitisch). "
            "Kupplungsseite hat Passfederverbindung DIN 6885 A 10x8x56. Bei Tausch: "
            "Wuchtgüte G2.5 einhalten."
        ),
        "author": "Schmidt, Klaus",
        "confidence": 0.8,
        "relation_type": "applies_to",
    },
    {
        "part": "Vibration Sensor VS-101",
        "category": "Failure Mode",
        "content": (
            "Sensor VS-101 (IFM efector VSP001) fiel 2022 zweimal durch Kabelbruch aus — "
            "Kabel scheuerte an Motorgehäuse. Abhilfe: Kabelschutzschlauch installiert. "
            "Alarm-Schwellwerte: Voralarm 4,5 mm/s, Hauptalarm 7,1 mm/s RMS (10–1.000 Hz). "
            "Kalibrierung jährlich durch externen Dienstleister."
        ),
        "author": "Müller, Hans",
        "confidence": 1.0,
        "relation_type": "experience_with",
    },
    {
        "part": "Cooling Fan M-101",
        "category": "Operating Experience",
        "content": (
            "Kühlgebläse des Motors M-101 reinigen alle 3 Monate — Lüftungsschlitze "
            "verstopfen durch Staubablagerungen in dieser Umgebung. Bei blockiertem Gebläse "
            "löst Motorschutzschalter nach ca. 12 min aus (Temperatur >155 °C Wicklung). "
            "Reinigung nur im Stillstand, Sicherheitsverriegelung beachten."
        ),
        "author": "Schmidt, Klaus",
        "confidence": 0.9,
        "relation_type": "applies_to",
    },
]


def main():
    if not os.path.exists(STEP_FILE):
        print(f"ERROR: STEP file not found at {STEP_FILE}")
        print("Run 'python scripts/generate_demo_step.py' first.")
        sys.exit(1)

    print("Initializing database…")
    init_db()

    # All 20 part names from generate_demo_step.py
    all_parts = [
        "Pump Housing P-101", "Suction Flange P-101", "Discharge Flange P-101",
        "Impeller P-101", "Drive Shaft P-101", "Motor Housing M-101",
        "Cooling Fan M-101", "Baseplate P-101", "Inlet Pipe DN80",
        "Discharge Pipe DN65", "Gate Valve GV-101", "Check Valve CV-101",
        "Pressure Gauge PI-101", "Pressure Gauge PI-102", "Flexible Coupling CK-101",
        "Bearing Housing DE", "Bearing Housing NDE", "Mechanical Seal P-101",
        "Vibration Sensor VS-101", "Temperature Sensor TE-101",
    ]

    print(f"Importing {len(all_parts)} parts from {STEP_FILE}…")
    part_map = repo.import_parts_from_step(STEP_FILE, all_parts)
    print(f"  {len(part_map)} parts in DB")

    print("Seeding knowledge nodes…")
    count = 0
    for entry in SEED_KNOWLEDGE:
        pid = part_map.get(entry["part"])
        if not pid:
            print(f"  WARN: part '{entry['part']}' not found in DB, skipping")
            continue
        repo.add_knowledge_node(
            semantic_part_id=pid,
            content=entry["content"],
            category=entry["category"],
            author=entry["author"],
            confidence=entry["confidence"],
            relation_type=entry["relation_type"],
        )
        print(f"  + [{entry['category']}] {entry['part']}")
        count += 1

    print(f"\nDone — {count} knowledge nodes seeded into data/semanticad.db")
    print("\nNow launch the app and open data/models/pump_station.step:")
    print("  /Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python -m semanticad")


if __name__ == "__main__":
    main()
