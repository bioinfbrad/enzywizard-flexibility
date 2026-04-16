from __future__ import annotations

import argparse

from .commands.flexibility import add_flexibility_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="enzywizard-flexibility",
        description="EnzyWizard-Flexibility: Estimate residue flexibility from a cleaned protein structure and generate a detailed JSON report."
    )
    add_flexibility_parser(parser)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)