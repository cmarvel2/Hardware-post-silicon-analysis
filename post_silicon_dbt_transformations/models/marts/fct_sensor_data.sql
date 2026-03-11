with stg_raw_sensor_data as (
    select * from {{ ref("stg_raw_sensor_data") }}
),

stg_raw_test_run as (
    select * from {{ ref("stg_raw_test_run_data") }}
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
    srsd.sensor_value,
    srtr.runtime_minutes,
    {{dbt.datediff('srtr.started_at', 'srsd.sample_timestamp', 'second')}} as seconds_from_start,
    case
        when {{dbt.datediff('srtr.started_at', 'srsd.sample_timestamp', 'second')}} <= 600 then True
        else False
    end as thermal_rampup
from stg_raw_sensor_data srsd
inner join stg_raw_test_run srtr
    on srsd.test_run_id = srtr.test_run_id
