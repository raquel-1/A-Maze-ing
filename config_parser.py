#!/usr/bin/env python3

REQUIRED_KEYS = {"WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"}
OPTIONAL_KEYS = {"SEED"}
VALID_KEYS = REQUIRED_KEYS | OPTIONAL_KEYS


def parse_config(filepath: str) -> dict[str, object]:
    """read file and extract strings"""
    try:
        raw: dict[str, str] = {}
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    raise ValueError(f"Invalid format (missing '='): {line}")
                k, v = line.split('=', 1)
                k = k.strip().upper()
                v = v.strip()
                if '#' in v:
                    v = v.split('#')[0].strip()
                if k not in VALID_KEYS:
                    raise ValueError(f"Unknown key: {k}")
                if k in raw:
                    raise ValueError(f"Duplicate key: {k}")
                raw[k] = v
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file not found: {filepath}")
    missing = REQUIRED_KEYS - raw.keys()
    if missing:
        raise ValueError(f"Missing required keys: {', '.join(missing)}")

    return _validate(raw)


def _validate(raw: dict[str, str]) -> dict[str, object]:
    """convert -> validate values"""
    config: dict[str, object] = {}
    # WIDTH
    try:
        config["width"] = int(raw["WIDTH"])
    except ValueError:
        raise ValueError(f"WIDTH must be an integer, got: {raw['WIDTH']}")
    if config["width"] <= 0:
        raise ValueError(
            f"WIDTH must be greater than 0, got: {config['width']}"
        )
    # HEIGHT
    try:
        config["height"] = int(raw["HEIGHT"])
    except ValueError:
        raise ValueError(f"HEIGHT must be an integer, got: {raw['HEIGHT']}")
    if config["height"] <= 0:
        raise ValueError(
            f"HEIGHT must be greater than 0, got: {config['height']}"
        )
    # -ENTRY-
    config["entry"] = _validate_coords(
        "ENTRY", raw["ENTRY"], config["width"], config["height"]
    )
    # -EXIT-
    config["exit"] = _validate_coords(
        "EXIT", raw["EXIT"], config["width"], config["height"]
    )
    if config["entry"] == config["exit"]:
        raise ValueError("ENTRY and EXIT must be different cells")
    # OUTPUT_FILE
    if not raw["OUTPUT_FILE"]:
        raise ValueError("OUTPUT_FILE cannot be empty")
    if not raw["OUTPUT_FILE"].endswith('.txt'):
        raise ValueError(
            f"OUTPUT_FILE must end with .txt, got: {raw['OUTPUT_FILE']}"
        )
    config["output_file"] = raw["OUTPUT_FILE"]
    # PERFEcT
    if raw["PERFECT"] not in ("True", "False"):
        raise ValueError(
            f"PERFECT must be True or False, got: {raw['PERFECT']}"
        )
    config["perfect"] = raw["PERFECT"] == "True"
    # SEEDoptional
    if "SEED" in raw:
        try:
            config["seed"] = int(raw["SEED"])
        except ValueError:
            raise ValueError(f"SEED must be an integer, got: {raw['SEED']}")
    else:
        config["seed"] = None

    return config


def _validate_coords(
    key: str, value: str, width: int, height: int
) -> tuple[int, int]:
    """parse -> validate coordinates"""
    parts = value.split(',')
    if len(parts) != 2:
        raise ValueError(f"{key} must be in format x,y, got: {value}")
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError(f"{key} coordinates must be integers, got: {value}")
    if x < 0 or x >= width or y < 0 or y >= height:
        raise ValueError(
            f"{key} ({x},{y}) is outside the maze {width}x{height}"
        )
    return (x, y)
