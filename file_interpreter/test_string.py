test_string = """DOI: 10.1111/jiec.13119
RESEARCH AND ANALYSIS
Reducing the carbon footprint of ICT products through
material efficiency strategies
A life cycle analysis of smartphones
Mauro Cordella1,2Felice Alfieri1Javier Sanfelix3
1European Commission, Joint Research
Centre, Seville, Spain
2TECNALIA, Basque Research and Technology
Alliance (BRTA), Derio, Spain
3European Commission, Directorate General
for Research and Innovation, Brussels, Belgium
Correspondence
Mauro Cordella, TECNALIA, Basque Research
and Technology Alliance (BRTA), Astondo
Bidea, Edificio 700, 48160 Derio, Spain.
Email: mauro.cordella@tecnalia.com
Editor Managing Review: Niko Heeren.
Funding information
European Commission, Grant/Award
Number: Administrative Agree-
ment N. 070201/2015/SI2.719458 (signed
between DG ENV and DG JRC)Abstract
With the support of a life cycle assessment model, this study estimates the carbon foot-
print (CF) of smartphones and life cycle costs (LCC) for consumers in scenarios where
different material efficiency strategies are implemented in Europe. Results show that
a major contribution to the CF of smartphones is due to extraction and processing of
materials and following manufacturing of parts: 10.7 kg CO2,eq/year, when assuming a
biennial replacement cycle. Printed wiring board, display assembly, and integrated cir-
cuits make 75% of the impacts from materials. The CF is increased by assembly ( +2.7 kg
CO2,eq/year), distribution ( +1.9 kg CO2,eq/year), and recharging of the device ( +1.9 kg
CO2,eq/year) and decreased by the end of life recycling ( −0.8 kg CO2,eq/year). However,
the CF of smartphones can dramatically increase when the energy consumed in com-
munication services is counted ( +26.4 kg CO2,eq/year). LCC can vary significantly (235–
622 EUR/year). The service contract can in particular be a decisive cost factor (up to
61–85% of the LCC). It was calculated that the 1:1 displacement of new smartphones
by used devices could decrease the CF by 52–79% (excluding communication services)
and the LCC by 5–16%. An extension of the replacement cycle from 2 to 3 years could
decrease the CF by 23–30% and the LCC by 4–10%, depending on whether repair oper-
ations are required. Measures for implementing such material efficiency strategies are
presented and results can help inform decision-makers about how to reduce impacts
associated with smartphones.
KEYWORDS
climate change, industrial ecology, life cycle assessment (LCA), life cycle costs (LCC), material
efficiency, smartphone
1 INTRODUCTION
Although the climate change threat due to anthropogenic emissions of greenhouse gases (GHG) was raised by the scientific community 30 years
ago (IPCC, 1992 ), it has been only partially reflected in effective interventions under the frameworks of the Kyoto Protocol (United Nations, 1997 )
and the Paris Agreement (United Nations, 2015 ).
This is an open access article under the terms of the Creative Commons Attribution License, which permits use, distribution and reproduction in any medium, provided
the original work is properly cited.
© 2021 European Commission, Joint Research Centre (JRC-Seville). Journal of Industrial Ecology published by Wiley Periodicals LLC on behalf of Yale University
448 wileyonlinelibrary.com/journal/jiec Journal of Industrial Ecology 2021;25:448–464.
CORDELLA ET AL . 449
FIGURE 1 Material efficiency aspects in the life cycle of a product (Cordella et al., 2020a )
The European Commission has reinforced its commitment to tackle environmental challenges through the “European Green Deal” (European
Commission, 2019a ), which includes measures on energy efficiency and circular economy performance of the information and communication tech-
nologies (ICT) sector.
The contribution of the ICT sector to the global GHG emissions was about 1.4% in 2007 and could exceed 14% in 2040. In particular, the contri-
bution from smartphones is increasing so rapidly that it could soon become greater than desktops, laptops, and displays. The main reasons for this
growth are the high market penetration of smartphones and their short replacement cycles (2 years on average) (Belkhir & Elmeligi, 2018 ).
In the European Union (EU), ICT products fall within the scope of Ecodesign Directive (European Union, 2009 ) and Energy Label Regulation
(European Union, 2017 ). These set out a regulatory framework for improving the energy efficiency of energy-related products (European Commis-
sion, 2016 ), with a current shift toward the more systematic consideration of material efficiency aspects (European Commission, 2019b ). Material
efficiency could be defined as the ratio between the performance of a system and the input of materials required (Cordella et al., 2020a ). As shown
in Figure 1, material efficiency can be improved along the life cycle of products by strategies that aim to minimize material consumption, waste
production, and their environmental impacts (Allwood et al., 2011 ; Huysman et al., 2015 ). In practice, this could be achieved by designing products
that are more durable and easier to repair, reuse, or recycle (European Commission, 2015 ).
The relevance of material efficiency strategies for mitigating climate change impacts depends on the relative impacts associated with each life
cycle stage of a product (Iraldo et al., 2017 ; Sanfelix et al., 2019 ; Tecchio et al., 2016 ), which can be quantified through life cycle assessment (LCA)
(ISO, 2006a ;I S O , 2006b ).
The analysis of LCA studies can provide indications about the environmental impacts of smartphones (Cordella & Hidalgo, 2016 ). For exam-
ple, Andrae ( 2016 ), Ercan et al. ( 2016 ), and Clément et al. ( 2020 ) analyzed the Bill of Materials (BoM) of specific devices and their life cycle GHG
 15309290, 2021, 2, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jiec.13119 by Universitsbibliothek, Wiley Online Library on [12/10/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
450 CORDELLA ET AL .
emissions (hereafter referred to as carbon footprint, CF). Manhart et al. ( 2016 ) analyzed resource efficiency aspects in the ICT sector, reporting the
CF of different devices. CF results are also shared by some manufacturers (e.g., Apple ( 2019 ); Huawei ( 2019 )).
In terms of scenarios of use, Ercan et al. ( 2016 ) analyzed the effects of different use intensities of smartphones. An assessment of CF mitigation
effects of remanufacturing, reuse, and recycling is provided in Andrae ( 2016 ), while repair and refurbishment scenarios were assessed by Proske
et al. ( 2016 ). A comparative assessment of end of life (EoL) repurposing (vs. refurbishment) was carried out by Zink et al. ( 2014 ) . Furthermore,
Suckling and Lee ( 2015 ) provided a comparison of the CF associated with the EoL collection of old phones for reuse, remanufacturing, and recycling.
Economic considerations for EoL scenarios can also be found in the literature (Clift & Wright, 2000 ; Geyer & Doctori Blass, 2010 ; Gurita et al.,
2018 ). Furthermore, recent studies go beyond attributional LCA approaches by discussing rebound effects that could happen at macro-scale (Makov
& Font Vivanco, 2018 ; Makov et al., 2018 ;Z i n k&G e y e r , 2017 ; Zink et al., 2014 ).
This study aims to build upon the existing LCA literature for smartphones and expand it by providing a broad and critical analysis of material effi-
ciency strategies and their effect on CF and life cycle costs (LCC) for consumers. Measures are also identified to assist decision-makers in mitigati ng
impacts of smartphones in a cost-effective way.
2 MATERIALS AND METHODS
2.1 Life cycle analysis of material efficiency strategies for smartphones
An attributional LCA was carried out for the analysis of material efficiency strategies. The aim was not to compare specific devices but to produce
general considerations for the EU. A number of scenarios were assessed that involve different technological and behavioral practices:
I. Baseline scenario (purchase, use and disposal of new smartphones);
II. Extended use scenarios with/without repair operations;
III. Scenarios involving the purchase of remanufactured or second-hand devices (both referred to also as “used devices” in this paper)1;
IV. Scenarios involving lean design concepts.
Table 1and the following sections provide an overview of analyzed scenarios and modeling assumptions.
2.1.1 Reference indicators
T h eC F ,e x p r e s s e da sC O 2,eq, was calculated based on the 100-year global warming potentials (GWP) of GHG emissions (IPCC, 2013 ). Although GWP
correlates to a number of environmental indicators (Askham et al., 2012 ; Huijbregts et al., 2006 ), a broader metric (covering impact categories such
as resource scarcity, biodiversity, and toxicity) would allow for a more comprehensive sustainability assessment (Moberg et al., 2014 ). Additional
environmental considerations are addressed qualitatively while discussing results. It is anticipated that the use of broader metric for the assess ment
of smartphones (Ercan et al., 2016 ; Moberg et al., 2014 ; Proske et al., 2016 ) confirmed the importance played by manufacturing processes and
extraction of materials (e.g., cobalt, copper, gold, silver, Praseodymium).
The quantitative assessment also included economic considerations about the LCC for consumers (COWI & VHK, 2011 ), expressed as EUR 2019
and calculated according to Equation ( 1). The formula was obtained by considering the present value factor equal to 1 (Boyano Larriba et al., 2017 ).
LCC=PP+N∑
1OE+MRC+ELC, (1)
where:
∙LCC: life cycle costs for end users;
∙PP: purchase price;
∙OE: annual operating expenses for each year of use;
∙N: reference time in years;
∙MRC: maintenance and repair costs (when applicable);
∙ELC: end of life costs/benefits.
1Definitions used for lifetime extension processes (value-retention processes) vary widely (IRP, 2018 ). In this work, remanufacturing and refurbishment are used interchangeably to indicate the
“modification of an object that is a waste or a product to increase or restore its performance and/or functionality or to meet applicable technical sta ndards or regulatory requirements, with the
result of making a fully functional product to be used for a purpose that is at least the one that was originally intended.” However, while remanufactur ing is typically used for an industrial process to
make “as-new” products that carry a legal warranty, refurbishment requires operations that exceed repair but are less structured, industrialized a nd quality focused than remanufacturing (e.g., data
wiping and upgrade, repair for functionality, aesthetic touch-ups). Refurbishment is defined as “comprehensive” when happening within industria l or factory settings (IRP, 2018 ).
 15309290, 2021, 2, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jiec.13119 by Universitsbibliothek, Wiley Online Library on [12/10/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
CORDELLA ET AL . 451
TABLE 1 Scenarios considered for the assessment of material efficiency aspects in the life cycle of smartphones
Scenario Key assumptions for the CF assessment Additional consideration for the LCC assessment
Baseline (BL) Replacement cycle : smartphones are replaced with a new
device (the same model) every 2 years; new devices are
bought and allocated to cover the reference lifetime (i.e.,
2.25 units for a period of 4.5 years).
EOL: the old product is kept unused at home.
Other system aspects : impact associated to data consumption
during the use phase are not considered. For sensitivity
analysis, BL +also consider:
- Impact associated to the usage of communication networks
during the use-phase;
- End-of-Life recycling with pre-treatment for battery
recovery.Costs associated to the mobile contract service are included.
For sensitivity analysis, the following scenarios are
considered:
- BL, where an average product is considered;
- BL-HE, where a high-end product is considered;
- BL-LE, where a low-end product is considered.
Extended use (EXT) Replacement cycle : compared to BL, replacement cycle
increased to 3 (EXT1) and 4 years (EXT2), which results in
the need of less devices along the reference lifetime (i.e.,
1.5 and 1.125 units, respectively).
Other assumptions: as BL .The following scenarios are considered:
- EXT1 and EXT2: as BL, with replacement cycle increased to 3
and 4 years, respectively;
- EXT1-HE and EXT2-HE: as BL-HE, with replacement cycle
increased to 3 and 4 years, respectively.
Battery change (BC) Replacement cycle : compared to EXT1 and EXT2, replacement
cycle is the same (i.e., 3 years for BC1 and 4 years for BC2)
with the change of the battery.
Other assumptions : as EXT1 and EXT2.The following scenarios are considered:
- BC1a: as EXT1, with change of the battery made by the user;
- BC1b: as EXT1, with change of the battery made by a
professional repairer;
- BC2: as EXT2, with change of the battery made by the user.
Display change (DC) Replacement cycle : compared to EXT1 and EXT2, replacement
cycle is the same (i.e., 3 years for DC1 and 4 years for DC2)
with the repair (change) of the display.
Other assumptions : as EXT1 and EXT2.The following scenarios are considered:
- DC1a: as EXT1, with repair of the display by the user;
- DC1b: as EXT1, with repair of the display by a professional
repairer;
- DC2: as EXT2, with repair of the display by the user.
Battery change +
display change
(BC-DC)Replacement cycle : compared to EXT1 and EXT2, replacement
cycle is the same (i.e., 3 years for BC-DC1 and 4 years for
BC-DC2) with battery change and the repair (change) of
the display.
Other assumptions : as EXT1 and EXT2.Not assessed directly.
Remanufacture (RM) Replacement cycle : remanufactured smartphones bought by
users every 2 years, to cover the reference lifetime (i.e.,
2.25 units for a period of 4.5 years).
Remanufactured device impacts : due to battery change, display
change, energy for manufacturing and transport.
EOL: the old product is kept unused at home .As BL, with purchase price of the product calculated as the
cost of battery change and display repair.
Reuse (RU) Replacement cycle : reused smartphones bought by users
every 2 years, to cover the reference lifetime (i.e., 2.25
units for a period of 4.5 years).
Reused device impacts : due to battery change, display change,
and transport.
EOL: the old product is kept unused at home.As BL, with purchase price of the product calculated as one
third of the original price and a margin of 40%.
Lean design (LD) Device manufacturing impacts : reduction of materials used for
housing:−10% by weight (LD1), −20% by weight (LD2),
−30% by weight (LD3).
Other assumptions :a sB L .Not assessed directly.
2.1.2 Functional unit and reference flow
Smartphones are multi-functional devices that provide different types and levels of performance. The assessment of specific devices should refer
to a functional unit (FU) that covers both quantitative and qualitative aspects (ETSI, 2019 ), and only products with similar characteristics should be
compared, which is beyond the scope of this study.
The FU considered in this study is the use of smartphones by a European consumer during a reference time of 4.5 years. This was chosen, based
on data from Prakash et al. ( 2015 ), as a proxy for the potential time during which smartphones can be used. This is comparable with average lifespan
 15309290, 2021, 2, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jiec.13119 by Universitsbibliothek, Wiley Online Library on [12/10/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
452 CORDELLA ET AL .
data for mobile phones reported by Bakker et al. ( 2014 ) (4.5 years in 2005, Dutch data) and Makov et al. ( 2018 ) (4.5 and 5.6 years for two brands in
2015–2016, US data), which cover the first use cycle and possible subsequent use cycles of the product before the EoL disposal by the final owner.
The reference flow is the number of smartphone devices purchased, used, and disposed by the consumer during this period. The reference
flow is determined by the replacement cycle of smartphones (see Section 2.2.2 ): for a replacement cycle of Xyears, the reference flow is equal to
4.5 divided by X.
2.1.3 Assessed scenarios and system boundaries
The scenarios assessed in this study are reported in Table 1. For each scenario, the system boundaries cover the cradle-to-grave analysis of a generic,
virtual product.
As a baseline (BL), the following stages are considered:
1. Production of parts (extraction, processing and transportation of materials, manufacturing of parts);
2. Smartphone manufacturing (transportation of parts, device assembly);
3. Distribution and purchase (transportation of smartphones to points of sale);
4. Use (energy for battery recharging);
5. EoL replacement (old unused device being kept at home).
Additional scenarios integrate the following aspects: system impacts associated with communication services and EoL recycling (BL +), extended
use (EXT), battery change (BC), repair and change of the display (DC), remanufacture (RM), reuse (RU), lean design (LD). Services and material goods
necessary to support the business (e.g., research and development, marketing) are excluded from the assessment.
2.2 Carbon footprint modeling
LCA studies published from 2014 onward were screened to identify relevant sources of data for the analysis (Cordella & Hidalgo, 2016 ). The CF was
calculated based on such information and life cycle inventory (LCI) datasets (cut-off system models) from Ecoinvent 3.5 (Wernet et al., 2016 ), with
proxies used in the presence of data gaps. Assumptions made to handle existing data limitations were discussed with experts in the sector (Cordella
et al., 2020b ), and results compared with those of other studies (see Table 2). The GHG emission factors used for the assessment are provided in
Supporting Information S1.
2.2.1 Production of parts and manufacturing of the device
An average smartphone was considered to have a display size of 75.53 cm2and a weight of about 160 g, including 39 g for the battery and excluding
accessories and packaging (Manhart et al., 2016 ). Additional materials are necessary for packaging (cardboard and plastic materials), documenta-
tion, and accessories such as head set, USB cable, charger. The BoM of the virtual product is reported in Supporting Information S1.
Scenarios RM and RU, which involve the purchase of remanufactured or second-hand devices, include a change of battery and display. The weight
of materials used for the housing and display of smartphones were proportionally decreased in the LD scenarios, without investigating how this can
affect other geometrical design characteristics (e.g., display size).
The assembly of one unit of smartphones was considered to happen in China and require 4.698 kWh (Proske et al., 2016 ). The same energy
consumption value (worst-case assumption) was considered for the remanufacturing of the device in industrial settings. However, when fewer
refurbishment operations are needed (e.g., clean-up and software update), the energy intensity of the remanufacturing process could be lower, for
example, 0.033 kWh per device (Skerlos et al., 2003 ). Section 3.1.4 shows a sensitivity analysis on this parameter, which provides an uncertainty
range for RM.
Regarding the transport of parts to the assembling factory, it was considered that housing and packaging materials are transported by lorry for
1000 km and 100 km, respectively, while other components (mostly electronics) are transported for 1000 km by flight and 100 km by lorry. Such
assumptions aimed to reflect the geographical availability of parts and materials and the ease/difficulty of procuring them.
2.2.2 Distribution and use
The following means of transport were considered for the distribution of smartphones: 8000 km by flight (distance between Beijing and Brussels)
and 600 km by heavy truck (transport distance proxy within Europe).
 15309290, 2021, 2, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jiec.13119 by Universitsbibliothek, Wiley Online Library on [12/10/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
CORDELLA ET AL . 453
TABLE 2 Carbon footprints and key parameters from LCA studies on smartphones
Parametera)BL (this study)Andrae
(2016 )Ercan et al.
(2016 )Proske et al.
(2016 ) Apple ( 2019 )f)Huawei ( 2019 )g)
CF, over the reference lifetime (kg CO 2,eq)b)77.2 39.2 56.7 43.9 45.0 −79.0
(average: 61.2)50.0−84.5
(average: 61.9)
CF contribution due to EOL recycling
(kg CO 2,eq)c)Not considered 0.4 −0.3 −1.0 ∼0.2 ∼0.1
Reference lifetime (years) 4.5 2 3 3 3 2
Replacement cycle (years) 2 2 3 3 3 2
Reference flow (smartphone units) 2.25 1 1 1 1 1
Weight of one device (g)d)160 223 152 168 112−208
(average: 159)142−232
(average: 163)
CF contribution due to the manufacturing of
one device (kg CO 2,eq)e)26.7 38.3 49.8 36.0 24.8–63.2
(average: 45.3)41.0–70.4
(average: 51.4)
CF, adjusted to BL conditions for this study
(kg CO 2,eq)
- Over 4.5 years 77.2 87 123 97 66.8−117.3
(average: 90.9)112.3−189.8
(average: 139.0)
- Normalized to 1 year of use 17.2 19.4 27.3 21.5 14.9−26.1
(average: 20.2)25.0−42.2
(average: 30.9)
- Normalized to BL 100% 113% 159% 125% 86−152%
(average: 117%)146−246%
(average: 180%)
Notes:
a)A full comparison of results is not possible since they depend on modeling assumptions and datasets used in different studies.
b)Communication services excluded.
c)Positive numbers indicate burdens, negative numbers indicate net savings.
d)Accessories and packaging excluded.
e)Including extraction and processing of raw materials, manufacturing of parts and assembling of the device.
f)Based on the analysis of 15 models (additional information reported in the Supporting Information).
g)Based on the analysis of 32 models (additional information reported in the Supporting Information).
The use of smartphones directly implies electricity consumption for the battery recharging cycles. The duration and frequency of recharg-
ing cycles can vary depending on technical characteristics of devices as well as user behavior (Falaki et al., 2010 ). An electricity consumption of
4.9 kWh/year was calculated by Proske et al. ( 2016 ) considering a battery capacity of 2420 mAh, 3.8 V of voltage, 69% of recharge efficiency, and
365 charge cycle per year. According to Andrae ( 2016 ), energy consumption is 1.538 times the battery capacity and can be 2–6 kWh/year, which is
similar to the 3–6 kWh/year estimated by Manhart et al. ( 2016 ). Ercan et al. ( 2016 ) instead quantified that the annual electricity demand of a smart-
phones can range from 2.58 kWh (1 recharge every 3 days) to 7.74 kWh (1 recharge per day). Based on the available information it was assumed
that the average electricity consumption directly associated with the use of smartphones is 4 kWh/year.
Furthermore, it was considered as BL that smartphones are used for 2 years (Belkhir & Elmeligi, 2018 ; Prakash et al., 2015 ), before being replaced
with new devices. This does not mean that the device performance is necessarily compromised after 2 years. The decision to replace a smartphone
is often based on perceived functional obsolescence when compared to new models on the market (Makov & Fitzpatrick, 2019 ; Watson et al., 2017 ).
The replacement cycle was extended in other scenarios, resulting in the need for fewer device units over the reference time of 4.5 years (see
Section 2.1.2 ), as indicated in Table 1. In some scenarios, this was associated with a repair operation. Replacements of battery and/or display are
analyzed since these parts are frequently impacted by loss of performance, failures, and breakages (OCU, 2018 ,2019 ). Cordella et al. ( 2020b )
estimated that the likelihood of replacing the display or the battery during the lifespan of a smartphone could be up to 24% and 50%, respectively.
These proxies were used to build an average EU scenario (see Section 3.3).
2.2.3 End of life
Based on the literature (Ellen MacArthur Foundation, 2012 ; Ercan, 2013 ; Manhart et al., 2016 ), it was estimated that about 49% of devices are
kept unused at home once they reach their EoL; 36% find a second use (either as donation or through second-hand markets); 15% are collected and
recycled/remanufactured. As BL, it was assumed that devices are kept unused at home.
 15309290, 2021, 2, Downloaded from https://onlinelibrary.wiley.com/doi/10.1111/jiec.13119 by Universitsbibliothek, Wiley Online Library on [12/10/2024]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
454 CORDELLA ET AL .
With respect to recycling, impacts can vary depending on characteristics of product recycling process (Geyer & Doctori Blass, 2010 ), as well as
on assumptions made and data used. For example, Proske et al. ( 2016 ) estimated that the recycling of battery, copper, and other precious materials
from a smartphone of 168 g yields a net saving of 1140 g CO 2,eq(calculated as “burdens from impacts” minus “credits from avoided impacts”).
Andrae ( 2016 ) instead reported that the recycling of a smartphone of about 220 g result in the emission of 400 g of CO 2,eq. A net saving of about
2150 g of CO 2,eqwould result by taking the full recovery of precious metals into account (calculated based on Manhart et al. ( 2016 )a n dA n d r a e
(2016 )). Although technologically feasible, a full recovery of precious metals (e.g., magnesium, tungsten, rare earth elements, tantalum) may not be
economically viable (Manhart et al., 2016 ).
The typical recycling process for smartphones consists of mechanical and manual operations for the separation of materials, including plastics,
and the recovery of batteries, copper, precious metals (gold, silver, platinum), aluminum, and steel (Manhart et al., 2016 ).
To provide an indication of the potential benefits associated with the recycling of smartphones (Cordella et al., 2020b ), the estimate from Proske
et al. ( 2016 ) was rescaled to 160 g (device weight considered in this study), and credits were assigned to the recovery of materials and energy from
the housing (display excluded). It was assumed that:
∙Recycled materials can fully displace primary materials, which is not necessarily the case in real markets (Palazzo et al., 2019 ), as also discussed
in Section 3.1.3 .
∙Aluminum and steel can be completely recycled at the EoL, and their recycling avoids the production of new materials, while emitting 1.01 and
0.85 g of CO 2,eqper gram of aluminum and steel recycled, respectively.
∙Plastics are incinerated, which avoids 0.094 Wh of electricity and produces 1.04 g of CO 2,eqper gram of plastic incinerated.
As a net result, it was estimated that the recycling of a smartphone could lead to the saving of 1640 g of CO 2,eq.
2.2.4 Communication services
Beside battery recharging, energy is also needed for the operation of communication services such as mobile networks, fixed access networks (e.g.,
wi-fi), and core networks (e.g., data center and transmission infrastructures). Ercan et al. ( 2016 ) estimated that the energy used for operating mobile,
wireless, and core networks correspond to 28.7 kWh/year for a light user, 33.3 kWh/year for a representative user, and 49 kWh/year for a heavy
user. According to Andrae ( 2016 ), the electricity consumption for operating networks and data center infrastructures is 1.16 kWh/GB. Considering
an average consumption of 4 GB per month (Transform Together, 2018 ), the annual consumption of electricity would be 55.7 kWh. This figure, which
is close to the heavy user estimation by Ercan et al. ( 2016 ), was considered in this study, also to reflect the trend toward increased data consumption
(Transform Together, 2018 ).
2.3 Life cycle cost modeling
2.3.1 Purchase price for new products and operating costs
A business model in which users are owners of smartphone devices was considered, which is a common scenario in the EU. It was estimated that
the average purchase price for a new smartphone in the EU is 320 EUR. This changes to less than 130 EUR and more than 480 EUR for low- and
high-end products, respectively (Cordella et al., 2020b ).
The LCC effects of lean design concepts or changes in material composition of devices were not assessed. However, almost 70% of the purchase
price of smartphones is independent of parts and materials (Benton et al., 2015 ).
Operating costs include electricity consumption to recharge the battery and mobile service contract. They were considered equal to 0.2113
EUR/kWh (Eurostat, 2019 ), and 31.80 EUR/month (DG Connect, 2018 ) for a service contract including 5 GB of data, 100 calls, and 140 SMS. The
service contract cost decreases to 14.11 EUR for 100 MB, 30 calls, and 100 SMS (as EU average in 2017).
Product–service systems (PSS) appears a less common scenario for smartphones (Poppelaars et al., 2018 ) and were not directly assessed. The
main advantage of PSS business models is the enhanced possibility for service providers of collecting and reprocessing used devices. From a con-
sumer perspective, the LCC considerations provided in Section 3.2can address the discussion of PSS business models. When the acquisition of a
smartphone is associated to a contract subscription with a telecommunication service provider, the product purchase cost is integrated in the sub-
scri"""