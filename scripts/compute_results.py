"""
Recomputes the numbers reported in the paper from the files of this repository.

Usage: python3 scripts/compute_results.py

Standard library only. Each number is checked against the value in the paper.
"""

import collections
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EVALUATION = ROOT / "evaluation"
RECONSTRUCTION = EVALUATION / "reconstruction-2026-10-15"
UNSURE = "I don't know"
TYPES = ["micro frontend", "screen", "fragment", "composition", "navigation", "communication",
         "API call", "state access"]


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def pct(part: float, whole: float) -> str:
    return f"{part / whole:.0%}" if whole else "—"


def majority(votes: list[str], severity: list[str]) -> str:
    """Most frequent answer among those given; ties go to the most severe one."""

    counts = collections.Counter(vote for vote in votes if vote)
    if not counts:
        return ""
    top = max(counts.values())
    return next(answer for answer in severity if counts.get(answer) == top)


def load(system: str, name: str) -> list[dict]:
    return json.loads((RECONSTRUCTION / system / f"{name}.json").read_text(encoding="utf-8"))


def count_system(system: str) -> collections.Counter:
    units = load(system, "microfrontends")
    counts = collections.Counter()
    counts["micro frontend"] = len(units)
    counts["screen"] = sum(len(u.get("screens") or []) for u in units)
    counts["fragment"] = sum(len(u.get("fragments") or []) for u in units)
    counts["composition"] = len(load(system, "compositions"))
    counts["navigation"] = len(load(system, "navigations"))
    counts["communication"] = sum(1 for i in load(system, "communications") if i.get("directed", True))
    counts["API call"] = len(load(system, "api_calls"))
    counts["state access"] = len(load(system, "state_accesses"))
    return counts


def count_mfe(system: str, mfe: str, directory: str) -> collections.Counter:
    unit = next(u for u in load(system, "microfrontends")
                if u["id"] == mfe and (not directory or u.get("directory") == directory))
    counts = collections.Counter()
    counts["micro frontend"] = 1
    counts["screen"] = len(unit.get("screens") or [])
    counts["fragment"] = len(unit.get("fragments") or [])
    counts["composition"] = sum(mfe in (i["consumer"], i["provider"]) for i in load(system, "compositions"))
    counts["navigation"] = sum(mfe in (i["source"], i["target"]) for i in load(system, "navigations"))
    counts["communication"] = sum(mfe in (i["source"], i["target"]) and i.get("directed", True)
                                  for i in load(system, "communications"))
    counts["API call"] = sum(i["microfrontend"] == mfe for i in load(system, "api_calls"))
    counts["state access"] = sum(i["microfrontend"] == mfe for i in load(system, "state_accesses"))
    return counts


def rq1() -> None:
    sample = [row for row in read(EVALUATION / "rq1-reconstruction" / "precision" / "sample-and-verdicts.csv")
              if row["in_evaluated_systems"] == "True"]
    systems = sorted({row["system"] for row in sample})
    population = sum((count_system(system) for system in systems), collections.Counter())

    precision = collections.defaultdict(collections.Counter)
    for row in sample:
        precision[row["type"]][row["consensus"]] += 1

    drawn = read(EVALUATION / "rq1-reconstruction" / "recall" / "sampled-mfes.csv")
    extracted = sum((count_mfe(r["system"], r["mfe"], r["directory"]) for r in drawn), collections.Counter())
    omissions = {row["item"]: row for row in read(EVALUATION / "rq1-reconstruction" / "recall" / "omissions-verified.csv")}
    missed = collections.Counter(row["type"] for row in omissions.values() if row["final_outcome"] == "false negative")

    print("RQ1 — reconstruction")
    print("type | extracted | sampled | correct | partial | incorrect | precision | in sampled MFEs | missed | recall")
    total = collections.Counter()
    weighted = [0.0, 0]
    for kind in TYPES:
        c = precision[kind]
        judged = c["correct"] + c["partial"] + c["incorrect"]
        print(f"{kind} | {population[kind]} | {sum(c.values())} | {c['correct']} | {c['partial']} | {c['incorrect']} | "
              f"{pct(c['correct'], judged)} | {extracted[kind]} | {missed[kind]} | "
              f"{pct(extracted[kind], extracted[kind] + missed[kind])}")
        total.update(c)
        weighted[0] += population[kind] * c["correct"] / judged
        weighted[1] += population[kind]
    judged = total["correct"] + total["partial"] + total["incorrect"]
    found, lost = sum(extracted.values()), sum(missed.values())
    print(f"total | {sum(population.values())} | {judged} | {total['correct']} | {total['partial']} | "
          f"{total['incorrect']} | {pct(total['correct'], judged)} | {found} | {lost} | {pct(found, found + lost)}")
    print(f"precision weighted by the extracted elements: {weighted[0] / weighted[1]:.0%}")

    assert sum(population.values()) == 3352
    assert (judged, total["correct"], total["partial"], total["incorrect"]) == (361, 331, 9, 21)
    assert (len(drawn), found, lost) == (19, 1137, 62)


def rq2() -> None:
    rows = read(EVALUATION / "rq2-detection" / "evaluated-set" / "detections-and-llm-verdicts.csv")
    by_pattern = collections.defaultdict(collections.Counter)
    for row in rows:
        by_pattern[row["anti_pattern"]][row["consensus"]] += 1
    false_negatives = {"nano-frontend": 1}

    print("\nRQ2 — LLM judges (consensus of the three)")
    print("anti-pattern | detections | Yes | No | I don't know | precision | recall")
    total = collections.Counter()
    for name, c in sorted(by_pattern.items()):
        fn = false_negatives.get(name, 0)
        print(f"{name} | {sum(c.values())} | {c['Yes']} | {c['No']} | {c[UNSURE]} | "
              f"{pct(c['Yes'], c['Yes'] + c['No'])} | {pct(c['Yes'], c['Yes'] + fn)}")
        total.update(c)
    print(f"total | {len(rows)} | {total['Yes']} | {total['No']} | {total[UNSURE]} | "
          f"{pct(total['Yes'], total['Yes'] + total['No'])} | {pct(total['Yes'], total['Yes'] + 1)}")
    hammering = by_pattern["hammering-apis"]
    rest = total - hammering
    print(f"without Hammering APIs: {pct(rest['Yes'], rest['Yes'] + rest['No'])}")
    assert (len(rows), total["Yes"], total["Yes"] + total["No"]) == (159, 137, 157)

    answers = read(EVALUATION / "rq2-detection" / "practitioners" / "answers.csv")
    severity = ["No", UNSURE, "Yes"]
    confirmed = collections.Counter()
    lines = collections.Counter()
    at_least_one = 0
    for row in answers:
        verdict = majority([row["C1"], row["C2"], row["C3"]], severity)
        lines[row["anti_pattern"]] += 1
        confirmed[row["anti_pattern"]] += verdict == "Yes"
        at_least_one += "Yes" in (row["C1"], row["C2"], row["C3"])

    print("\nRQ2 — practitioners (majority of the respondents)")
    print("anti-pattern | rows | confirmed | precision")
    for name in sorted(lines):
        print(f"{name} | {lines[name]} | {confirmed[name]} | {pct(confirmed[name], lines[name])}")
    print(f"total | {len(answers)} | {sum(confirmed.values())} | {pct(sum(confirmed.values()), len(answers))}")
    print(f"rows with at least one Yes: {at_least_one}")
    assert (len(answers), sum(confirmed.values()), at_least_one) == (42, 25, 39)


if __name__ == "__main__":
    rq1()
    rq2()
