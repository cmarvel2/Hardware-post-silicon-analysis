with source as (
    select *
    from {{ ref("stg_raw_sensor_data") }}
),


