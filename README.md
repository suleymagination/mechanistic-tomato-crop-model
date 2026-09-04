# Mechanistic Dwarf Tomato Growth & Resource-Use Model

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Data License: CC BY 4.0](https://img.shields.io/badge/Data--License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/suleymagination/mechanistic-tomato-crop-model/blob/main/notebooks/model_validation.ipynb)

An object-oriented, process-based Python framework for modeling daily dry matter production, carbon allocation, canopy transpiration, and water usage in dwarf tomato (*Solanum lycopersicum*) cultivations. The model is parameterized and validated using empirical experimental data from the **4th International Autonomous Greenhouse Challenge** hosted by Wageningen University & Research (WUR).

---

## Overview & Model Architecture

This repository implements an object-oriented, process-based mechanistic crop simulation model written in Python. It models daily dry matter accumulation, carbon allocation, fruit fresh weight development, canopy transpiration, and water demand for dwarf tomato (*Solanum lycopersicum*) grown under Controlled Environment Agriculture (CEA) conditions. 

The model is parameterized and empirically validated using high-resolution time-series data from Compartment 3.06 (Reference Strategy) of the **4th International Autonomous Greenhouse Challenge** (Wageningen University & Research, Bleiswijk, The Netherlands).

```text
      [ Raw WUR Datasets ]
 (reference.csv / Harvest.xlsx)
               │
               ▼
    notebooks/extract_data.ipynb  ──►  data/*.csv
               │
               ▼
       ┌────────────────┐
       │  src/climate   │  (5-min microclimate ──► Daily DLI & VPD)
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ src/physiology │  (Farquhar/Penman-Monteith process functions)
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │   src/model    │  (Daily dry matter, carbon allocation, FW per pot)
       └───────┬────────┘
               │
               ▼
notebooks/model_validation.ipynb  ──► [ Validation Charts ]

```

### Key Mathematical & Physiological Mechanisms

#### 1. Microclimate Aggregation (`src/climate.py`)

* Processes 5-minute interval sensor streams into daily integrals.
* Calculates Daily Light Integral ($\text{DLI}$, $\text{mol}\cdot\text{m}^{-2}\cdot\text{day}^{-1}$) from Photosynthetic Photon Flux Density ($\text{PPFD}$, $\mu\text{mol}\cdot\text{m}^{-2}\cdot\text{s}^{-1}$):

$$\text{DLI} = \sum \left(\text{PPFD} \times 10^{-6}\right) \times 300\text{ s}$$



#### 2. Crop Physiology (`src/physiology.py`)

* **Photosynthesis:** Evaluates gross carbon assimilation using a non-rectangular hyperbola light-response curve modulated by ambient $\text{CO}_2$ concentration (Marshall & Biscoe, 1980; Thornley & Johnson, 1990).
* **Vapor Pressure Deficit (VPD):** Computes atmospheric moisture demand ($\text{kPa}$) from air temperature ($T$) and relative humidity ($\text{RH}$) using empirical saturation vapor pressure formulations (Allen et al., 1998; Monteith & Unsworth, 2013):

$$\text{VP}_{\text{sat}} = 0.61078 \times \exp\left(\frac{17.27 \times T}{T + 237.3}\right), \quad \text{VPD} = \text{VP}_{\text{sat}} \times \left(1 - \frac{\text{RH}}{100}\right)$$


* **Canopy Transpiration:** Estimates daily water demand ($\text{L}\cdot\text{m}^{-2}\cdot\text{day}^{-1}$) driven by atmospheric vapor pressure deficit and radiation load (de Zwart, 1996; Stanghellini, 1987).

#### 3. Mechanistic Crop Growth & Partitioning (`src/model.py`)

* **Biomass Production:** Converts accumulated daily light into dry weight ($\text{g DW}\cdot\text{m}^{-2}\cdot\text{day}^{-1}$) via empirical Light Use Efficiency ($\text{LUE} = 8.4\text{ g FW}/\text{mol PAR}$).
* **Generative Carbon Allocation:** Dynamically scales assimilate partitioning toward reproductive sink organs (fruits) as plant phenology progresses.
* **Fresh Weight & Density Scaling:** Converts accumulated fruit dry matter into fresh weight per pot ($\text{g FW}/\text{pot}$) based on fruit dry matter fraction ($\sim 7\%$) and dynamic pot spacing density ($\delta = 56 \rightarrow 42 \rightarrow 30 \rightarrow 20\text{ pots}/\text{m}^2$).

#### 4. Empirical Validation (`notebooks/model_validation.ipynb`)

* Simulates the entire 74-day cultivation cycle and benchmarks predicted yield trajectories against destructive harvest trial metrics recorded across multiple sampling dates.

---

## Repository Structure

```text
mechanistic-tomato-crop-model/
├── data/
│   ├── Harvest.xlsx                  # Raw WUR harvest experimental spreadsheet
│   ├── greenhouse_climate.csv        # Processed 5-min microclimate time-series
│   ├── harvest_summary.csv           # Cleaned multi-date destructive harvest metrics
│   └── reference.csv                 # Raw WUR microclimate & actuators time-series
├── notebooks/
│   ├── extract_data.ipynb            # ETL pipeline for raw WUR challenge datasets
│   └── model_validation.ipynb        # Simulation execution & empirical validation plot
├── src/
│   ├── __init__.py
│   ├── climate.py                    # Data loader & daily DLI/VPD aggregator
│   ├── model.py                      # Object-oriented daily crop simulator
│   └── physiology.py                 # Photosynthesis, VPD, and transpiration logic
├── .gitignore                        # Git untracked files exclusion rules
├── LICENSE                           # Open-source project license
├── README.md                         # Model documentation & validation breakdown
└── requirements.txt                  # Project dependencies

```

---

## Model Validation & Discussion

The mechanistic growth model was validated against empirical destructive harvest trial data from WUR Compartment 3.06 (Reference Strategy) across three distinct harvest dates.

### Quantitative Performance Breakdown

| Date | Observed FW ($\text{g}/\text{pot}$) | Simulated FW ($\text{g}/\text{pot}$) | Absolute Error ($\text{g}/\text{pot}$) | Percentage Error ($\%$) | Status |
| --- | --- | --- | --- | --- | --- |
| **2024-10-22** | $0.00$ | $2.39$ | $2.39$ | — | **Excellent** (Near-zero ripening onset) |
| **2024-11-05** | $85.69$ | $101.65$ | $15.96$ | $18.6\%$ | **High Precision** (Mid-season trajectory) |
| **2024-11-15** | $275.20$ | $207.85$ | $67.34$ | $24.5\%$ | **Conservative** (Late-stage peak underestimation) |

**Overall Model Statistics:**

* **Mean Absolute Error (MAE):** $28.57\text{ g}/\text{pot}$
* **Root Mean Square Error (RMSE):** $39.98\text{ g}/\text{pot}$
* **Mean Absolute Percentage Error (MAPE):** $21.55%\$

---

### Physiological Discussion of Results

1. **Early & Mid-Season Accuracy ($2024-10-22$ and $2024-11-05$):**
The model effectively tracks early vegetative-to-generative transition dynamics and ripening onset. Incorporating an S-curve maturation delay accurately captures the zero-harvest state on October 22 while achieving an $18.6\%$ relative error on November 5.
2. **Late-Season Fresh Weight Underestimation ($2024-11-15$):**
The overall residual error ($\text{MAPE} = 21.55%\$) is primarily driven by the final harvest point, where observed fruit fresh weight reached $275.20\text{ g}/\text{pot}$ compared to the simulated $207.85\text{ g}/\text{pot}$.

* **Physiological Cause:** Standard Light Use Efficiency (LUE) frameworks assume a constant conversion factor from dry matter assimilation to total fresh weight. However, during final fruit maturation (post-breaker stage), dwarf tomatoes undergo rapid cellular expansion driven by sink-driven water uptake rather than additional dry matter accumulation. Because static LUE models do not account for late-stage cell enlargement and osmotic water uptake, the model yields a conservative fresh weight prediction at final harvest.

---

## Data Provenance & Attribution

The climate time-series, crop growth, and harvest metrics stored in `data/` are derived from open-access experimental datasets published via **4TU.ResearchData**:

* **Dataset Title:** 4th Autonomous Greenhouse Challenge: Dwarf Tomato Timeseries and Images


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

---

## References

* **Allen, R. G., Pereira, L. S., Raes, D., & Smith, M. (1998).** *Crop evapotranspiration: Guidelines for computing crop water requirements* (FAO Irrigation and Drainage Paper No. 56). Food and Agriculture Organization of the United Nations. http://www.climasouth.eu/sites/default/files/FAO%2056.pdf
* **de Zwart, H. F. (1996).** *Analyzing energy-saving options in greenhouse cultivation using a simulation model* [Doctoral dissertation, Wageningen Agricultural University]. WUR Repository. https://library.wur.nl/WebQuery/wda/919866
* **Maree, S. C., Zhang, P., van Marrewijk, B. M., de Zwart, F., Bijlaard, M., & Hemming, S. (2025).** Autonomous greenhouse cultivation of dwarf tomato: Performance evaluation of intelligent algorithms for multiple-sensor feedback. *Sensors*, 25(14), Article 4321. https://doi.org/10.3390/s25144321
* **Marshall, B., & Biscoe, P. V. (1980).** A model for C3 leaves describing the dependence of net photosynthesis on irradiance. *Journal of Experimental Botany*, 31(1), 29–39. https://doi.org/10.1093/jxb/31.1.29
* **Monteith, J. L., & Unsworth, M. H. (2013).** *Principles of environmental physics: Plants, animals, and the atmosphere* (4th ed.). Academic Press. https://doi.org/10.1016/B978-0-12-386910-4.00013-5
* **Stanghellini, C. (1987).** *Transpiration of greenhouse crops: An aid to climate management* [Doctoral dissertation, Wageningen Agricultural University]. WUR Repository. https://library.wur.nl/WebQuery/wda/488134

```

```
