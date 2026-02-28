with stg_raw_sensor_data as (
    select *
    from {{ ref("stg_raw_sensor_data") }}
),

stg_raw_test_run as (
    select *
    from {{ ref("stg_raw_test_run_data") }}

)

select
    srsd.machine_id,
    srsd.test_run_id,
    srtr.test_id,
    srtr.instver_id,
    srtr.load_id,
    srtr.mode_id,
    srtr.dataset_id,
    srsd.hardware_id,
    srsd.hardware_field_id,
    srsd.sensor_id,
    srsd.value,
    srsd.sample_timestamp,
    srtr.runtime_minutes,
    srtr.started_at
from stg_raw_sensor_data srsd
left join stg_raw_test_run srtr
    on srsd.test_run_id = srtr.test_run_id
