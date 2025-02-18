from pydantic import BaseModel

class FormatWithAdjective(BaseModel):
    summary: str
    adjective: str

class BatteryQuality(BaseModel):
    quality_of_battery: FormatWithAdjective

class Longevity(BaseModel):
    durability: FormatWithAdjective
    planned_obsolescence: FormatWithAdjective

class RepairabilityAndModifiability(BaseModel):
    ease_of_reparation: FormatWithAdjective
    ease_of_modification: FormatWithAdjective

class Production(BaseModel):
    origin: FormatWithAdjective
    transportation: FormatWithAdjective
    manufactoring: FormatWithAdjective

class RecycledParts(BaseModel):
    recycled_parts: FormatWithAdjective

class SustainableInnovativity(BaseModel):
    innovativity: FormatWithAdjective

class InterpreterFormatWithAdjectiveStructure(BaseModel):
    quality_of_battery: BatteryQuality
    longevity: Longevity
    repairability_and_modifiability: RepairabilityAndModifiability
    production: Production
    recycled_parts: RecycledParts
    innovativity: SustainableInnovativity
