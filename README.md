# CPU Cores Post Silicon Analysis

## Engineering Problem
"The CPU cores team needs to understand how the HX 370's cores behave under sustained workloads — specifically, 
how fast the clock speed drops from its advertised peak, what temperature causes it to stop dropping and hold steady, 
and whether running different types of math-heavy instructions (SSE, AVX, AVX2) changes that behavior. 
We need this characterized and visualized so the team can set realistic performance expectations and 
identify whether any instruction set is pushing the cores harder than the others."

### Engineering Questions


## Data Architecture
- High level diagram
<img width="1502" height="601" alt="Data pathway" src="https://github.com/user-attachments/assets/eec5f26f-df9c-473b-a139-6ad50d600027" />


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
- Data collection still in progress
  
## What I've learned

