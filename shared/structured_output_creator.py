from pydantic import BaseModel

class FormatWithAdjective(BaseModel):
    summary: str
    adjective: str

class AllClasses(BaseModel):
    metals: FormatWithAdjective
    chemicals: FormatWithAdjective
    materials_origin: FormatWithAdjective
    transportation: FormatWithAdjective
    production: FormatWithAdjective
    planned_obsolescence: FormatWithAdjective
    recycling: FormatWithAdjective