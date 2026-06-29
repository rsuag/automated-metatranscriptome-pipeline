#!/usr/bin/env python3
import argparse
import json
import os
import urllib.error
import urllib.request
from datetime import date

from read_project_value import load_simple_yaml


def fetch_json(url, timeout=15):
    request = urllib.request.Request(url, headers={"User-Agent": "automated-metatranscriptome-pipeline"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def summarize_source(source):
    if source["type"] != "github_releases":
        return {
            "status": "watch",
            "note": "Static watch source. Review manually or replace with a machine-readable feed.",
            "items": [{"title": source["name"], "version": "", "published_at": "", "url": source["url"]}],
        }
    try:
        releases = fetch_json(source["url"])
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"status": "unavailable", "note": str(exc), "items": []}
    items = []
    for release in releases[:5]:
        items.append(
            {
                "title": release.get("name") or release.get("tag_name") or "unnamed release",
                "version": release.get("tag_name") or "",
                "published_at": release.get("published_at") or "",
                "url": release.get("html_url") or source["url"],
            }
        )
    return {"status": "ok", "note": "", "items": items}


def checklist(stage):
    base = [
        "maintenance status checked",
        "RNA-specific assumptions documented",
        "container or conda availability checked",
        "small benchmark dataset identified",
        "outputs are parseable by audit scripts",
        "evidence limits documented",
    ]
    if stage in {"optional", "default"}:
        base.append("backward compatibility plan written")
    if stage == "default":
        base.append("benchmark and interpretation review passed")
    return base


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sources", required=True)
    parser.add_argument("--project", required=True)
    args = parser.parse_args()

    with open(args.sources, "r", encoding="utf-8") as handle:
        config = json.load(handle)
    project = load_simple_yaml(args.project)
    report_path = project["automation"]["method_radar_report"]
    os.makedirs(os.path.dirname(report_path), exist_ok=True)

    lines = [
        "# Method Radar",
        "",
        f"- Date: {date.today().isoformat()}",
        f"- Project: {project['project_name']}",
        "",
        "The radar tracks candidate tools and methods. It creates a review queue; it does not silently change defaults.",
        "",
    ]

    for source in config["sources"]:
        summary = summarize_source(source)
        lines.extend(
            [
                f"## {source['name']}",
                "",
                f"- Module: `{source['module']}`",
                f"- Adoption stage: `{source['adoption_stage']}`",
                f"- Status: `{summary['status']}`",
            ]
        )
        if summary["note"]:
            lines.append(f"- Note: {summary['note']}")
        lines.extend(["", "| Item | Version | Published | Link |", "| --- | --- | --- | --- |"])
        if summary["items"]:
            for item in summary["items"]:
                lines.append(f"| {item['title']} | {item['version']} | {item['published_at']} | {item['url']} |")
        else:
            lines.append("| No items collected |  |  |  |")
        lines.extend(["", "Adoption checklist:", ""])
        lines.extend([f"- {item}" for item in checklist(source["adoption_stage"])])
        lines.append("")

    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines))
    print(report_path)


if __name__ == "__main__":
    main()

