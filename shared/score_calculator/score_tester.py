from shared.score_calculator.score_analyzer import generate_score

### Materials Section
## test fairphone
resp_str = """
The Fairphone 5 employs ethically-sourced metals like cobalt, lithium, and recycled aluminum, promoting sustainable use and responsible extraction practices. It includes Fairtrade gold and focuses on transparency in sourcing.
In a similar vein, the smartphone successfully eliminates toxic chemicals such as beryllium, brominated flame retardants, PVC, phthalates, arsenic, and mercury, significantly enhancing product safety and minimizing environmental impact.
Correspondingly, the smartphone utilizes over 70% fair or recycled materials, including bio-based plastics and recycled metals, significantly reducing environmental impact. By sourcing materials ethically and integrating recycled components, the phone promotes sustainability and responsible manufacturing.
Additionally, the device sources materials like cobalt from artisanal mines in the DRC, and lithium from IRMA-assessed sites in Chile, emphasizing ethical practices and community support. This sourcing approach enhances sustainability and social responsibility.
"""

## test samsung
resp_str1 = """
The Galaxy S24 Ultra incorporates various critical metals, including gold, lithium, cobalt, tantalum, tungsten, and tin, essential for its electronic components. The extraction and processing of these metals contribute significantly to its environmental impact.
In continuation, it contains toxic chemicals such as beryllium, brominated flame retardants, PVC, phthalates, arsenic, and mercury, which pose significant environmental and health risks during production and disposal.
Samsung's Galaxy S24 Ultra employs eco-friendly materials like bio-based plastics and recycled elements from e-waste. This approach minimizes reliance on rare earths and toxic chemicals, positively impacting sustainability.
The raw materials for the Galaxy S24 Ultra, particularly rare earth metals, are sourced from mines predominantly in China, Australia, and Brazil, often raising ethical and environmental concerns related to extraction practices.
"""

## test iphone
resp_str2 = """
The iPhone 16 incorporates various metals, primarily sourced from recycled materials, including aluminum, cobalt, and tungsten. This responsible sourcing significantly reduces its environmental footprint, making the device sustainable and eco-friendly.
Additionally, the device is designed to minimize toxic chemicals but still includes some hazardous materials such as beryllium, PVC, and historically, mercury. It emphasizes reducing these substances through careful material selection.
Not only that, but it incorporates 100% recycled aluminum, cobalt, lithium, and gold in its construction, aiming to reduce reliance on toxic materials and promote sustainability.
Another noteworthy point is that the phone sources its raw materials globally, emphasizing ethical and sustainable practices. Key materials like rare earth elements are predominantly mined in regions like China, Australia, and the U.S., raising ethical concerns and environmental impact.
"""

## test huawei
resp_str3 = """
The Redmi 14C incorporates various metals like tungsten, tin, gold, cobalt, lithium, tantalum, and recycled aluminum, essential for its components. The sourcing and processing of these metals significantly contribute to environmental concerns, especially regarding sustainability and ethical implications.
As an additional point, the smartphone includes various toxic chemicals such as beryllium, brominated flame retardants, PVC, phthalates, arsenic, and mercury, raising significant environmental and health concerns during production and disposal.
Moreover, the device utilizes bio-based plastics from apple pomace and recycled materials, like ocean debris, in its manufacturing. This approach reduces reliance on rare earth materials and toxic chemicals, supporting sustainability in smartphone production.
On top of that, the device sources its raw materials, especially rare earth elements, from mining operations predominantly in China, the USA, and Australia, highlighting significant environmental concerns related to sustainable extraction methods.
"""

test_list = [resp_str, resp_str1, resp_str2, resp_str3]
phone_names = ["fairphone", "samsung", "iphone", "redmi"]
inc_c = 0
for t_ in test_list:
    el_ex: list[dict] = [{"html_output": t_}]
    answ:dict = generate_score(el_ex, "materials")
    
    print(phone_names[inc_c]+ ": " +str(answ["score"]))
    inc_c = inc_c + 1