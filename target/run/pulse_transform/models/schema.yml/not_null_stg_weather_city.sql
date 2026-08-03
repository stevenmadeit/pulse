
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city
from "pulse"."public_public"."stg_weather"
where city is null



  
  
      
    ) dbt_internal_test