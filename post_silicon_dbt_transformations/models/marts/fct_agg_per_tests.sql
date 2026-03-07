with test_data as (
    select * from {{ref('int_sensor_data')}}
)

select
    test_id,
    hardware_id,
    hardware_field_id,
    instver_id,
    load_id,
    mode_id,
    dataset_id,
    sensor_id,
    max(sensor_value) as max_sensor_value,
    avg(sensor_value) as avg_sensor_value,
    min(sensor_value) as min_sensor_value
from test_data
where seconds_from_start > 600
group by 1,2,3,4,5,6,7,8