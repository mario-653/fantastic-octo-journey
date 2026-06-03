import pytest
from app import app as flask_app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = False
    return flask_app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def get_index(client):
    return client.get("/")


# ---------------------------------------------------------------------------
# Status code
# ---------------------------------------------------------------------------

class TestStatusCodes:
    def test_index_returns_200(self, client):
        response = get_index(client)
        assert response.status_code == 200

    def test_unknown_route_returns_404(self, client):
        response = client.get("/nonexistent")
        assert response.status_code == 404

    def test_unknown_nested_route_returns_404(self, client):
        response = client.get("/hello/world")
        assert response.status_code == 404

    def test_post_to_index_returns_405(self, client):
        response = client.post("/")
        assert response.status_code == 405

    def test_put_to_index_returns_405(self, client):
        response = client.put("/")
        assert response.status_code == 405

    def test_delete_to_index_returns_405(self, client):
        response = client.delete("/")
        assert response.status_code == 405

    def test_patch_to_index_returns_405(self, client):
        response = client.patch("/")
        assert response.status_code == 405


# ---------------------------------------------------------------------------
# Content-Type
# ---------------------------------------------------------------------------

class TestContentType:
    def test_index_content_type_is_html(self, client):
        response = get_index(client)
        assert "text/html" in response.content_type

    def test_index_content_type_includes_charset(self, client):
        response = get_index(client)
        assert "utf-8" in response.content_type.lower() or "charset" in response.content_type.lower()


# ---------------------------------------------------------------------------
# Response body — structural HTML
# ---------------------------------------------------------------------------

class TestIndexBodyStructure:
    def test_body_contains_doctype(self, client):
        response = get_index(client)
        assert b"<!DOCTYPE html>" in response.data

    def test_body_contains_html_tag(self, client):
        response = get_index(client)
        assert b"<html" in response.data

    def test_body_contains_head_tag(self, client):
        response = get_index(client)
        assert b"<head>" in response.data

    def test_body_contains_body_tag(self, client):
        response = get_index(client)
        assert b"<body>" in response.data

    def test_body_contains_closing_html_tag(self, client):
        response = get_index(client)
        assert b"</html>" in response.data


# ---------------------------------------------------------------------------
# Response body — meta / head content
# ---------------------------------------------------------------------------

class TestIndexHeadContent:
    def test_page_title_is_hello_world(self, client):
        response = get_index(client)
        assert b"<title>Hello, World!</title>" in response.data

    def test_charset_utf8_meta_present(self, client):
        response = get_index(client)
        assert b'charset="UTF-8"' in response.data or b"charset=UTF-8" in response.data

    def test_viewport_meta_present(self, client):
        response = get_index(client)
        assert b"viewport" in response.data

    def test_lang_attribute_is_en(self, client):
        response = get_index(client)
        assert b'lang="en"' in response.data

    def test_google_fonts_preconnect_present(self, client):
        response = get_index(client)
        assert b"fonts.googleapis.com" in response.data

    def test_google_fonts_stylesheet_linked(self, client):
        response = get_index(client)
        assert b"Poppins" in response.data

    def test_css_stylesheet_link_present(self, client):
        response = get_index(client)
        assert b"style.css" in response.data

    def test_static_css_url_is_resolved(self, client):
        response = get_index(client)
        # url_for should render to /static/css/style.css — not a raw Jinja tag
        assert b"{{" not in response.data
        assert b"}}" not in response.data
        assert b"/static/css/style.css" in response.data


# ---------------------------------------------------------------------------
# Response body — visible page content
# ---------------------------------------------------------------------------

class TestIndexPageContent:
    def test_heading_hello_world_present(self, client):
        response = get_index(client)
        assert b"Hello, World!" in response.data

    def test_subtitle_text_present(self, client):
        response = get_index(client)
        assert b"Welcome to my minimal Flask application" in response.data

    def test_badge_built_with_present(self, client):
        response = get_index(client)
        assert b"Built with" in response.data

    def test_badge_flask_version_present(self, client):
        response = get_index(client)
        assert b"Flask 3.0" in response.data

    def test_wave_emoji_present(self, client):
        response = get_index(client)
        # The waving hand emoji encoded in UTF-8
        assert "👋".encode("utf-8") in response.data

    def test_emoji_aria_label_present(self, client):
        response = get_index(client)
        assert b"aria-label" in response.data

    def test_card_class_present(self, client):
        response = get_index(client)
        assert b'class="card"' in response.data

    def test_page_wrapper_class_present(self, client):
        response = get_index(client)
        assert b"page-wrapper" in response.data

    def test_heading_class_present(self, client):
        response = get_index(client)
        assert b'class="heading"' in response.data

    def test_subtitle_class_present(self, client):
        response = get_index(client)
        assert b'class="subtitle"' in response.data

    def test_badge_class_present(self, client):
        response = get_index(client)
        assert b'class="badge"' in response.data

    def test_clean_grow_text_present(self, client):
        response = get_index(client)
        assert b"ready to grow" in response.data


# ---------------------------------------------------------------------------
# Response data encoding
# ---------------------------------------------------------------------------

class TestResponseEncoding:
    def test_response_data_is_bytes(self, client):
        response = get_index(client)
        assert isinstance(response.data, bytes)

    def test_response_data_decodable_as_utf8(self, client):
        response = get_index(client)
        decoded = response.data.decode("utf-8")
        assert "Hello, World!" in decoded

    def test_no_jinja_template_tags_in_output(self, client):
        response = get_index(client)
        text = response.data.decode("utf-8")
        assert "{{" not in text
        assert "}}" not in text
        assert "{%" not in text
        assert "%}" not in text


# ---------------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------------

class TestAppConfiguration:
    def test_testing_flag_is_set(self, app):
        assert app.config["TESTING"] is True

    def test_app_has_index_route(self, app):
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert "/" in rules

    def test_index_route_allows_get(self, app):
        rules = {rule.rule: rule for rule in app.url_map.iter_rules()}
        assert "GET" in rules["/"].methods

    def test_index_route_does_not_allow_post(self, app):
        rules = {rule.rule: rule for rule in app.url_map.iter_rules()}
        assert "POST" not in rules["/"].methods

    def test_app_name(self, app):
        assert app.name == "app"


# ---------------------------------------------------------------------------
# Statelessness / repeated requests
# ---------------------------------------------------------------------------

class TestStatelessness:
    def test_two_sequential_requests_both_return_200(self, client):
        r1 = get_index(client)
        r2 = get_index(client)
        assert r1.status_code == 200
        assert r2.status_code == 200

    def test_two_sequential_requests_return_same_content(self, client):
        r1 = get_index(client)
        r2 = get_index(client)
        assert r1.data == r2.data

    def test_multiple_requests_do_not_degrade(self, client):
        for _ in range(10):
            response = get_index(client)
            assert response.status_code == 200
            assert b"Hello, World!" in response.data


# ---------------------------------------------------------------------------
# HEAD request
# ---------------------------------------------------------------------------

class TestHeadRequest:
    def test_head_request_returns_200(self, client):
        response = client.head("/")
        assert response.status_code == 200

    def test_head_request_returns_no_body(self, client):
        response = client.head("/")
        assert response.data == b""