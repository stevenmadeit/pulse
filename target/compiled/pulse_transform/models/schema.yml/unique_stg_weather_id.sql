
    
    

select
    id as unique_field,
    count(*) as n_records

from "pulse"."public_public"."stg_weather"
where id is not null
group by id
having count(*) > 1


