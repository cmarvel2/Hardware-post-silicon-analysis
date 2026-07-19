# CPU Core Performance Validation Analysis

## Engineering Problem
"The CPU cores team needs to understand how the HX 370's two distinct core types — the four high-performance Zen 5 cores and the eight compact Zen 5c cores — differ in core power use during sustained steady-state workloads. The main question is whether each core type uses a different amount of core SMU power for every MHz of effective clock speed it sustains. In plain terms, the team needs to determine whether a MHz on a Zen 5c core is cheaper or more expensive in watts than a MHz on a Zen 5 core.

This needs to be measured across SSE, AVX2, and AVX512 workloads to determine whether the difference stays consistent across instruction sets. Package power, whole-CPU temperature, and effective clock speed will also be monitored to show whether the system remains stable after thermal ramp-up and whether package-level behavior changes by workload. The findings will document the measured power-per-clock trade-off between Zen 5 and Zen 5c on the tested ASUS ProArt P16 performance-mode configuration."

### Analytical Questions Derived from the Problem
- Does the efficiency ratio differ between Zen 5 and Zen 5c cores?
- Does package power, whole-CPU temperature, and effective clock speed remain stable during the steady-state period of each workload?

## Data Architecture
- High level diagram & dbt DAG
<img width="1502" height="601" alt="Data pathway" src="https://github.com/user-attachments/assets/eec5f26f-df9c-473b-a139-6ad50d600027" />


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
 
## Analysis & Validation report
- [Link to written report:](https://umich-my.sharepoint.com/:w:/g/personal/cmarvel_umich_edu/IQAfCteE0Ut2RqWBQZsi3vi6AYqR2JJwHK2cvWhPIUCI3GU?e=486AAi)
  
## What I've learned and Implemented
- Database design
- Building End-to-end Data Pipeliens
- Medallion Architecture
- PostgeSQL
- Simple visualizations with PowerBI and DAX
- dbt (models, staging, marts, fct, dim, etc...)

