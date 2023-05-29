
from pandas import ExcelFile
import pandas as pd

from .schema import PaybackSchema


def compute_annual_energy_rate(profile_curves: list, time_interval: int = 15) -> int:
    """
    Computes the Annual Energy Rate.

    Args:
        profile_curves: List or array representing the consumption or production profile curve
        time_interval: Time interval in minutes between each data point on the curve

    Returns:
        The annual energy rate.
    """

    # Number of quarters in a year (4 quarters per hour * 24 hours * 365 days)
    num_quarters_per_year = 4 * 24 * 365

    # Energy rate per quarter of an hour
    energy_per_quarter = [item * (time_interval / 60) for item in profile_curves]

    # Total annual energy rate
    annual_energy_rate = sum(energy_per_quarter) * num_quarters_per_year

    return annual_energy_rate


def retrieve_data_set(excel_file: ExcelFile, column: list, skiprows: list = []) -> list[int]:
    """
    read excel spreadsheet, extract and covert data to a list

    Args:
        excel_file: Excel spreadsheet containing sample data
        column: data column to be selected
        skiprows: data rows to be skipped

    Returns:
        List of data series from selected column.
    """
    dataframe = pd.read_excel(excel_file, usecols=column, skiprows=skiprows)
    data_series = dataframe[column[0]].to_list()
    return data_series


def energy_savings_cost(data: PaybackSchema, electricity_price: float) -> float:
    """
    Computes the Energy Savings Cost. Add or Subtract the cost of energy difference between produced and consumed energy
    to solar panel installation cost

    Args:
        data: data object containing annual consumed energy, installation cost and watt peak
        electricity_price: Average Belpex Price for Electricity per kWh

    Returns:
        The solar panel installation cost after energy different.
    """
    annual_energy_consumption = data.annual_energy_consumption
    installation_cost = data.installation_cost
    solar_installed_wp = data.installation_wp

    # convert produced energy to kWh
    energy_production = (solar_installed_wp * 365 * 24) / 1000  # Assuming solar panels produce their peak power for the entire year

    if energy_production < annual_energy_consumption:
        # purchase electricity from the grid
        energy_difference = annual_energy_consumption - energy_production
        purchase_cost = energy_difference * electricity_price
        purchase_cost += purchase_cost * 0.20
        grid_fees = energy_difference * 0.12
        purchase_cost += grid_fees

        # add the additional cost from cost of solar panel installation 
        installation_cost += purchase_cost

    elif energy_production > annual_energy_consumption:
        # inject electricity to the grid and get paid
        energy_difference = energy_production - annual_energy_consumption
        amount_sold = energy_difference * (electricity_price * 0.80)

        # deduct the earned amount from cost of solar panel installation 
        installation_cost -= amount_sold

    return installation_cost


def number_of_solar_panels_with_shortest_payback_time(data: PaybackSchema, electricity_price):
    """
    Computes the optimal solution with Number of Solar Panel in watt peak and the shortest payback time based on customer data

    Args:
        data: data object containing annual consumed energy, installation cost and watt peak
        electricity_price: Average Belpex Price for Electricity per kWh

    Returns:
        The shortest_payback_time and solar_panels_in_Wp
    """

    annual_energy_consumption = data.annual_energy_consumption
    installation_cost = data.installation_cost
    installation_wp = data.installation_wp

    cost_per_watt_peak = installation_cost / installation_wp
    cost_of_consumed_energy = annual_energy_consumption * electricity_price

    shortest_payback_time = float('inf')
    optimal_watt_peak = 0
    
    for watt_peak in range(1000, 20001, 1000):  # Calculate for different watt peaks from 1000 Wp to 10000 Wp
        total_installation_cost_per_Wp = watt_peak * cost_per_watt_peak
        data.installation_cost = total_installation_cost_per_Wp
        data.installation_wp = watt_peak

        installation_cost_with_energy_savings = energy_savings_cost(
            data,
            electricity_price,
        )

        payback_time = installation_cost_with_energy_savings / cost_of_consumed_energy

        if payback_time < shortest_payback_time:
            shortest_payback_time = payback_time
            optimal_watt_peak = watt_peak
    
    return {
        'shortest_payback_time': shortest_payback_time,
        'solar_panels_in_Wp': optimal_watt_peak
    }
