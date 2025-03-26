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


class Co_Footprint(BaseModel):
    co_footprint: FormatWithAdjective


class InterpreterFormatWithAdjectiveStructure(BaseModel):
    quality_of_battery: BatteryQuality
    longevity: Longevity
    repairability_and_modifiability: RepairabilityAndModifiability
    production: Production
    recycled_parts: RecycledParts
    innovativity: SustainableInnovativity
    co_footprint: Co_Footprint


def create_inner_struct(descr, min_token_size):
    return {
        "type": "object",
        "properties": {
            "summary": {
                "type": "string",
                "description": f"""The summary must have a length of **at least {min_token_size} tokens** and maximum of {min_token_size + 10} tokens. Extend the summary by further explanation in order to achieve the requivered length. {descr}""",
            },
            "adjective": {
                "type": "string",
                "description": """one or two adjectives which summarize the description. If it are two add a connection such as `and` or `but` """,
            },
        },
        "required": ["summary", "adjective"],
    }
