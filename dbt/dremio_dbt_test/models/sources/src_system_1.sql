{{ config(materialized='view') }}
select * from {{ source('src_system_1', 'table_name') }}