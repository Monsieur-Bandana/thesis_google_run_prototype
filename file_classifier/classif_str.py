from pydantic import BaseModel

class RelatabilityByFloat(BaseModel):
    probability: float
    reason: str



class InterpreterFormatOnDominance(BaseModel):
    metals: RelatabilityByFloat
    chemicals: RelatabilityByFloat
    origin: RelatabilityByFloat
    transportation: RelatabilityByFloat
    production_process: RelatabilityByFloat
    production_waste: RelatabilityByFloat
    supplier_energy_use: RelatabilityByFloat
    location_of_assembly: RelatabilityByFloat
    ease_of_reparation: RelatabilityByFloat
    ease_of_modification: RelatabilityByFloat
    top_notch_technology: RelatabilityByFloat
    quality_of_battery: RelatabilityByFloat
    durability: RelatabilityByFloat
    energy_consumption: RelatabilityByFloat
    planned_obsolescence: RelatabilityByFloat
    second_use: RelatabilityByFloat
    recycling: RelatabilityByFloat