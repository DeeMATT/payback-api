from fastapi.testclient import TestClient
import pytest
from httpx import AsyncClient


from app import app as application, retrieve_data_set, compute_annual_energy_rate

client = TestClient(application)


@pytest.fixture
def annual_energy_production_in_watts():
    """
    compute the ex ante (predicted) energy in W produced per Wp
    """
    data_set = retrieve_data_set(
        'datafiles/SPP2023-ex-ante-v20.xlsx',
        ['5414492999998'],
    )
    annual_energy_produced = compute_annual_energy_rate(data_set)

    return annual_energy_produced


@pytest.fixture
def annual_energy_consumption_in_kWh():
    """
    compute the annual energy consumption spread over the year for every kWh
    """
    data_set = retrieve_data_set(
        'datafiles/rlp0n2023-electricity-all-dsos.xlsx',
        ['5414492999998'],
        skiprows=[0, 1]
    )
    annual_energy_consumed = compute_annual_energy_rate(data_set)

    return annual_energy_consumed


@pytest.mark.asyncio
async def test_compute_payback_time(annual_energy_production_in_watts, annual_energy_consumption_in_kWh):
    """
    Test solar panel payback time API
    """

    average_watts_peak_by_hour = annual_energy_production_in_watts / (365 * 24)

    annual_energy_consumed = annual_energy_consumption_in_kWh

    requestData = {
        "annual_energy_consumption": annual_energy_consumed,
        "installation_cost": 15000,
        "installation_wp": average_watts_peak_by_hour
    }

    async with AsyncClient(app=application, base_url="http://test") as ac:
        response = await ac.post("/payback_time", json=requestData)

    assert response.status_code == 200
