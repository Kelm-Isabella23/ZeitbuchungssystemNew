# CSV-Export/-Import (Standardbibliothek)
import csv

# In-Memory Text-Buffer, um CSV als String zu erzeugen (ohne Datei zu schreiben)
import io

# JSON-Export/-Import (Standardbibliothek)
import json

# XML-Erzeugung und -Parsing (Standardbibliothek)
import xml.etree.ElementTree as ET

# Django-Aggregationsfunktion (Summenbildung für Statistiken)
from django.db.models import Sum

# Importiert die Datenmodelle, mit denen gearbeitet wird
from .models import Report, Module


def get_reports_as_dicts(user):
    """
    Liefert alle Reports eines Users als Liste von Dictionaries zurück.
    Wird als gemeinsame Basis für Exporte (JSON/CSV/XML) genutzt.
    """
    # select_related("module") vermeidet zusätzliche DB-Abfragen pro Report
    reports = Report.objects.filter(user=user).select_related("module").order_by("date")

    return [
        {
            "date": r.date.isoformat(),  # Datum als ISO-String für Exportformate
            "minutes": r.minutes,
            "module": r.module.name,
            "text": r.text,
        }
        for r in reports
    ]


def export_reports(user, fmt: str) -> str:
    """
    Exportiert Reports eines Users in das gewünschte Format (json/csv/xml).
    Gibt den Export als String zurück.
    """
    data = get_reports_as_dicts(user)

    # JSON: lesbar formatiert, Umlaute bleiben erhalten (ensure_ascii=False)
    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    # CSV: schreibt Daten zeilenweise in einen String-Buffer
    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["date", "minutes", "module", "text"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return buf.getvalue()

    # XML: erstellt eine simple XML-Struktur <reports><report>...</report></reports>
    if fmt == "xml":
        root = ET.Element("reports")
        for row in data:
            r_el = ET.SubElement(root, "report")
            for k, v in row.items():
                ET.SubElement(r_el, k).text = str(v)
        return ET.tostring(root, encoding="unicode")

    # Schutz: unbekanntes Format
    raise ValueError("Unbekanntes Format")


def import_reports_overwrite(user, fmt: str, content: str):
    """
    Importiert Reports aus json/csv/xml und überschreibt die bestehenden Reports des Users.
    (Erst löschen, dann neu anlegen.)
    """
    rows = []

    # JSON: String -> Python-Liste/Dictionaries
    if fmt == "json":
        rows = json.loads(content)

    # CSV: liest aus einem String-Buffer via DictReader
    elif fmt == "csv":
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)

    # XML: parst Struktur und baut Zeilen-Dictionaries daraus
    elif fmt == "xml":
        root = ET.fromstring(content)
        for r in root.findall("report"):
            rows.append({
                "date": r.findtext("date"),
                "minutes": r.findtext("minutes"),
                "module": r.findtext("module"),
                "text": r.findtext("text"),
            })

    else:
        raise ValueError("Unbekanntes Format")

    # Überschreiben: alte Reports entfernen
    Report.objects.filter(user=user).delete()

    # Neue Reports anlegen (Module werden bei Bedarf automatisch erstellt)
    for r in rows:
        module, _ = Module.objects.get_or_create(name=r["module"])
        Report.objects.create(
            user=user,
            date=r["date"],                 # Django kann ISO-Date-Strings i. d. R. parsen
            minutes=int(r["minutes"]),
            module=module,
            text=(r["text"] or "")[:300],   # Längenbegrenzung + Schutz gegen None
        )


def get_module_stats(user):
    """
    Berechnet Statistik pro Modul:
    - Summierte Minuten pro Modul
    - Prozentanteil am Gesamtaufwand
    Gibt (rows, total_all) zurück.
    """
    # Aggregiert Minuten je Modul direkt in der Datenbank
    qs = (
        Report.objects.filter(user=user)
        .values("module__name")
        .annotate(total_minutes=Sum("minutes"))
        .order_by("module__name")
    )

    # Gesamtminuten über alle Module (für Prozentberechnung)
    total_all = sum(item["total_minutes"] or 0 for item in qs) or 0

    # Aufbereitung für Anzeige/Template (Modulname, Minuten, Prozent)
    rows = []
    for item in qs:
        minutes = item["total_minutes"] or 0
        percent = round((minutes / total_all) * 100, 1) if total_all else 0.0
        rows.append({
            "module": item["module__name"],
            "minutes": minutes,
            "percent": percent
        })

    return rows, total_all
