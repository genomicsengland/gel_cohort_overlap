select distinct dg.identifier_value, coalesce(de.value_datetime::varchar, 
							de.value_string::varchar,
						    de.value_numeric::varchar, 
						    de.value_integer::varchar,
						    de.value_boolean::varchar,
						    c.concept_code ) as val,
						    c2.concept_code
            from pmi.data_group dg 
            join pmi.data_element de 
            on dg.uid = de.data_group_uid 
            left join pmi.concept c 
            on c.uid = de.value_cid 
            left join pmi.concept c2 
            on c2.uid = de.field_type_cid 
            join pmi.concept c3 
            on c3.uid = dg.data_group_type_cid 
            where stale = false
            and c3.concept_code in ('date_of_birth','nhs_number')
            order by dg.identifier_value