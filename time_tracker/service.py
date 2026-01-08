import csv
import io
import json
import xml.etree.ElementTree as ET

from .models import Report, Module


def get_reports_as_dicts(user):
    reports = Report.objects.filter(user=user).select_related("module").order_by("date")
    return [
        {
            "date": r.date.isoformat(),
            "minutes": r.minutes,
            "module": r.module.name,
            "text": r.text,
        }
        for r in reports
    ]


def export_reports(user, fmt: str) -> str:
    data = get_reports_as_dicts(user)

    if fmt == "json":
        return json.dumps(data, ensure_ascii=False, indent=2)

    if fmt == "csv":
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["date", "minutes", "module", "text"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return buf.getvalue()

    if fmt == "xml":
        root = ET.Element("reports")
        for row in data:
            r_el = ET.SubElement(root, "report")
            for k, v in row.items():
                ET.SubElement(r_el, k).text = str(v)
        return ET.tostring(root, encoding="unicode")

    raise ValueError("Unbekanntes Format")


def import_reports_overwrite(user, fmt: str, content: str):
    rows = []

    if fmt == "json":
        rows = json.loads(content)

    elif fmt == "csv":
        reader = csv.DictReader(io.StringIO(content))
        rows = list(reader)

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

    # 🔥 Überschreiben = löschen + neu anlegen
    Report.objects.filter(user=user).delete()

    for r in rows:
        module, _ = Module.objects.get_or_create(name=r["module"])
        Report.objects.create(
            user=user,
            date=r["date"],
            minutes=int(r["minutes"]),
            module=module,
            text=r["text"][:300],
        )
