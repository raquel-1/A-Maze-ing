#!/usr/bin/env python3

def parse_config(filepath: str) -> dict[str, object]:
    """read file and extract strings"""
    required_keys = {
        "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
    }
    optional_keys = {"SEED"}
    valid_keys = required_keys | optional_keys

    red = "\033[91m"
    reset = "\033[0m"

    # config.txt
    filename = filepath.replace('\\', '/').split('/')[-1]
    if filename != "config.txt":
        raise ValueError(
            f"{red}The file must be named exactly 'config.txt', "
            f"got: {filename}{reset}"
        )
    try:
        raw: dict[str, str] = {}
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '#' in line:
                    line = line.split('#')[0].strip()
                    if not line:
                        continue
                if '=' not in line:
                    raise ValueError(
                        f"{red}Invalid format (missing '='): {line}{reset}"
                    )
                k, v = line.split('=', 1)
                k = k.strip()
                v = v.strip()
                if k not in valid_keys:
                    raise ValueError(f"{red}Unknown key: {k}{reset}")
                if k in raw:
                    raise ValueError(f"{red}Duplicate key: {k}{reset}")
                raw[k] = v
    except FileNotFoundError:
        raise FileNotFoundError(
            f"{red}Config file not found: {filepath}{reset}"
        )
    missing = required_keys - raw.keys()
    if missing:
        raise ValueError(
            f"{red}Missing required keys: {', '.join(missing)}{reset}"
        )

    return _validate(raw)


def _validate(raw: dict[str, str]) -> dict[str, object]:
    """convert -> validate values"""
    red = "\033[91m"
    reset = "\033[0m"

    config: dict[str, object] = {}
    # WIDTH
    try:
        width = int(raw["WIDTH"])
    except ValueError:
        raise ValueError(
            f"{red}WIDTH must be an integer, got: {raw['WIDTH']}{reset}"
        )
    if width <= 0:
        raise ValueError(
            f"{red}WIDTH must be greater than 0, got: {width}{reset}"
        )
    config["width"] = width
    # HEIGHT
    try:
        height = int(raw["HEIGHT"])
    except ValueError:
        raise ValueError(
            f"{red}HEIGHT must be an integer, got: {raw['HEIGHT']}{reset}"
        )
    if height <= 0:
        raise ValueError(
            f"{red}HEIGHT must be greater than 0, got: {height}{reset}"
        )
    config["height"] = height
    # -ENTRY-
    config["entry"] = _validate_coords(
        "ENTRY", raw["ENTRY"], width, height
    )
    # -EXIT-
    config["exit"] = _validate_coords(
        "EXIT", raw["EXIT"], width, height
    )
    if config["entry"] == config["exit"]:
        raise ValueError(f"{red}ENTRY and EXIT must be different cells{reset}")
    # OUTPUT_FILE
    if not raw["OUTPUT_FILE"]:
        raise ValueError(f"{red}OUTPUT_FILE cannot be empty{reset}")
    name_no_txt = raw["OUTPUT_FILE"][:-4]  # Quita el '.txt'
    if not raw["OUTPUT_FILE"].endswith('.txt') or name_no_txt.strip('.') == "":
        raise ValueError(
            f"{red}OUTPUT_FILE must be a valid filename ending with .txt, "
            f"got: {raw['OUTPUT_FILE']}{reset}"
        )
    config["output_file"] = raw["OUTPUT_FILE"]
    # PERFEcT
    if raw["PERFECT"] not in ("True", "False"):
        raise ValueError(
            f"{red}PERFECT must be True or False, got: {raw['PERFECT']}{reset}"
        )
    config["perfect"] = raw["PERFECT"] == "True"
    # SEEDoptional
    if "SEED" in raw:
        try:
            config["seed"] = int(raw["SEED"])
        except ValueError:
            raise ValueError(
                f"{red}SEED must be an integer, got: {raw['SEED']}{reset}"
            )
    else:
        config["seed"] = None

    return config


def _validate_coords(
    key: str, value: str, width: int, height: int
) -> tuple[int, int]:
    """parse -> validate coordinates"""
    red = "\033[91m"
    yellow = "\033[93m"
    reset = "\033[0m"

    parts = value.split(',')
    if len(parts) != 2:
        raise ValueError(
            f"{red}{key} must be in format x,y got: {value}{reset}"
        )
    try:
        x, y = int(parts[0].strip()), int(parts[1].strip())
    except ValueError:
        raise ValueError(
            f"{red}{key} coordinates must be integers, got: {value}{reset}"
        )
    if x < 0 or x >= width or y < 0 or y >= height:
        if key == "ENTRY":
            raise ValueError(
                f"{red}{key} ({x},{y}) is outside the maze {width}x{height}. "
                f"{yellow}Please use (0,0){reset}"
            )
        elif key == "EXIT":
            raise ValueError(
                f"{red}{key} ({x},{y}) is outside the maze {width}x{height}. "
                f"{yellow}Please use ({width - 1},{height - 1}){reset}"
            )
        else:
            raise ValueError(
                f"{red}{key} ({x},{y}) is outside the "
                f"maze {width}x{height}{reset}"
            )
    return (x, y)
