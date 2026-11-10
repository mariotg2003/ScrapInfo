from functions import get_url
import pytest


def test_get_html_body_returns_soup_for_successful_response(monkeypatch):
    class Response:
        status_code = 200
        text = "<html><body><h1>OK</h1></body></html>"

    monkeypatch.setenv("SCRAPE_TOKEN", " token ")
    monkeypatch.setattr(get_url.requests, "get", lambda *args, **kwargs: Response())

    result = get_url.get_html_body("https://example.com")

    assert result.h1.text == "OK"


def test_get_html_body_returns_none_without_token(monkeypatch):
    monkeypatch.delenv("SCRAPE_TOKEN", raising=False)

    assert get_url.get_html_body("https://example.com") is None


def test_fallback_is_skipped_when_primary_succeeds(monkeypatch):
    calls = []
    result = object()

    def fetch(url):
        calls.append(url)
        return result

    monkeypatch.setattr(get_url, "get_html_body", fetch)
    assert get_url.get_html_body_with_fallback("primary", "backup") is result
    assert calls == ["primary"]


def test_fallback_is_tried_after_primary_failure(monkeypatch, capsys):
    calls = []
    result = object()

    def fetch(url):
        calls.append(url)
        return result if url == "backup" else None

    monkeypatch.setattr(get_url, "get_html_body", fetch)
    assert get_url.get_html_body_with_fallback("primary", "backup") is result
    assert calls == ["primary", "backup"]
    output = capsys.readouterr().out
    assert "Intentando URL principal: primary" in output
    assert "Intentando URL de respaldo: backup" in output
    assert "HTML obtenido correctamente desde URL de respaldo: backup" in output
    assert "HTML obtenido correctamente desde URL principal" not in output


@pytest.mark.parametrize("backup, expected", [("", ["primary"]), ("backup", ["primary", "backup"])])
def test_fallback_reports_failure(monkeypatch, backup, expected):
    calls = []

    def fetch(url):
        calls.append(url)
        return None

    monkeypatch.setattr(get_url, "get_html_body", fetch)
    with pytest.raises(RuntimeError, match="No se pudo obtener HTML"):
        get_url.get_html_body_with_fallback("primary", backup)
    assert calls == expected
