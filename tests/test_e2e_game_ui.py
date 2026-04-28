"""
Checks E2E UI minimaux pour la page de jeu.
"""

# pyright: reportMissingImports=false, reportUnknownMemberType=false, reportUnknownVariableType=false

from __future__ import annotations

import socket
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

from playwright.sync_api import sync_playwright
from werkzeug.serving import make_server

from app import create_app


def _get_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


class _ServerThread(threading.Thread):
    def __init__(self, port: int) -> None:
        super().__init__(daemon=True)
        app = create_app()
        app.config["TESTING"] = True
        self._server = make_server("127.0.0.1", port, app)

    def run(self) -> None:
        self._server.serve_forever()

    def shutdown(self) -> None:
        self._server.shutdown()


@contextmanager
def _new_page() -> Iterator[tuple[Any, str]]:
    port = _get_free_port()
    server = _ServerThread(port=port)
    server.start()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(base_url=f"http://127.0.0.1:{port}")
        page = context.new_page()
        try:
            yield page, f"http://127.0.0.1:{port}"
        finally:
            context.close()
            browser.close()
            server.shutdown()
            server.join(timeout=2)


def test_instant_button_stays_synced_with_accessibility_text_speed() -> None:
    with _new_page() as (page, base_url):
        page.goto(f"{base_url}/game", wait_until="domcontentloaded")
        page.wait_for_selector("#instant-btn")
        page.wait_for_selector("#access-btn")

        # Active d'abord le mode instantané via le raccourci header.
        page.click("#instant-btn")
        instant_active = page.eval_on_selector(
            "#instant-btn", "el => el.classList.contains('active')"
        )
        assert instant_active is True

        # Puis repasse en vitesse normale via la modale accessibilité.
        page.click("#access-btn")
        page.select_option("#acc-text-speed", "normal")

        instant_flag = page.evaluate("() => localStorage.getItem('luna_instant')")
        assert instant_flag == "off"
        instant_active_after = page.eval_on_selector(
            "#instant-btn", "el => el.classList.contains('active')"
        )
        assert instant_active_after is False


def test_choice_double_click_sends_single_story_choice_request() -> None:
    with _new_page() as (page, base_url):
        page.goto(f"{base_url}/game", wait_until="domcontentloaded")
        page.wait_for_selector("#choices-container .choice-btn")

        # Compte uniquement les requêtes métier de choix.
        choice_requests = {"count": 0}

        def on_request(req: Any) -> None:
            if req.method == "POST" and req.url.endswith("/api/story/choice"):
                choice_requests["count"] += 1

        page.on("request", on_request)

        first_choice = page.locator("#choices-container .choice-btn").first
        first_choice.dblclick()

        # Laisse le temps aux requêtes de partir.
        page.wait_for_timeout(700)
        assert choice_requests["count"] == 1


def test_journal_modal_shows_connection_error_when_api_unreachable() -> None:
    with _new_page() as (page, base_url):
        page.goto(f"{base_url}/game", wait_until="domcontentloaded")
        page.wait_for_selector("#journal-btn")

        # Simule un offline partiel pour l'API journal.
        def abort_journal_route(route: Any) -> None:
            route.abort()

        page.route("**/api/story/journal", abort_journal_route)

        page.click("#journal-btn")
        page.wait_for_selector("#journal-modal.visible")
        page.wait_for_selector("#journal-modal-text")

        journal_text = page.inner_text("#journal-modal-text")
        assert "Connexion perdue." in journal_text
