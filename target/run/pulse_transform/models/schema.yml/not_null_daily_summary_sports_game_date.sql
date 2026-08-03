
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sports_game_date
from "pulse"."public_public"."daily_summary"
where sports_game_date is null



  
  
      
    ) dbt_internal_test