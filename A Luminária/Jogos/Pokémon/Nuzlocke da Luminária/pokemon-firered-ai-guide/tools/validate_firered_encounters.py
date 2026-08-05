#!/usr/bin/env python3
"""Validate that the generated wild encounter data is FireRed-only.

Checks are intentionally small and dependency-free:
- local structural guard: every encounter record must be version=FireRed and
  must not reference a LeafGreen encounter table;
- canonical sample guard: several early-game tables are checked against known
  FireRed totals from the generated pret/pokefirered data;
- optional online guard: the same samples can be compared against PokeAPI's
  location-area `version_details=firered` records.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

FIRERED = "FireRed"
LEAFGREEN = "LeafGreen"

LOCAL_EXPECTED = {
    ("MAP_ROUTE2", "land"): {
        "Rattata": 45,
        "Pidgey": 45,
        "Caterpie": 5,
        "Weedle": 5,
    },
    ("MAP_VIRIDIAN_FOREST", "land"): {
        "Caterpie": 40,
        "Weedle": 40,
        "Kakuna": 10,
        "Metapod": 5,
        "Pikachu": 5,
    },
    ("MAP_ROUTE24", "land"): {
        "Weedle": 20,
        "Caterpie": 20,
        "Pidgey": 15,
        "Oddish": 25,
        "Abra": 15,
        "Kakuna": 4,
        "Metapod": 1,
    },
    ("MAP_ROUTE25", "land"): {
        "Weedle": 20,
        "Caterpie": 20,
        "Pidgey": 15,
        "Oddish": 25,
        "Abra": 15,
        "Kakuna": 4,
        "Metapod": 1,
    },
}

POKEAPI_AREAS = {
    ("MAP_ROUTE2", "land"): 296,
    ("MAP_VIRIDIAN_FOREST", "land"): 321,
    ("MAP_ROUTE24", "land"): 314,
    ("MAP_ROUTE25", "land"): 315,
}

METHOD_MAP = {"land": "walk", "surf": "surf", "old_rod": "old-rod", "good_rod": "good-rod", "super_rod": "super-rod"}
NAME_FIX = {
    "nidoran-f": "Nidoran F",
    "nidoran-m": "Nidoran M",
    "farfetchd": "Farfetchd",
    "mr-mime": "Mr Mime",
    "ho-oh": "Ho Oh",
}


def norm_pokeapi_name(name: str) -> str:
    if name in NAME_FIX:
        return NAME_FIX[name]
    return " ".join(part.capitalize() for part in name.split("-"))


def totals_for(rows, map_id: str, method: str) -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for row in rows:
        if row.get("map_id") == map_id and row.get("method") == method:
            totals[row["species"]] += int(row["slot_rate_percent"])
    return dict(sorted(totals.items()))


def pokeapi_totals(area_id: int, method: str) -> dict[str, int]:
    req = urllib.request.Request(
        f"https://pokeapi.co/api/v2/location-area/{area_id}/",
        headers={"User-Agent": "Hermes MoniLocke FireRed encounter verifier"},
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.load(response)
    target_method = METHOD_MAP[method]
    totals: dict[str, int] = defaultdict(int)
    for pokemon in data.get("pokemon_encounters", []):
        species = norm_pokeapi_name(pokemon["pokemon"]["name"])
        for version in pokemon.get("version_details", []):
            if version.get("version", {}).get("name") != "firered":
                continue
            for detail in version.get("encounter_details", []):
                if detail.get("method", {}).get("name") == target_method:
                    totals[species] += int(detail.get("chance", 0))
    return dict(sorted(totals.items()))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--guide", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--online", action="store_true", help="also verify representative samples against PokeAPI")
    args = parser.parse_args()

    rows = json.loads((args.guide / "data/encounters.json").read_text(encoding="utf-8"))
    errors: list[str] = []

    for row in rows:
        if row.get("version") != FIRERED:
            errors.append(f"non-FireRed version: {row.get('id')} version={row.get('version')}")
        if LEAFGREEN in row.get("encounter_table_id", "") or LEAFGREEN in row.get("id", ""):
            errors.append(f"LeafGreen marker leaked: {row.get('id')}")

    for key, expected in LOCAL_EXPECTED.items():
        got = totals_for(rows, *key)
        if got != dict(sorted(expected.items())):
            errors.append(f"local sample mismatch {key}: expected {expected}, got {got}")

    if args.online:
        for key, area_id in POKEAPI_AREAS.items():
            local = totals_for(rows, *key)
            online = pokeapi_totals(area_id, key[1])
            if local != online:
                errors.append(f"PokeAPI mismatch {key}: local={local}, online={online}")

    if errors:
        print("FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"PASS: {len(rows)} encounter rows are FireRed-only")
    if args.online:
        print("PASS: representative FireRed samples matched PokeAPI version_details=firered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
