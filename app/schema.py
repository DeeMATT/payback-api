from pydantic import BaseModel, Field

class PaybackSchema(BaseModel):
    annual_energy_consumption: int = Field(..., description="The annual energy consumption in kWh")
    installation_cost: int = Field(..., description="The cost of the solar panel installation")
    installation_wp: int = Field(..., description="The watt peak of the installed solar panel")
