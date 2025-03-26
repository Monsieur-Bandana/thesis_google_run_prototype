from pydantic import BaseModel

class InterpreterStructure(BaseModel):
    quality_of_battery: str
    durability: str
    planned_obsolescence: str
    ease_of_reparation: str
    ease_of_modification: str
    origin: str
    transportation: str
    manufactoring: str
    recycled_parts: str
    innovativity: str
    co_footprint: str