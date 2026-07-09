from pathlib import Path

from api import routes
from api.app import STATIC_DIR


def setup_function():
    routes.reset_vehicle()


def test_frontend_console_asset_exists():
    html = Path(STATIC_DIR / "index.html").read_text(encoding="utf-8")

    assert "Simulator Console" in html
    assert "/static/app.js" in html


def test_vehicle_api_reports_and_updates_simulator_state():
    response = routes.lock_vehicle()

    assert response["state"]["locked"] is True

    response = routes.set_window_percentage(routes.WindowRequest(percentage=45))

    assert response["state"]["window"] == 45

    response = routes.start_climate(routes.ClimateRequest(target_temp=72))

    assert response["state"]["climate_control_on"] is True
    assert response["state"]["target_temp"] == 72

    response = routes.shift_transmission(routes.GearRequest(gear="D"))

    assert response["state"]["transmission"] == "D"


def test_fault_injection_endpoint_reports_detected_failures():
    response = routes.inject_fault(routes.FaultRequest(field="window", value=120))

    assert response["state"]["window"] == 0
    assert response["state"]["detected_failures"][0]["field"] == "window"


def test_legacy_awake_and_charge_routes_still_work():
    assert routes.awake_vehicle()["state"]["awake"] is True
    assert routes.charge_vehicle()["state"]["charging"] is True
    assert routes.stop_charge_vehicle()["state"]["charging"] is False


def test_speedrun_frontend_assets_are_present():
    html = Path(STATIC_DIR / "index.html").read_text(encoding="utf-8")
    js = Path(STATIC_DIR / "app.js").read_text(encoding="utf-8")
    css = Path(STATIC_DIR / "styles.css").read_text(encoding="utf-8")

    assert "Wikipedia Speedrun" in html
    assert "speedrunStrengthGraph" in html
    assert "performance.now()" in js
    assert "requestAnimationFrame" in js
    assert "strength-bar" in css


def test_speedrun_endpoint_returns_cached_wikipedia_links(monkeypatch):
    from api import speedrun

    speedrun._cached_links.cache_clear()

    class DummyResponse:
        status_code = 200
        ok = True
        headers = {}

        def json(self):
            return {
                "query": {
                    "pages": [
                        {
                            "links": [
                                {"title": "Electric car"},
                                {"title": "Battery electric vehicle"},
                            ]
                        }
                    ]
                }
            }

    calls = []

    def fake_get(*args, **kwargs):
        calls.append((args, kwargs))
        return DummyResponse()

    monkeypatch.setattr(speedrun.requests, "get", fake_get)
    monkeypatch.setattr(speedrun.time, "sleep", lambda *_: None)

    first = speedrun.wikipedia_links("Electric vehicle")
    second = speedrun.wikipedia_links("Electric vehicle")

    assert len(calls) == 1
    assert first == second
    assert first[0]["title"] == "Electric car"
    assert 0 <= first[0]["score"] <= 1
    assert calls[0][1]["headers"]["User-Agent"]
