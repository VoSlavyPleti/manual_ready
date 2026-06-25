"""Extract DOCX text while preserving common Word numbered-clause structure.

This is a mechanical source-preparation helper. It does not perform legal
analysis and does not read evaluation workbooks.
"""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def wtag(name: str) -> str:
    return f"{{{NS['w']}}}{name}"


def read_xml(zf: zipfile.ZipFile, name: str) -> ET.Element | None:
    try:
        return ET.fromstring(zf.read(name))
    except KeyError:
        return None


def text_of_paragraph(paragraph: ET.Element) -> str:
    parts = []
    for node in paragraph.iter():
        if node.tag == wtag("t") and node.text:
            parts.append(node.text)
        elif node.tag == wtag("tab"):
            parts.append(" ")
    return "".join(parts).strip()


def paragraph_num(paragraph: ET.Element) -> tuple[str | None, int | None]:
    ppr = paragraph.find("w:pPr", NS)
    if ppr is None:
        return None, None
    numpr = ppr.find("w:numPr", NS)
    if numpr is None:
        return None, None
    num_id_node = numpr.find("w:numId", NS)
    ilvl_node = numpr.find("w:ilvl", NS)
    if num_id_node is None:
        return None, None
    num_id = num_id_node.get(wtag("val"))
    ilvl = int(ilvl_node.get(wtag("val"))) if ilvl_node is not None else 0
    return num_id, ilvl


def parse_numbering(root: ET.Element | None) -> dict[str, dict[int, dict[str, str]]]:
    if root is None:
        return {}

    abstract_levels: dict[str, dict[int, dict[str, str]]] = {}
    for abstract in root.findall("w:abstractNum", NS):
        abstract_id = abstract.get(wtag("abstractNumId"))
        if abstract_id is None:
            continue
        levels: dict[int, dict[str, str]] = {}
        for lvl in abstract.findall("w:lvl", NS):
            ilvl = int(lvl.get(wtag("ilvl"), "0"))
            start = lvl.find("w:start", NS)
            fmt = lvl.find("w:numFmt", NS)
            text = lvl.find("w:lvlText", NS)
            levels[ilvl] = {
                "start": start.get(wtag("val")) if start is not None else "1",
                "fmt": fmt.get(wtag("val")) if fmt is not None else "decimal",
                "text": text.get(wtag("val")) if text is not None else f"%{ilvl + 1}.",
            }
        abstract_levels[abstract_id] = levels

    num_to_levels: dict[str, dict[int, dict[str, str]]] = {}
    for num in root.findall("w:num", NS):
        num_id = num.get(wtag("numId"))
        abstract_ref = num.find("w:abstractNumId", NS)
        if num_id is None or abstract_ref is None:
            continue
        abstract_id = abstract_ref.get(wtag("val"))
        levels = {k: dict(v) for k, v in abstract_levels.get(abstract_id, {}).items()}
        for override in num.findall("w:lvlOverride", NS):
            ilvl = int(override.get(wtag("ilvl"), "0"))
            start_override = override.find("w:startOverride", NS)
            if start_override is not None:
                levels.setdefault(ilvl, {})["start"] = start_override.get(wtag("val"), "1")
        num_to_levels[num_id] = levels
    return num_to_levels


def render_number(num_id: str, ilvl: int, levels: dict[int, dict[str, str]], counters: dict[int, int]) -> str | None:
    level = levels.get(ilvl, {})
    if level.get("fmt") not in {"decimal", None}:
        return None
    for parent in range(ilvl + 1):
        if parent not in counters:
            parent_start = int(levels.get(parent, {}).get("start") or "1")
            counters[parent] = parent_start
    counters[ilvl] += 0 if counters.get(ilvl) is not None else int(level.get("start") or "1")
    # Remove deeper counters when moving back up.
    for deeper in [key for key in counters if key > ilvl]:
        del counters[deeper]

    pattern = level.get("text") or f"%{ilvl + 1}."
    rendered = pattern
    for idx in range(ilvl + 1):
        rendered = rendered.replace(f"%{idx + 1}", str(counters.get(idx, 1)))
    if not re.fullmatch(r"\d+(?:\.\d+)*\.?", rendered):
        rendered = ".".join(str(counters.get(idx, 1)) for idx in range(ilvl + 1)) + "."
    counters[ilvl] += 1
    return rendered.rstrip(".")


def extract_docx(docx_path: Path) -> tuple[str, dict]:
    with zipfile.ZipFile(docx_path) as zf:
        document = read_xml(zf, "word/document.xml")
        numbering = parse_numbering(read_xml(zf, "word/numbering.xml"))
    if document is None:
        raise ValueError("word/document.xml not found")

    counters_by_num: dict[str, dict[int, int]] = {}
    lines: list[str] = []
    numbered_count = 0
    recovered_count = 0

    for paragraph in document.iter(wtag("p")):
        text = text_of_paragraph(paragraph)
        if not text:
            continue
        num_id, ilvl = paragraph_num(paragraph)
        prefix = None
        if num_id is not None and ilvl is not None and num_id in numbering:
            counters = counters_by_num.setdefault(num_id, {})
            prefix = render_number(num_id, ilvl, numbering[num_id], counters)
        if prefix and not re.match(r"^\d+(?:\.\d+)*\.?\s", text):
            lines.append(f"{prefix}. {text}")
            numbered_count += 1
            recovered_count += 1
        else:
            if re.match(r"^\d+(?:\.\d+)*\.?\s", text):
                numbered_count += 1
            lines.append(text)

    result = "\n".join(lines).strip() + "\n"
    stats = {
        "source": str(docx_path),
        "line_count": len(lines),
        "numbered_line_count": numbered_count,
        "docx_recovered_numbering_count": recovered_count,
        "zero_prefixed_count": len(re.findall(r"(?m)^\s*0(?:\.0|\.\d+)+\.?\s", result)),
    }
    return result, stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("docx", type=Path)
    parser.add_argument("txt_out", type=Path)
    parser.add_argument("--stats-out", type=Path)
    args = parser.parse_args()

    text, stats = extract_docx(args.docx)
    args.txt_out.parent.mkdir(parents=True, exist_ok=True)
    args.txt_out.write_text(text, encoding="utf-8")
    payload = json.dumps(stats, ensure_ascii=False, indent=2)
    if args.stats_out:
        args.stats_out.parent.mkdir(parents=True, exist_ok=True)
        args.stats_out.write_text(payload, encoding="utf-8")
    print(payload)
    if stats["zero_prefixed_count"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
