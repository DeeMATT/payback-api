from pydantic import BaseModel, Field

class PaybackSchema(BaseModel):
    annual_energy_consumption: int = Field(..., description="The annual energy consumption in kWh")
    installation_cost: int = Field(..., description="The cost of the solar panel installation")
    installation_wp: int = Field(..., description="The watt peak of the installed solar panel")


class OptimalSolutionData(BaseModel):
    shortest_payback_time: float
    solar_panels_in_Wp: int


class PaybackResponse(BaseModel):
    payback_time_in_years: float
    optimal_solution: OptimalSolutionData
