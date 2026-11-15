import json
from pathlib import Path

MANIFEST = json.loads((Path(__file__).resolve().parents[1] / "data" / "plugin.json").read_text(encoding="utf-8"))


def test_existing_installs_keep_their_id_and_keyword():
    assert MANIFEST["ID"] == "E6AC0CD2BDD84AFE9E7D4BBCDEB0BF11"
    assert MANIFEST["ActionKeyword"] == "h"


def test_runs_on_python_v2():
    assert MANIFEST["Language"] == "python_v2"
    assert MANIFEST["ExecuteFileName"] == "run.py"


def test_description_matches_the_plugin():
    assert "Plex" not in MANIFEST["Description"]
    assert "WSL" in MANIFEST["Description"]
