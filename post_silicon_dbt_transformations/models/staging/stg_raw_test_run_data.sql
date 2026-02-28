with
source as (
    select * from {{ source('hardware_raw', 'raw_test_run_data') }}
),

renamed as (

    select
        test_run_id,
        machine_id,
        test_id,
        instver_id,
        load_id,
        mode_id,
        dataset_id,
        runtime_mins as runtime_minutes,
        run_date as started_at

    from source
)

select * from renamed