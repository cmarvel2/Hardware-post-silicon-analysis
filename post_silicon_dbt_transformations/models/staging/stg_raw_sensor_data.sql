with
source as ( 
    select * from {{ source('hardware_raw', 'raw_sensor_data') }}
),

renamed as (

    select
        machine_id,
        workload_run_id,
        hardware_id,
        hardware_field_id,
        sensor_id,
        sensor_value as value, 
        collection_ts as sample_timestamp,

    from source 
    where sensor_value is not null

)

select * from renamed