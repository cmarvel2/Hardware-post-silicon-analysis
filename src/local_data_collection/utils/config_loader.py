from pathlib import Path
import yaml

def load_conf(filename: str | Path ) -> dict:
    root = Path(__file__).resolve().parents[3]
    targetpath = root / "conf" / "conf_local_data_collection" / filename
    

    with open(targetpath, "r") as ofile:
        loadconfig = yaml.safe_load(ofile)

    return loadconfig
