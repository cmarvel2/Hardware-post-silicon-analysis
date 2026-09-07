# CPU Core Performance Validation Pipeline

## Engineering Problem
"The CPU cores team needs to understand how the AMD Ryzen AI 9 HX 370's two distinct core types — the four high-performance Zen 5 cores and the eight compact Zen 5c cores — differ in core power use during sustained steady-state workloads. The main question is whether each core type uses a different amount of core SMU power for every MHz of effective clock speed it sustains. In plain terms, the team needs to determine whether a MHz on a Zen 5c core is cheaper or more expensive in watts than a MHz on a Zen 5 core. This needs to be measured across SSE, AVX2, and AVX512 workloads while package power, whole-CPU temperature, and effective clock speed are monitored to verify steady-state behavior after thermal ramp-up.

The original analysis was completed with a Python and LibreHardwareMonitor collection process, an Azure PostgreSQL warehouse, dbt transformations, and Power BI reporting. As the project expands to collect larger sensor batches across CPU, GPU, and memory sources, the PostgreSQL-centered workflow needs to be migrated to an Azure Databricks lakehouse architecture. Azure Data Lake Storage is needed to retain raw JSON sensor batches, while Databricks and Unity Catalog provide a governed environment for organizing, transforming, validating, and reproducing the original analysis at a larger scale. The goal is to preserve the completed Zen 5 versus Zen 5c analytical reasoning while replacing the storage and transformation architecture with a more scalable data-engineering design."

### Analytical Questions Derived from the Problem
- Does the efficiency ratio differ between Zen 5 and Zen 5c cores?
- Does package power, whole-CPU temperature, and effective clock speed remain stable during the steady-state period of each workload?

## Data Architecture
The pipeline collects CPU, GPU, and memory sensor data from the local hardware device through a Python ingestion script using LibreHardwareMonitor. The ingestion process buffers sensor snapshots into JSON payloads and uploads the raw batches to an Azure Data Lake Storage landing container.

Azure Databricks processes the raw sensor data through Bronze, Silver, and Gold layers. The Bronze layer retains the raw landed data, the Silver layer standardizes and cleans the sensor records, and the Gold layer prepares the datasets for downstream hardware performance reporting. Unity Catalog provides governance for the lakehouse data and Power BI consumes the Gold-layer datasets for analysis.

- High level pipeline diagram
![alt text](<data diag.png>)

## Prerequisites / How to Run The Project
**The original pipeline used Azure PostgreSQL as a tightly coupled database centered storage and transformation layer. The current project is undergoing a migration to a decoupled lakehouse architecture built on Azure Data Lake Storage and Azure Databricks.**
 
## Analysis & Validation report
- Link to written report: (https://umich-my.sharepoint.com/:w:/g/personal/cmarvel_umich_edu/IQAfCteE0Ut2RqWBQZsi3vi6AYqR2JJwHK2cvWhPIUCI3GU?e=486AAi)