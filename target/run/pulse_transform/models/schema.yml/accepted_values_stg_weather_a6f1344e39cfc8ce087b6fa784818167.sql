
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

with all_values as (

    select
        condition as value_field,
        count(*) as n_records

    from "pulse"."public_public"."stg_weather"
    group by condition

)

select *
from all_values
where value_field not in (
    'clear','mainly_clear','partly_cloudy','overcast','fog','depositing_rime_fog','drizzle_light','drizzle_moderate','drizzle_dense','freezing_drizzle_light','freezing_drizzle_dense','rain_slight','rain_moderate','rain_heavy','freezing_rain_light','freezing_rain_heavy','snow_fall_slight','snow_fall_moderate','snow_fall_heavy','snow_grains','rain_showers_slight','rain_showers_moderate','rain_showers_violent','snow_showers_slight','snow_showers_heavy','thunderstorm_slight_or_moderate','thunderstorm_hail_slight','thunderstorm_hail_heavy','unknown'
)



  
  
      
    ) dbt_internal_test