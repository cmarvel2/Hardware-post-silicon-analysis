with sensor_types as (
    select * from {{source('hardware_raw', 'sensor_types')}}
),

hardware_types as (
    select * from {{source('hardware_raw', 'hardware_types')}}
),

hardware_fields as (
    select * from {{source('hardware_raw', 'hardware_fields')}}
),

stg_raw_sensor_data as (
    select * from {{ ref('stg_raw_sensor_data') }}
)

select * from (
select distinct
    st.sensor_id,
    st.sensor_name,
    ht.hardware_name,
    hf.hardware_field,
    case
        when ht.hardware_name = 'AMD Ryzen AI 9 HX 370 w/ Radeon 890M'
            and hf.hardware_field in (
                'cpu_clock',
                'cpu_power',
                'cpu_temperature'
            ) 
            and ( 
                st.sensor_name like 'Core #1%'
                or st.sensor_name like 'Core #2%'
                or st.sensor_name like 'Core #3%'
                or st.sensor_name like 'Core #4%'
            )
        then 'Zen 5'

        when ht.hardware_name = 'AMD Ryzen AI 9 HX 370 w/ Radeon 890M'
            and hf.hardware_field in (
                'cpu_clock',
                'cpu_power',
                'cpu_temperature'
            ) 
            and (
                st.sensor_name like 'Core #5%'
                or st.sensor_name like 'Core #6%'
                or st.sensor_name like 'Core #7%'
                or st.sensor_name like 'Core #8%'
                or st.sensor_name like 'Core #9%'
                or st.sensor_name like 'Core #10%'
                or st.sensor_name like 'Core #11%'
                or st.sensor_name like 'Core #12%'
            )
        then 'Zen 5c'

        else null
    end as core_type
from stg_raw_sensor_data srsd
inner join sensor_types st
    on srsd.sensor_id = st.sensor_id
inner join hardware_types ht
    on srsd.hardware_id = ht.hardware_id
inner join hardware_fields hf
    on srsd.hardware_field_id = hf.field_id
)
where core_type is not null

