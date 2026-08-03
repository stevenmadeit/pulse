
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select away_score
from "pulse"."public_public"."stg_sports"
where away_score is null



  
  
      
    ) dbt_internal_test