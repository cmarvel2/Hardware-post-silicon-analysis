# CPU Cores Post Silicon Analysis

## Engineering Problem
"The CPU cores team needs to understand how the HX 370's cores behave under sustained workloads specifically, how fast the clock speed drops from its advertised peak and at what temperature it stabilizes. AVX and AVX2 instruction sets are expected to push the cores harder than SSE by design, but the team needs to quantify by how much: whether the frequency penalty each instruction set carries is proportional to the additional thermal and power demand it creates, and whether any instruction set is hitting the chip's limits harder than the architecture intends. This needs to be characterized and visualized so the team has a documented record of the chip's sustained performance envelope and the cost in frequency and temperature of moving up the instruction set stack."

### Engineering Questions Derived from the Problem
- Over SSE, AVX, and AVX2 tests when does the clock speed drop from the advertised speed (if it reaches it) and at what temperature does the clock speed stabilize?
- What is the average Clock speed, tctl/tdie and package power for the CPU under each instruction set and are the porportional to each other?
- What is the Max Clock speed and tctl/tdie for each test and how closely do they approach the Max GHz and Max Operating Temperature?


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

