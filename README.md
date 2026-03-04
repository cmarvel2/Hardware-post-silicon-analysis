# Hardware Post Silicon Analysis

# Engineering Problem
"The HX 370 is rated for a 5.1 GHz boost clock, but sustained workloads force the chip to trade frequency for thermal headroom. 
Characterize how quickly boost collapses under sustained CPU stress, at what temperature the sustained frequency ceiling stabilizes, 
and whether that ceiling differs across SSE vs. AVX vs. AVX2 instruction sets."

# Data Architecture
- High level diagram
<img width="1502" height="601" alt="Data pathway" src="https://github.com/user-attachments/assets/eec5f26f-df9c-473b-a139-6ad50d600027" />


# Prerequisites / How to Run The Project
- Any benchmarking tool (This was made with OCCT in mind)
- PostgreSQL (Or Azure PostgreSQL for multiple devices)
- DBT Core

- Install all the libraries with `pip install -r requirements.txt`
- Create your .env file and set your variables for your PostgreSQL database
- Open main.py and set endtime to the amount of time you intend on running your workload in minutes
- Open main.py and set chosen_workload to the you intend on using from your benchmarking software
- Run your benchmark software main.py script alongside it and reviewthe logs console to ensure the program is working correctly
- from `cd post_silicon_dbt_transformations` folder run `dbt build` now to create new dbt models used by Power BI within your PostgreSQL database
 
# Analyses of Data
- Data collection still in progress
  
  

