# Hardware Post Silicon Analysis

# Overview 
This project began as a simple monitoring tool with psutil to attempt to build around 
my interest in computing hardware along with analytics and has evolved to become an end-to-end 
ELT pipeline aiming at simulating what hardware analytics teams do by gathering CPU, GPU, and memory
data from my devices.

### Data Architecture
- High level diagram
  <img width="3288" height="1048" alt="image" src="https://github.com/user-attachments/assets/e6b94bf3-b8fa-4454-bef1-830eface12c5" />
  - The first PostgreSQL block represents where the raw data is loaded and the second is where the dbt transformed data is loaded.

# Prerequisites
- Any benchmarking tool (This was made with OCCT in mind)
- PostgreSQL (Or Azure PostgreSQL for multiple devices)
- DBT Core

# How to Run The Project
- Install all the libraries with `pip install -r requirements.txt`
- Create your .env file and set your variables for your PostgreSQL database
- Open main.py and set endtime to the amount of time you intend on running your workload in minutes
- Open main.py and set chosen_workload to the you intend on using from your benchmarking software
- Run your benchmark software main.py script alongside it and reviewthe logs console to ensure the program is working correctly
- from `cd post_silicon_dbt_transformations` folder run `dbt build` now to create new dbt models used by Power BI within your PostgreSQL database
 
# Analyses of Data
- Data collection still in progress
  
  

