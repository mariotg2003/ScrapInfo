import json

from functions.create_json import write_json
from functions.read_params import get_info


def test_get_info_reads_json_from_data_directory():
    months = get_info("month")

    assert months["1"] == "Enero"
    assert len(months) == 12


def test_write_json_creates_expected_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    write_json([{"name": "GPU"}], "products")

    output = tmp_path / "datos_products.json"
    assert json.loads(output.read_text(encoding="utf-8")) == [{"name": "GPU"}]
