
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select crypto_coin
from "pulse"."public_public"."daily_summary"
where crypto_coin is null



  
  
      
    ) dbt_internal_test