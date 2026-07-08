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
