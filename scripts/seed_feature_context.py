"""
Comprehensive demo seed — baseline knowledge nodes + feature-context nodes + relationships.
Idempotent: skips any node whose content already exists for that part.

Run:
    /Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python scripts/seed_feature_context.py
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

STEP_FILE = os.path.join(ROOT, "data", "models", "pump_station.step")

from semanticad.data.database import init_db, get_connection
from semanticad.data import repository as repo

# ---------------------------------------------------------------------------
# All 20 part names (must match generate_demo_step.py)
# ---------------------------------------------------------------------------
ALL_PARTS = [
    "Pump Housing P-101", "Suction Flange P-101", "Discharge Flange P-101",
    "Impeller P-101", "Drive Shaft P-101", "Motor Housing M-101",
    "Cooling Fan M-101", "Baseplate P-101", "Inlet Pipe DN80",
    "Discharge Pipe DN65", "Gate Valve GV-101", "Check Valve CV-101",
    "Pressure Gauge PI-101", "Pressure Gauge PI-102", "Flexible Coupling CK-101",
    "Bearing Housing DE", "Bearing Housing NDE", "Mechanical Seal P-101",
    "Vibration Sensor VS-101", "Temperature Sensor TE-101",
]

# ---------------------------------------------------------------------------
# Knowledge nodes
# Format: (part_name, category, content, author, confidence, relation_type)
# ---------------------------------------------------------------------------
KNOWLEDGE = [
    # ---------- Baseline nodes (from original seed_demo_data.py) ----------

    ("Suction Flange P-101", "Design Rationale",
     "Bei der Schweißnaht zwischen Pumpengehäuse und Saugflansch muss auf 150 °C "
     "vorgewärmt werden. Erfahrung aus Schadensfall S-2019-047: bei niedrigerer "
     "Vorwärmtemperatur trat Risswachstum im Wärmeeinflussbereich auf. Bericht von "
     "Müller unter Doc-ID 4711 im PLM.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Mechanical Seal P-101", "Maintenance",
     "Gleitringdichtung alle 8.000 Betriebsstunden wechseln, spätestens nach 3 Jahren. "
     "Auf Leckage-Sensor VS-101 achten — Voralarm bei >0,1 ml/min. Ersatzteilnummer: "
     "GRD-4418-SiC. Niemals ohne neue O-Ringe (Viton, 80 Shore) einbauen.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Impeller P-101", "Material Experience",
     "Laufrad aus Duplex-Stahl (1.4462) wegen Kavitationsgefahr bei niedrigem NPSH. "
     "In 2021 wurden zwei Laufräder aus Grauguss eingebaut — beide zeigten nach "
     "6 Monaten Kavitationsnarben. Rückkehr zu Duplex ist Pflicht. Gewicht: 4,2 kg.",
     "Schmidt, Klaus", 0.9, "experience_with"),

    ("Pump Housing P-101", "Failure Mode",
     "Schadensfall 2018: Riss im Pumpengehäuse nach Frost. Ursache: stehendes Wasser "
     "bei Stillstand im Winter. Maßnahme: Entleerungsventil DN15 am tiefsten Punkt "
     "immer öffnen, wenn Stillstand >48 h bei T<5 °C. Protokoll im QM-System unter "
     "Ref. QM-2018-031.",
     "Müller, Hans", 1.0, "warning_for"),

    ("Bearing Housing DE", "Maintenance",
     "Antriebsseitiges Lagergehäuse: Fett-Nachschmierung alle 2.000 h mit Klüber "
     "Isoflex NBU 15. Lager SKF 6315-2RS ersetzen bei Schwingungs-RMS >4,5 mm/s "
     "(Sensor VS-101 Alarm). Achtung: Lagerdeckel mit max. 25 Nm anziehen.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Gate Valve GV-101", "Operating Experience",
     "Absperrventil GV-101 NIEMALS schnell schließen — Druckstoßgefahr im System "
     "(berechnet: Δp_max = 12 bar bei t_close < 3 s). Mindest-Schließzeit 15 Sekunden. "
     "Bei Notabschaltung erst Pumpe stoppen, dann Ventil schließen.",
     "Müller, Hans", 1.0, "warning_for"),

    ("Check Valve CV-101", "Safety Note",
     "Rückschlagventil CV-101 schützt vor Rückströmung bei Pumpenstillstand. "
     "Funktion monatlich prüfen: Pumpe abschalten, Druckabfall auf Druckseite "
     "beobachten. Kein Druckabfall innerhalb 30 s = CV-101 defekt → sofort wechseln. "
     "Ersatz: Wafer-Typ DN65, PN16, Edelstahlscheibe.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Drive Shaft P-101", "Design Rationale",
     "Wellenauslegung: kritische Drehzahl liegt bei 4.200 rpm — Betriebsdrehzahl "
     "1.480 rpm (Sicherheitsabstand 65 %). Wellenwerkstoff 1.4021 (martensitisch). "
     "Kupplungsseite hat Passfederverbindung DIN 6885 A 10x8x56. Bei Tausch: "
     "Wuchtgüte G2.5 einhalten.",
     "Schmidt, Klaus", 0.8, "applies_to"),

    ("Vibration Sensor VS-101", "Failure Mode",
     "Sensor VS-101 (IFM efector VSP001) fiel 2022 zweimal durch Kabelbruch aus — "
     "Kabel scheuerte an Motorgehäuse. Abhilfe: Kabelschutzschlauch installiert. "
     "Alarm-Schwellwerte: Voralarm 4,5 mm/s, Hauptalarm 7,1 mm/s RMS (10–1.000 Hz). "
     "Kalibrierung jährlich durch externen Dienstleister.",
     "Müller, Hans", 1.0, "experience_with"),

    ("Cooling Fan M-101", "Operating Experience",
     "Kühlgebläse des Motors M-101 reinigen alle 3 Monate — Lüftungsschlitze "
     "verstopfen durch Staubablagerungen in dieser Umgebung. Bei blockiertem Gebläse "
     "löst Motorschutzschalter nach ca. 12 min aus (Temperatur >155 °C Wicklung). "
     "Reinigung nur im Stillstand, Sicherheitsverriegelung beachten.",
     "Schmidt, Klaus", 0.9, "applies_to"),

    # ---------- Feature-context nodes (new) ----------

    ("Pump Housing P-101", "Design Rationale",
     "Schweißnaht Saugseite (Kehlnaht a6): Verbindung Gehäuse–Saugflansch-Stutzen. "
     "Vorwärmtemperatur 150 °C Pflicht (S-2019-047). WIG-geschweißt, Werkstoff 1.4408. "
     "Nachprüfung per Farbeindringprüfung nach jedem Schweißvorgang.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Pump Housing P-101", "Design Rationale",
     "Spiralgehäuse Druckseite: Mindestwandstärke an der engsten Stelle 8 mm "
     "(berechnet für PN 25). Bei Nacharbeit oder Reparaturschweißung nicht unterschreiten — "
     "Druckprüfung 1,5×Betriebsdruck (37,5 bar) erforderlich.",
     "Schmidt, Klaus", 0.9, "applies_to"),

    ("Suction Flange P-101", "Maintenance",
     "Dichtfläche Saugflansch (Form B nach DIN EN 1092): Rauhigkeit Ra ≤ 1,6 μm. "
     "Nach jedem Demontagezyklus mit Rautentiefenmessgerät prüfen. "
     "Planschleifen erforderlich wenn Ra > 3,2 μm. Flachdichtung Klingersil C-4430.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Drive Shaft P-101", "Failure Mode",
     "Lagersitz DE-Seite (Toleranz k6, Ra 0,8 μm): Passungsrost aufgetreten 2020-08 "
     "wegen falscher Lagerungsart (Wälzlager im Ölbad statt Fettschmierung). "
     "Abhilfe: Osmo 4010 auf Lagersitz aufbringen, korrekte Fettschmierung einhalten.",
     "Müller, Hans", 1.0, "warning_for"),

    ("Drive Shaft P-101", "Design Rationale",
     "Wellenabsatz Kupplungsseite: Passfedernut DIN 6885 A 10×8×56, Toleranz JS9. "
     "Kupplung CK-101 muss nach Tausch neu gewuchtet werden — Wuchtgüte G2.5. "
     "Ohne Neuauswuchtung: Schwingungen >4,5 mm/s innerhalb von 48 h Betrieb.",
     "Schmidt, Klaus", 0.95, "applies_to"),

    ("Mechanical Seal P-101", "Maintenance",
     "Gleitringdichtung — Gleitfläche SiC/SiC: Planheit ≤ 0,9 μm (Lichtbandmessung). "
     "Dichtfläche nie trocken laufen lassen — thermischer Schock zerstört Gleitring "
     "innerhalb 30 s. Vor Inbetriebnahme Sperrwasserversorgung (1–3 bar) prüfen.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Bearing Housing DE", "Maintenance",
     "Fettschmiernippel DE-Lagerung (DIN 71412 Form A M8): Klüber Isoflex NBU 15, "
     "alle 2.000 h nachschmieren, max. 5 g pro Schmierintervall. "
     "Überfettung zerstört Labyrinthdichtung — Fett tritt dann ins Motorinnere ein.",
     "Müller, Hans", 1.0, "applies_to"),

    ("Impeller P-101", "Operating Experience",
     "Laufradspalt zum Spiralgehäuse (radialer Spalt): Sollmaß 0,3–0,5 mm. "
     "Bei Verschleiß über 1,0 mm sinkt Förderhöhe messbar um >5 %. "
     "Letzter Spaltcheck: 2023-11 durch Schmidt (Ergebnis: 0,4 mm, i.O.).",
     "Schmidt, Klaus", 0.9, "experience_with"),
]

# ---------------------------------------------------------------------------
# Relationships to seed
# Format: (from_part, to_part, relation_type)
# ---------------------------------------------------------------------------
RELATIONSHIPS = [
    ("Motor Housing M-101",      "Drive Shaft P-101",       "drives"),
    ("Drive Shaft P-101",        "Flexible Coupling CK-101","connected_to"),
    ("Drive Shaft P-101",        "Impeller P-101",          "connected_to"),
    ("Mechanical Seal P-101",    "Drive Shaft P-101",       "seals"),
    ("Bearing Housing DE",       "Drive Shaft P-101",       "contains"),
    ("Vibration Sensor VS-101",  "Drive Shaft P-101",       "monitors"),
    ("Temperature Sensor TE-101","Bearing Housing DE",      "monitors"),
    ("Gate Valve GV-101",        "Inlet Pipe DN80",         "connected_to"),
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _node_exists(conn, semantic_part_id: str, content_prefix: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM knowledge_nodes kn "
        "JOIN anchors a ON kn.knowledge_id = a.knowledge_id "
        "WHERE a.semantic_part_id = ? AND kn.content LIKE ?",
        (semantic_part_id, content_prefix[:60] + "%"),
    ).fetchone()
    return row is not None


def _relation_exists(conn, from_id: str, to_id: str, rel_type: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM part_relationships "
        "WHERE from_part_id = ? AND to_part_id = ? AND relation_type = ?",
        (from_id, to_id, rel_type),
    ).fetchone()
    return row is not None


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    if not os.path.exists(STEP_FILE):
        print(f"ERROR: STEP file not found at {STEP_FILE}")
        print("Run 'python scripts/generate_demo_step.py' first.")
        sys.exit(1)

    print("Initializing database…")
    init_db()

    print(f"Importing {len(ALL_PARTS)} parts…")
    part_map = repo.import_parts_from_step(STEP_FILE, ALL_PARTS)
    print(f"  {len(part_map)} parts in DB\n")

    # -- Knowledge nodes -------------------------------------------------
    print("Seeding knowledge nodes (skipping duplicates)…")
    added_k = skipped_k = 0
    with get_connection() as conn:
        for part_name, category, content, author, confidence, rel_type in KNOWLEDGE:
            pid = part_map.get(part_name)
            if not pid:
                print(f"  WARN: part '{part_name}' not in DB, skipping")
                continue
            if _node_exists(conn, pid, content):
                skipped_k += 1
                continue
            repo.add_knowledge_node(pid, content, category, author, confidence, rel_type)
            print(f"  + [{category}] {part_name[:30]:<30}  {content[:55]}…")
            added_k += 1

    print(f"  → {added_k} added, {skipped_k} already existed\n")

    # -- Relationships ---------------------------------------------------
    print("Seeding relationships (skipping duplicates)…")
    added_r = skipped_r = 0
    with get_connection() as conn:
        for from_name, to_name, rel_type in RELATIONSHIPS:
            from_id = part_map.get(from_name)
            to_id   = part_map.get(to_name)
            if not from_id or not to_id:
                print(f"  WARN: part not found for {from_name} or {to_name}")
                continue
            if _relation_exists(conn, from_id, to_id, rel_type):
                skipped_r += 1
                continue
            repo.add_relationship(from_id, to_id, rel_type)
            print(f"  + {from_name} --{rel_type}--> {to_name}")
            added_r += 1

    print(f"  → {added_r} added, {skipped_r} already existed\n")

    # -- Summary ---------------------------------------------------------
    with get_connection() as conn:
        stats = {
            "parts":    conn.execute("SELECT COUNT(*) FROM parts").fetchone()[0],
            "nodes":    conn.execute("SELECT COUNT(*) FROM knowledge_nodes").fetchone()[0],
            "anchors":  conn.execute("SELECT COUNT(*) FROM anchors").fetchone()[0],
            "rels":     conn.execute("SELECT COUNT(*) FROM part_relationships").fetchone()[0],
        }
    print("Done. Ontology now contains:")
    print(f"  {stats['parts']} Bauteile  |  {stats['nodes']} Wissensknoten  "
          f"|  {stats['anchors']} Anker  |  {stats['rels']} Verbindungen")
    print("\nStart the app:")
    print("  /Users/nickmllr8/opt/anaconda3/envs/semanticad/bin/python -m semanticad")


if __name__ == "__main__":
    main()
