# CPU Cores Post Silicon Analysis

## Engineering Problem
"The CPU cores team needs to understand how the HX 370's two distinct core types — the four high-performance Zen 5 cores and the eight efficiency-focused Zen 5c cores — diverge in their power consumption behavior when subjected to a sustained steady-state workload. The team already knows clock frequency and temperature lock in tight. What is less characterized is whether the two core architectures draw power differently per unit of clock frequency they sustain: in plain terms, is each MHz of frequency on a Zen 5c core "cheaper" or "more expensive" in watts than on a Zen 5 core, and does that relationship hold the same way across SSE, AVX2, and AVX512? The team needs this quantified across all three instruction sets so that any architectural difference in per-core power efficiency between Zen 5 and Zen 5c can be identified, documented, and compared against what the cTDP design range would predict."

### Analytical Questions Derived from the Problem
- Does the efficiency ratio differ between Zen 5 and Zen 5c cores?
- Does that difference hold consistently across SSE, AVX2, and AVX512, or does it change?

## Data Architecture
- High level diagram
<img width="1502" height="601" alt="Data pathway" src="https://github.com/user-attachments/assets/eec5f26f-df9c-473b-a139-6ad50d600027" />

- dbt DAG
<img width="2497" height="1550" alt="image" src="https://github.com/user-attachments/assets/547ee094-359c-4545-a4a8-483add1ecd95" />

## Prerequisites / How to Run The Project
- Any benchmarking tool (This was made with OCCT in mind)
- PostgreSQL (Or Azure PostgreSQL for multiple devices)
- DBT Core

Steps:
- Install all the libraries with `pip install -r requirements.txt`
- Create your .env file and set your variables for your PostgreSQL database
- Open main.py and set endtime to the amount of time you intend on running your workload in minutes
- Open main.py and set chosen_workload to the you intend on using from your benchmarking software
- Run your benchmark software and main.py script alongside it with high priority and review logs console to ensure the program is executing successfully
- from `cd post_silicon_dbt_transformations` folder run `dbt build` to create new dbt models used by Power BI within your PostgreSQL database
 
## Analyses and Dashboard
- Writing Report
  
## What I've learned and Implemented
- Database design
- Building End-to-end Data Pipeliens
- Medallion Architecture
- PostgeSQL
- Simple visualizations with PowerBI and DAX
- dbt (models, staging, marts, fct, dim, etc...)

