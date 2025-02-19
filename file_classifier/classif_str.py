from pydantic import BaseModel

class RelatabilityByFloat(BaseModel):
    probability: float
    reason: str



class InterpreterFormatOnDominance(BaseModel):
    quality_of_battery: RelatabilityByFloat
    durability: RelatabilityByFloat
    planned_obsolescence: RelatabilityByFloat
    ease_of_reparation: RelatabilityByFloat
    ease_of_modification: RelatabilityByFloat
    origin: RelatabilityByFloat
    transportation: RelatabilityByFloat
    manufactoring: RelatabilityByFloat
    recycled_parts: RelatabilityByFloat
    innovativity: RelatabilityByFloat
    co_footprint: RelatabilityByFloat