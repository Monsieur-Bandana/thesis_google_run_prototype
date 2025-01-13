from pydantic import BaseModel

class Materials(BaseModel):
    metals: str
    chemicals: str
    alternatives: str
    origin: str
class Transportation(BaseModel):
    transportation: str
class Production(BaseModel):
    production_process: str
    production_waste: str
    supplier_energy_use: str
    location_of_assembly: str
class Use(BaseModel):
    ease_of_reparation: str
    ease_of_modification: str
    top_notch_technology: str
    quality_of_battery: str
    durability: str
    energy_consumption: str
class EndOfLife(BaseModel):
    planned_obsolescence: str
    second_use: str
    recycling: str

class_list: list = [Materials, Transportation, Production, Use, EndOfLife]

class InterpreterStructure(BaseModel):
    materials: Materials
    transportation: Transportation
    production: Production
    use: Use
    end_of_life: EndOfLife