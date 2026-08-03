
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select game_date
from "pulse"."public_public"."stg_sports"
where game_date is null



  
  
      
    ) dbt_internal_test