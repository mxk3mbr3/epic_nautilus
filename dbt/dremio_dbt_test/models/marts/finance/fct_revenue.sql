with total_revenue as (
    select
        order_id,
        sum(revenue) as revenue
    from {{ ref('orders_fct') }}
    group by order_id
)
select * from total_revenue
