
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select weather_city
from "pulse"."public_public"."daily_summary"
where weather_city is null



  
  
      
    ) dbt_internal_test