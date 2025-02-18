from pydantic import BaseModel

class BatteryQuality(BaseModel):
    quality_of_battery: str
class Longevity(BaseModel):
    durability: str
    planned_obsolescence: str
class RepairabilityAndModifiability(BaseModel):
    ease_of_reparation: str
    ease_of_modification: str
class Production(BaseModel):
    origin: str
    transportation: str
    manufactoring: str
class RecycledParts(BaseModel):
    recycled_parts: str
class SustainableInnovativity(BaseModel):
    innovativity: str


class InterpreterStructure(BaseModel):
    quality_of_battery: BatteryQuality
    longevity: Longevity
    repairability_and_modifiability: RepairabilityAndModifiability
    production: Production
    recycled_parts: RecycledParts
    innovativity: SustainableInnovativity