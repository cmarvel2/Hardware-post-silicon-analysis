from pathlib import Path
import yaml

def load_conf(filename: str) -> dict:
    path = Path(__file__).resolve().parents[1] / "config_files"

    destfile = fr"{path}\{filename}"

    with open(destfile, "r") as ofile:
        loadconfig = yaml.safe_load(ofile)

    return loadconfig