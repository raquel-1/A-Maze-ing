#!/usr/bin/env python3

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}


def parse_config(filepath: str) -> dict:
	