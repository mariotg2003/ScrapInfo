from functions import get_url


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
