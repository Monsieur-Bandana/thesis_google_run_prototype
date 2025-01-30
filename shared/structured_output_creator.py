from pydantic import BaseModel

class FormatWithAdjective(BaseModel):
    summary: str
    adjective: str

class Materials(BaseModel):
    metals: FormatWithAdjective
    chemicals: FormatWithAdjective
    origin: FormatWithAdjective
class Transportation(BaseModel):
    transportation: FormatWithAdjective
class Production(BaseModel):
    production_process: FormatWithAdjective
    production_waste: FormatWithAdjective
    supplier_energy_use: FormatWithAdjective
    location_of_assembly: FormatWithAdjective
class Use(BaseModel):
    ease_of_reparation: FormatWithAdjective
    ease_of_modification: FormatWithAdjective
    top_notch_technology: FormatWithAdjective
    quality_of_battery: FormatWithAdjective
    durability: FormatWithAdjective
    energy_consumption: FormatWithAdjective
class EndOfLife(BaseModel):
    planned_obsolescence: FormatWithAdjective
    second_use: FormatWithAdjective
    recycling: FormatWithAdjective

class InterpreterFormatWithAdjectiveucture(BaseModel):
    materials: Materials
    transportation: Transportation
    production: Production
    use: Use
    end_of_life: EndOfLife