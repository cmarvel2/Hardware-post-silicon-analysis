with
source as (
    select * from {{ source('hardware_raw', 'raw_workload_run_data') }}
),

renamed as (

    select
        workload_run_id,
        machine_id,
        workload_id,
        runtime_mins as runtime_minutes,
        run_date as started_at

    from source
)

select * from renamed