from pathlib import Path
import yaml

def load_conf(filename: str | Path ) -> dict:
    try:
        fullpath = Path(filename)

        with open(fullpath, "r") as ofile:
            loadconfig = yaml.safe_load(ofile)

        return loadconfig
    except Exception as e:
        raise e