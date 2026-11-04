#!/usr/bin/env python3
"""Local, provider-neutral gate controller for CodeAtlas multi-agent TDD."""
from __future__ import annotations
import argparse
import datetime as dt
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / ".artifacts"
PHASES = ["plan", "tests", "test_review", "red", "implement", "green", "refactor", "docs", "review", "ci", "complete"]
REQUIRED = {
    "plan": ["feature-plan.md", "api-contract.md"],
    "tests": ["frontend-test-report.md", "backend-test-report.md"],
    "test_review": ["test-review-report.md"],
    "implement": ["implementation-report.md"],
    "refactor": ["refactor-report.md"],
    "docs": ["documentation-report.md"],
    "review": ["review-report.md"],
    "ci": ["final-verification.md"],
}
ROLES = {
    "plan": "Planner",
    "tests": "Frontend Test Engineer + Backend Test Engineer (parallel)",
    "test_review": "Test Reviewer",
    "red": "Orchestrator / test runner",
    "implement": "Frontend Implementer + Backend Implementer (parallel where safe)",
    "green": "Orchestrator / test runner",
    "refactor": "Implementers",
    "docs": "Documentation Engineer",
    "review": "Independent Reviewer",
    "ci": "Orchestrator / CI verifier",
}


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def feature_dir(slug: str) -> Path:
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Feature slug must use lowercase letters, numbers and single hyphens.")
    path = (ARTIFACTS / slug).resolve()
    if ARTIFACTS.resolve() not in path.parents:
        raise ValueError("Invalid feature path")
    return path


def load_state(folder: Path) -> dict:
    state_file = folder / "workflow.json"
    if not state_file.is_file():
        raise ValueError(f"No workflow found in {folder}. Run: python tools/orchestrate.py start --feature <slug>")
    return json.loads(state_file.read_text(encoding="utf-8"))


def save_state(folder: Path, state: dict) -> None:
    state["updated_at"] = now()
    target = folder / "workflow.json"
    temp = target.with_suffix(".json.tmp")
    temp.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
    temp.replace(target)


def write_report(folder: Path, name: str, content: str) -> None:
    target = folder / name
    if target.exists():
        raise ValueError(f"Refusing to overwrite existing evidence: {target}. Review it and remove it explicitly before rerunning.")
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def status_line(path: Path, expected: str) -> bool:
    if not path.is_file():
        return False
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()[:5]
    return any(line.strip().lower() == f"status: {expected}".lower() for line in lines)


def cmd_start(args: argparse.Namespace) -> int:
    folder = feature_dir(args.feature)
    if folder.exists() and any(folder.iterdir()):
        print(f"ERROR: {folder} already exists and is not empty", file=sys.stderr)
        return 2
    folder.mkdir(parents=True, exist_ok=True)
    state = {"feature": args.feature, "phase": "plan", "created_at": now(), "updated_at": now(), "test_commands": {}, "history": [{"phase": "plan", "at": now(), "event": "started"}]}
    save_state(folder, state)
    print(f"Started TDD workflow: {args.feature}\nCurrent phase: plan\nNext: python tools/orchestrate.py prompt --feature {args.feature}")
    return 0


def prompt_text(feature: str, phase: str, folder: Path) -> str:
    outputs = REQUIRED.get(phase, [])
    outputs_text = "\n".join(f"- `{name}`" for name in outputs) or "- See the phase-specific evidence instructions below."
    common = f"Feature: {feature}\nArtifact directory: `{folder.relative_to(ROOT)}`\nRead `AGENTS.md`, `docs/TDD_WORKFLOW.md` and `docs/AGENT_HANDOFF_CONTRACT.md` first. Read predecessor evidence before starting. Do not fabricate commands, results or behavior."
    instructions = {
        "plan": "Act as Planner. Read product requirements and acceptance criteria. Define scope, map criteria to FE and BE behavior, select stack and test commands, define file ownership and a shared API/interface contract. Do not write tests or production code.",
        "tests": "Delegate to two independent roles: (1) Frontend Test Engineer writes FE tests only; (2) Backend Test Engineer writes BE tests only. Both use the approved plan and same API contract, work in separate files, and report exact commands and criteria mapping. No production implementation.",
        "test_review": "Act as independent Test Reviewer. Review both test suites for criteria traceability, API contract consistency, meaningful assertions, edge cases, deterministic setup and expected failure behavior. Do not implement production code. First line of report must be `Status: APPROVED` or `Status: CHANGES_REQUESTED`.",
        "red": "Run the FE and BE test commands from the approved plan before implementation. Use `verify-red` with both commands. Failures must represent missing behavior, not broken test setup. Inspect and explain failures.",
        "implement": "Delegate to two implementers where file ownership allows: (1) Frontend Implementer implements FE production code; (2) Backend Implementer implements BE production code. They work only against reviewed tests and the locked contract. They must not modify, delete, skip or weaken tests.",
        "green": "Run the exact FE and BE test commands recorded during RED using `verify-green`. Both suites must pass. Do not change tests to obtain GREEN.",
        "refactor": "Refactor for clarity and maintainability without changing observable behavior. Run focused and full tests. Do not weaken tests. Record changes and verification.",
        "docs": "Act as Documentation Engineer. Read plan, API contract, implementation diff and observed test evidence. Update docs to describe actual behavior, setup, API shapes and limitations. Do not invent behavior.",
        "review": "Act as independent Reviewer. Review acceptance coverage, test quality, architecture, security/data policy, implementation and docs. Report findings by severity. First line must be `Status: APPROVED` or `Status: CHANGES_REQUESTED`.",
        "ci": "Run the full repository checks and inspect the relevant GitHub Actions result. Record exact commands, outcomes, CI status and unresolved risks. First line must be `Status: PASS` or `Status: FAIL`.",
    }
    return f"# Agent task: {ROLES[phase]}\n\n{common}\n\n## Instructions\n{instructions[phase]}\n\n## Required outputs\n{outputs_text}\n\n## Gate\nDo not advance the workflow yourself. The human/orchestrator runs `python tools/orchestrate.py advance --feature {feature}` after reviewing your evidence."


def cmd_prompt(args: argparse.Namespace) -> int:
    folder = feature_dir(args.feature)
    state = load_state(folder)
    phase = state["phase"]
    if phase == "complete":
        print("Workflow is complete.")
        return 0
    print(prompt_text(args.feature, phase, folder))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    folder = feature_dir(args.feature)
    state = load_state(folder)
    print(f"Feature: {state['feature']}\nPhase: {state['phase']}\nUpdated: {state['updated_at']}")
    for phase in PHASES[:-1]:
        marker = "-->" if phase == state["phase"] else ("[x]" if PHASES.index(phase) < PHASES.index(state["phase"]) else "[ ]")
        print(f"{marker} {phase}")
    return 0


def cmd_advance(args: argparse.Namespace) -> int:
    folder = feature_dir(args.feature)
    state = load_state(folder)
    phase = state["phase"]
    if phase in ("red", "green"):
        print(f"Use verify-{phase}; this phase requires actually running the recorded test commands.", file=sys.stderr)
        return 2
    if phase == "complete":
        print("Workflow is already complete.")
        return 0
    missing = [name for name in REQUIRED.get(phase, []) if not (folder / name).is_file()]
    if missing:
        print("Cannot advance; missing evidence:\n" + "\n".join(f"- {name}" for name in missing), file=sys.stderr)
        return 2
    gate_file = {"test_review": "test-review-report.md", "review": "review-report.md", "ci": "final-verification.md"}.get(phase)
    expected = {"test_review": "APPROVED", "review": "APPROVED", "ci": "PASS"}.get(phase)
    if gate_file and not status_line(folder / gate_file, expected):
        print(f"Cannot advance; first five lines of {gate_file} must include `Status: {expected}`.", file=sys.stderr)
        return 2
    next_phase = PHASES[PHASES.index(phase) + 1]
    state["history"].append({"phase": phase, "at": now(), "event": "gate_passed", "next": next_phase})
    state["phase"] = next_phase
    save_state(folder, state)
    print(f"Gate passed: {phase}\nNext phase: {next_phase}")
    if next_phase != "complete":
        print(f"Generate next task: python tools/orchestrate.py prompt --feature {args.feature}")
    return 0


def run_test_command(label: str, command: str) -> dict:
    argv = shlex.split(command)
    if not argv:
        raise ValueError(f"Empty {label} test command")
    # shell=False: command text is tokenized, never interpreted by a shell.
    result = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300, check=False)
    return {"label": label, "command": command, "exit_code": result.returncode, "output": result.stdout[-12000:]}


def cmd_verify_red(args: argparse.Namespace) -> int:
    folder = feature_dir(args.feature)
    state = load_state(folder)
    if state["phase"] != "red":
        print(f"RED verification is not the current phase (current: {state['phase']}).", file=sys.stderr)
        return 2
    try:
        results = [run_test_command("frontend", args.frontend_cmd), run_test_command("backend", args.backend_cmd)]
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"Could not run test command: {exc}", file=sys.stderr)
        return 2
    if any(item["exit_code"] == 0 for item in results):
        print("RED gate failed: both FE and BE test commands must currently fail. If a layer is already implemented, document and review that exception instead of forcing a failure.", file=sys.stderr)
        for item in results:
            print(f"{item['label']}: exit {item['exit_code']}")
        return 2
    state["test_commands"] = {item["label"]: item["command"] for item in results}
    report = ["Status: RED_CONFIRMED", "", "Both test commands exited non-zero before implementation. Inspect outputs below and confirm failures represent missing behavior rather than test setup errors.", ""]
    for item in results:
        report += [f"## {item['label']} — exit {item['exit_code']}", f"Command: `{item['command']}`", "```text", item["output"], "```", ""]
    write_report(folder, "red-phase-report.md", "\n".join(report))
    state["history"].append({"phase": "red", "at": now(), "event": "commands_failed_as_expected"})
    state["phase"] = "implement"
    save_state(folder, state)
    print("RED evidence recorded. Current phase: implement")
    return 0


def cmd_verify_green(args: argparse.Namespace) -> int:
    folder = feature_dir(args.feature)
    state = load_state(folder)
    if state["phase"] != "green":
        print(f"GREEN verification is not the current phase (current: {state['phase']}).", file=sys.stderr)
        return 2
    commands = state.get("test_commands", {})
    if set(commands) != {"frontend", "backend"}:
        print("Missing recorded FE/BE test commands from RED phase.", file=sys.stderr)
        return 2
    try:
        results = [run_test_command(label, commands[label]) for label in ("frontend", "backend")]
    except (ValueError, subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"Could not run test command: {exc}", file=sys.stderr)
        return 2
    if any(item["exit_code"] != 0 for item in results):
        print("GREEN gate failed. Keep the workflow in this phase and repair without changing tests.", file=sys.stderr)
        for item in results:
            print(f"{item['label']}: exit {item['exit_code']}")
        return 2
    report = ["Status: GREEN_CONFIRMED", "", "Both recorded test commands exited zero after implementation.", ""]
    for item in results:
        report += [f"## {item['label']} — exit {item['exit_code']}", f"Command: `{item['command']}`", "```text", item["output"], "```", ""]
    write_report(folder, "green-phase-report.md", "\n".join(report))
    state["history"].append({"phase": "green", "at": now(), "event": "all_tests_passed"})
    state["phase"] = "refactor"
    save_state(folder, state)
    print("GREEN evidence recorded. Current phase: refactor")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Gate controller for CodeAtlas multi-agent TDD")
    sub = parser.add_subparsers(dest="command", required=True)
    for name, func in [("start", cmd_start), ("prompt", cmd_prompt), ("status", cmd_status), ("advance", cmd_advance)]:
        item = sub.add_parser(name)
        item.add_argument("--feature", required=True)
        item.set_defaults(func=func)
    red = sub.add_parser("verify-red")
    red.add_argument("--feature", required=True)
    red.add_argument("--frontend-cmd", required=True)
    red.add_argument("--backend-cmd", required=True)
    red.set_defaults(func=cmd_verify_red)
    green = sub.add_parser("verify-green")
    green.add_argument("--feature", required=True)
    green.set_defaults(func=cmd_verify_green)
    return parser


if __name__ == "__main__":
    try:
        parsed = build_parser().parse_args()
        raise SystemExit(parsed.func(parsed))
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(2)
