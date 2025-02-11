# This script assigns each journal to a category in the Frascati Manual

# Importing required modules

import pandas as pd

# Read in the data

data = pd.read_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers.csv')

# A dictionary for assigning each journal to a Frascati Manual category

fm = {'Mathematics':1,
'Microorganisms':1,
'Int. J. Mol. Sci.':1,
'Fluids':1,
'Galaxies':1,
'Polymers':2,
'Int. J. Environ. Res. Public Health':3,
'Energies':1,
'Sensors':2,
'Land':5,
'Sustainability':5,
'Diversity':1,
'Entropy':1,
'Quantum Beam Sci.':1,
'Climate':1,
'Cells':1,
'Remote Sens.':2,
'Atmosphere':1,
'Catalysts':1,
'Vet. Sci.':4,
'Agriculture':4,
'Animals':4,
'Forests':1,
'Viruses':1,
'Molecules':1,
'Smart Cities':5,
'Electronics':2,
'J. Clin. Med.':3,
'Water':5,
'Toxins':1,
'Symmetry':1,
'Biomolecules':1,
'Antioxidants':3,
'Stats':1,
'Cancers':3,
'Logistics':2,
'ISPRS Int. J. Geo-Inf.':5,
'Appl. Sci.':2,
'Infrastructures':2,
'Nutrients':3,
'Information':1,
'Diagnostics':3,
'Materials':2,
'Forecasting':1,
'Healthcare':3,
'Foods':4,
'Coatings':2,
'Crystals':1,
'Societies':5,
'Econometrics':5,
'Economies':5,
'Educ. Sci.':5,
'Processes':2,
'Geosciences':1,
'Nanomaterials':2,
'Recycling':5,
'J. Funct. Biomater.':2,
'Risks':5,
'Pharmaceuticals':3,
'Int. J. Financial Stud.':5,
'Fermentation':2,
'Children':3,
'Religions':6,
'Fishes':4,
'J. Mar. Sci. Eng.':2,
'Buildings':2,
'Insects':1,
'Biomedicines':3,
'Pharmaceutics':3,
'Electrochem':2,
'Computers':2,
'Mar. Drugs':3,
'J. Risk Financial Manag.':5,
'Genes':1,
'Plants':1,
'Vaccines':3,
'Metals':2,
'J. Compos. Sci.':2,
'Trop. Med. Infect. Dis.':3,
'Agronomy':4,
'Metabolites':1,
'Psychiatry Int.':3,
'J. Pers. Med.':3,
'Beverages':2,
'Minerals':1,
'Cosmetics':3,
'Algorithms':1,
'Photonics':1,
'Pharmacy':3,
'Vehicles':2,
'Vision':3,
'Condens. Matter':1,
'Proceedings':1,
'Antibiotics':3,
'Brain Sci.':3,
'Axioms':1,
'Biosensors':2,
'Micromachines':2,
'J':5,
'Pathogens':1,
'Sports':3,
'Universe':1,
'Bioengineering':2,
'J. Funct. Morphol. Kinesiol.':3,
'Heritage':6,
'Computation':1,
'Resources':5,
'Informatics':2,
'Earth':1,
'Membranes':2,
'Magnetochemistry':1,
'Aerospace':2,
'Medicina':3,
'Int. J. Neonatal Screen.':3,
'Medicines':3,
'World Electr. Veh. J.':2,
'Biology':1,
'Machines':2,
'Environments':1,
'Soc. Sci.':5,
'Prosthesis':3,
'Clocks &amp; Sleep':3,
'Laws':5,
'Gastrointest. Disord.':3,
'C':1,
'World':5,
'Humanities':6,
'Biomimetics':1,
'Fire':1,
'J. Fungi':1,
'Behav. Sci.':5,
'Systems':5,
'Genealogy':6,
'Multimodal Technologies Interact.':2,
'Arts':6,
'Inorganics':1,
'Geriatrics':3,
'Colloids Interfaces':2,
'Separations':1,
'J. Imaging':2,
'Transplantology':3,
'Atoms':1,
'Antibodies':3,
'Chem. Proc.':1,
'Eng. Proc.':2,
'Mater. Proc.':2,
'Future Internet':2,
'Epigenomes':1,
'Modelling':1,
'Life':1,
'Robotics':2,
'Technologies':2,
'Publications':6,
'Challenges':5,
'Chemosensors':2,
'J. Nucl. Eng.':2,
'J. Sens. Actuator Netw.':2,
'Instruments':2,
'Urban Sci.':5,
'Non-Coding RNA':1,
'Appl. Syst. Innov.':2,
'Math. Comput. Appl.':1,
'Physics':1,
'J. Manuf. Mater. Process.':2,
'Soil Syst.':1,
'Toxics':2,
'Sci':1,
'Osteology':3,
'Drones':2,
'Methods Protoc.':1,
'Fractal Fract':1,
'J. Cardiovasc. Dev. Dis.':3,
'Acoustics':2,
'Horticulturae':4,
'AI':1,
'ChemEngineering':2,
'Fibers':2,
'Batteries':2,
'Lubricants':2,
'Int. J. Turbomach. Propuls. Power':2,
'Diseases':3,
'Dent. J.':3,
'Oceans':1,
'Sci. Pharm.':3,
'Quantum Reports':1,
'Proteomes':1,
'Eur. J. Investig. Health Psychol. Educ.':5,
'Hydrology':1,
'J. Dev. Biol.':1,
'Chemistry':1,
'Reports':3,
'Actuators':2,
'Vibration':2,
'Big Data Cogn. Comput.':2,
'Molbank':1,
'Particles':1,
'Gels':2,
'J. Open Innov. Technol. Mark. Complex.':5,
'AgriEngineering':4,
'J. Intell.':5,
'Mach. Learn. Knowl. Extr.':1,
'Ceramics':2,
'Data':1,
'Adm. Sci.':5,
'Surfaces':1,
'Inventions':2,
'Corros. Mater. Degrad.':2,
'Dairy':4,
'Safety':2,
'civileng':2,
'Quaternary':1,
'Sus. Chem.':2,
'Clean Technol.':2,
'Nitrogen':1,
'Games':5,
'Cryptography':1,
'Med. Sci.':3,
'Languages':6,
'Plasma':1,
'Hearts':3,
'J. Low Power Electron. Appl.':2,
'Bloods':3,
'GeoHazards':1,
'electron. mater.':2,
'Designs':2,
'High-Throughput':1,
'Appl. Mech.':2,
'Signals':2,
'Endocrines':3,
'Electricity':2,
'Reprod. Med.':3,
'Psych':5,
'Optics':1,
'J. Nanotheranostics':3,
'Analytica':1,
'Diabetology':3,
'Philosophies':6,
'Telecom':2,
'Surgeries':3,
'IoT':2,
'Appl. Nano':2,
'Sinusitis':3,
'EJBC':3,
'J. Otorhinolaryngol. Hear. Balance Med.':3,
'Neuroglia':3,
'Sinusitis and Asthma':3,
'Cyber':2,
'Reactions':1,
'Soils':1,
'Microarrays':1,
'Chromatography':1,
'Dermatopathology':3,
'Automation':2,
'Polysaccharides':1,
'Environ Sci Proc':1,
'Macromol':1,
'Constr. Mater.':2,
'NeuroSci':3,
'Ecologies':1,
'Gastroenterol. Insights':3,
'J. Mol. Pathol.':3,
'Stresses':1,
'J. Zool. Bot. Gard.':1,
'Fuels':2,
'Obesities':3,
'Organics':1,
'Pollutants':2,
'Thermo':2,
'Electron. Mater.':2,
'Adolescents':3,
'Allergies':3,
'Multimodal Technol. Interact.':2,
'Eur. Burn J.':3,
'Oral':3,
'J. Respir.':3,
'Quantum Rep.':1,
'Eng':2,
'Journal. Media.':5,
'Women':3,
'Taxonomy':1,
'Fractal Fract.':1,
'Gases':2,
'BioTech':2,
'Hydrogen':2,
'Cardiogenetics':3,
'Clin. Pract.':3,
'Biomechanics':3,
'J. Xenobiot.':1,
'Infect. Dis. Rep.':3,
'Epidemiologia':3,
'Sexes':6,
'Encyclopedia':2,
'Pathophysiology':3,
'Audiol. Res.':3,
'Pediatr. Rep.':3,
'Birds':1,
'Hemato':3,
'Digital':2,
'Neurol. Int.':3,
'J. Theor. Appl. Electron. Commer. Res.':5,
'J. Cybersecur. Priv.':2,
'Tour. Hosp.':5,
'Histories':6,
'Sustain. Chem.':2,
'Microbiol. Res.':1,
'Radiation':3,
'Curr. Oncol.':3,
'Geomatics':2,
'Quantum rep.':1,
'CivilEng':2,
'Nurs. Rep.':3,
'Solids':2}

# Adding Frascati Manual to the data

cats = [fm[j] for j in data.Journal]
cats = pd.Series(cats, name = 'Frascati')
data = pd.concat([data, cats], axis = 1)

# Writing the data to file

data.to_csv('C:/Users/User/Documents/Data/COVID-19/MDPI_papers_with_FM.csv', index = False)

