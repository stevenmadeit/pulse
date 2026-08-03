
    
    

select
    id as unique_field,
    count(*) as n_records

from "pulse"."public_public"."stg_crypto"
where id is not null
group by id
having count(*) > 1


