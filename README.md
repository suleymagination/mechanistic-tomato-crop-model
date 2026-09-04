# Mechanistic Dwarf Tomato Growth & Resource-Use Model

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data--License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An object-oriented, process-based Python framework for modeling daily dry matter production, carbon allocation, canopy transpiration, and water usage in dwarf tomato (*Solanum lycopersicum*) cultivations. The model is parameterized and validated using empirical experimental data from the **4th International Autonomous Greenhouse Challenge** hosted by Wageningen University & Research (WUR).

---

## Data Provenance & Attribution

The climate time-series, crop growth, and harvest metrics stored in `data/` are derived from open-access experimental datasets published via **4TU.ResearchData**:

* **Dataset Title:** 4th Autonomous Greenhouse Challenge: Dwarf Tomato Timeseries and Images[cite: 1, 2]
* **DOI / Resource Identifier:** [10.4121/fa102772-32db-4b30-bace-12f2016722ce.v1](https://doi.org/10.4121/fa102772-32db-4b30-bace-12f2016722ce.v1)
* **Authors:** Stef Maree, Pinglin Zhang, Bart M. van Marrewijk, Feije de Zwart, Monique Bijlaard, and Silke Hemming
* **Publisher & Host Institution:** 4TU.ResearchData | Greenhouse Horticulture Business Unit, Wageningen University & Research (Bleiswijk, The Netherlands)
* **Data License:** Creative Commons Attribution 4.0 International ([CC BY 4.0](https://creativecommons.org/licenses/by/4.0/))
* **Associated Paper:** Maree, S. C., Zhang, P., van Marrewijk, B. M., de Zwart, F., Bijlaard, M., & Hemming, S. (2025). Autonomous Greenhouse Cultivation of Dwarf Tomato: Performance Evaluation of Intelligent Algorithms for Multiple-Sensor Feedback. *Sensors*, 25(14), 4321. [https://doi.org/10.3390/s25144321](https://doi.org/10.3390/s25144321)
* **Data Processing Pipeline:** See `notebooks/extract_data.ipynb` for the automated raw-to-processed extraction workflow.

---

## Experimental Facility Details

* **Location:** WUR Greenhouse Horticulture Research Station, Bleiswijk, The Netherlands ($52.03203^\circ\text{ N}, 4.530938^\circ\text{ E}$)
* **Trial Duration:** September–November 2024 (2-month cultivation cycle)
* **Setup:** 6 high-tech greenhouse compartments ($96\text{ m}^2$ each) equipped with LED lighting, climate sensor arrays, automated fertigation, and downward-facing RGBD canopy cameras.
