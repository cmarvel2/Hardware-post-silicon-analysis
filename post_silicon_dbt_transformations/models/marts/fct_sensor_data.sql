with stg_raw_sensor_data as (
    select *
    from {{ ref("stg_raw_sensor_data") }}
),

stg_raw_workload_run as (
    select *
    from {{ ref("stg_raw_workload_run_data") }}

)

select
    srsd.machine_id,
    srsd.workload_run_id,
    srwr.workload_id,
    srsd.hardware_id,
    srsd.hardware_field_id,
    srsd.sensor_id,
    srsd.value,
    srsd.sample_timestamp,
    srwr.runtime_minutes,
    srwr.started_at
from stg_raw_sensor_data srsd
left join stg_raw_workload_run srwr
    on srsd.workload_run_id = srwr.workload_run_id
