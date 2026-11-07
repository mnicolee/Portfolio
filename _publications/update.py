import json
import re
import urllib.request
from pathlib import Path

ORCID = "0000-0001-6953-2177"
OUT = Path(__file__).resolve().parent.parent / "publications.bib"
SERVERS = {"10.1101/": "bioRxiv", "10.64898/": "bioRxiv", "10.48550/arxiv.": "arXiv"}
MONTHS = "jan feb mar apr may jun jul aug sep oct nov dec".split()


def get(url, accept):
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "portfolio-publications"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def words(title):
    return set(re.findall(r"[a-z0-9]+", title.lower()))


def same_work(a, b):
    wa, wb = words(a), words(b)
    return len(wa & wb) / (min(len(wa), len(wb)) or 1) >= 0.8


def works():
    data = json.loads(get(f"https://pub.orcid.org/v3.0/{ORCID}/works", "application/json"))
    for group in data["group"]:
        s = group["work-summary"][0]
        ids = s.get("external-ids", {}).get("external-id", [])
        doi = next((e["external-id-value"] for e in ids if e["external-id-type"] == "doi"), None)
        if doi:
            yield {"title": s["title"]["title"]["value"], "type": s["type"], "doi": doi.lower()}


def keep(items):
    items = [w for w in items if not re.match(r"(author )?correction", w["title"], re.I)]
    published = [w for w in items if w["type"] != "preprint"]
    return [w for w in items if w["type"] != "preprint" or not any(same_work(w["title"], p["title"]) for p in published)]


def bibtex(doi):
    entry = get(f"https://doi.org/{doi}", "application/x-bibtex").strip()
    entry = re.sub(r"<i>\s*(.*?)\s*</i>", lambda m: "\\textit{" + m.group(1) + "}", entry, flags=re.S)
    entry = re.sub(r"\s*\n\s*", " ", entry)
    server = next((name for prefix, name in SERVERS.items() if doi.startswith(prefix)), None)
    if server:
        entry = re.sub(r"^@\w+\{", "@misc{", entry, count=1)
        entry = re.sub(r"publisher\s*=\s*\{[^}]*\}", "publisher={" + server + "}", entry)
    arxiv = re.match(r"10\.48550/arxiv\.\d{2}(\d{2})\.", doi)
    if arxiv and not re.search(r"\bmonth\s*=", entry):
        entry = entry[: entry.rfind("}")].rstrip().rstrip(",") + ", month=" + MONTHS[int(arxiv.group(1)) - 1] + " }"
    entry = re.sub(r"month\s*=\s*\{?([A-Za-z]+)\}?", lambda m: "month=" + m.group(1)[:3].lower(), entry)
    entry = re.sub(r"title\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", lambda m: "title={{" + m.group(1).strip() + "}}", entry, count=1)
    entry = re.sub(r"(doi\s*=\s*\{)([^}]*)\}", lambda m: m.group(1) + m.group(2).lower() + "}", entry, flags=re.I)
    key = "doi_" + re.sub(r"[^a-z0-9]+", "_", doi)
    return re.sub(r"^@(\w+)\{[^,]*,", lambda m: "@" + m.group(1).lower() + "{" + key + ",", entry, count=1)


def main():
    chosen = keep(list(works()))
    OUT.write_text("\n\n".join(bibtex(w["doi"]) for w in chosen) + "\n", encoding="utf-8")
    for w in chosen:
        print(w["type"], w["doi"], w["title"][:70])


if __name__ == "__main__":
    main()
