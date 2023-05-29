from statistics import mean
from fastapi import FastAPI
from app.utils import (
    energy_savings_cost, 
    retrieve_data_set,
    number_of_solar_panels_with_shortest_payback_time
)
from .schema import PaybackSchema, PaybackResponse


app = FastAPI()


@app.post('/payback_time')
async def compute_payback_time(data: PaybackSchema, response_model=PaybackResponse):
    """
    Computes the payback time of solar panels.

    # Args:
    #     annual_energy_consumption: The annual energy consumption in kWh.
    #     installation_cost: The cost of the installation in EUR.
    #     installation_wp: The watt peak of the installation.

    Returns:
        The number of years it takes for the installation to be paid back as well as the optimal solution given the input parameters.
    """
    annual_energy_consumption = data.annual_energy_consumption

    # retrieve list of belpex price each represented in €/mWh
    belpex_price_list = retrieve_data_set(
        'datafiles/SpotBelpex-2022.xlsx',
        ['Euro'],
    )

    # average electricity price based on belpex price for a year
    average_belpex_price_per_kWh = round(mean(belpex_price_list), 3) / 1000

    # consumed energy cost by average belpex price
    cost_of_consumed_energy = annual_energy_consumption * average_belpex_price_per_kWh

    # add/subtract cost of energy difference to installation cost
    installation_cost_after_energy_difference = energy_savings_cost(
        data,
        average_belpex_price_per_kWh
    )

    payback_time = installation_cost_after_energy_difference / cost_of_consumed_energy

    # BONUS
    # Compute how many solar panels in Wp will give you the shortest payback
    # time assuming that the cost per Wp of the installation stays the same.
    optimal_solution = number_of_solar_panels_with_shortest_payback_time(data, average_belpex_price_per_kWh)
    
    return {
        'payback_time_in_years': payback_time,
        'optimal_solution': optimal_solution
    }
