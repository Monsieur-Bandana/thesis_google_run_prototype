from openai import OpenAI
# from ind_key import key

def accessScientificInformation() -> str:
    return f"""Key Emission Sources in the Smartphone Lifecycle
Material Extraction and Manufacturing: These stages are the highest contributors to CO2 emissions, largely due to the energy-intensive processes of mining and refining materials, like cobalt, copper, gold, and silver. The printed wiring board (PWB), integrated circuits (ICs), and display assembly collectively contribute 75% of material-related emissions.

Assembly, Distribution, and Usage:

Assembly: Emissions during the assembly phase account for around 16% of the total CF, with high energy use during manufacturing.
Distribution: Emissions occur primarily due to global transportation (e.g., air freight from production sites).
Usage: Recharging and, notably, the energy required for mobile communication services significantly increase emissions. The latter, which includes network and data center operations, can double or even triple the CF, especially with increased data usage (e.g., streaming).
End-of-Life (EoL) Scenarios: While recycling reduces emissions by enabling the recovery of valuable materials, only a partial recovery is economically viable, limiting its overall impact.

Strategies for Reducing Carbon Emissions
Extending Product Lifespan:

Longer Replacement Cycles: Extending the replacement cycle from two years to three or four significantly reduces the CF by 30-44%, as fewer units are required over a given period.
Repair and Refurbishment: Repairing components, such as batteries and displays, can extend device life without the need for new manufacturing. Battery replacement, for instance, allows a three-year replacement cycle, reducing emissions by approximately 30%.
Use of Secondary Markets:

Remanufactured and Second-Hand Devices: Replacing new purchases with remanufactured or second-hand phones can cut the CF by up to 80% under optimal conditions. The CF reduction varies depending on whether the phone is fully refurbished (about 50%) or lightly refurbished.
Lean and Durable Design:

Material Efficiency: Designs that reduce material quantities by up to 30% can lower emissions by 7%. However, trade-offs are necessary, as durable designs may make repairs more challenging.
Modular Design: Facilitates easy disassembly and repair, helping prolong device life. Enhanced durability for components most prone to damage, like displays and batteries, also aids in reducing emissions over time.
End-of-Life Recycling:

Efficient Recycling Processes: Improved recycling of metals and critical components could cut emissions further by up to 30%. However, actual benefits depend on effective collection and recycling rates, which are currently low."""

# Eingabetext
def generateAnswer(input: str)  -> str:
    
    
    context = accessScientificInformation()
    comment = f"""please tell me about the carbon footprint of the {input}"""

    context = f"""You are a helpful assistant, returning a structered text abot the carbon footprint of smartphones use the following input: {accessScientificInformation()}."""
    sk = ""
    client = OpenAI(api_key=sk)
    
    client.api_key = sk
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": comment
            }
        ]
    )
    
    generated_text = completion.choices[0].message.content
    html_output = ''.join(f'<p>{line}</p>' for line in generated_text.split('\n') if line.strip())
   

    print(generated_text)

    return html_output
