
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select coin
from "pulse"."public_public"."stg_crypto"
where coin is null



  
  
      
    ) dbt_internal_test