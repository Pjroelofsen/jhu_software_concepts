SELECT * FROM application_data;

1) SELECT COUNT(*) FROM application_data WHERE term = 'Fall 2024';

2) SELECT 
	    COUNT(*) as total_entries,
	    COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) as international_entries,
	    ROUND(
	        (COUNT(CASE WHEN us_or_international = 'International' THEN 1 END) * 100.0 / COUNT(*)), 
	        2
	    ) as international_percentage
	FROM application_data;

3) SELECT 
	    COUNT(gpa) as gpa_count,
	    ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa,
	    COUNT(gre) as gre_quant_count,
	    ROUND(AVG(gre)::NUMERIC, 2) as avg_gre_quant,
	    COUNT(gre_v) as gre_verbal_count,
	    ROUND(AVG(gre_v)::NUMERIC, 2) as avg_gre_verbal,
	    COUNT(gre_aw) as gre_writing_count,
	    ROUND(AVG(gre_aw)::NUMERIC, 2) as avg_gre_writing
	FROM application_data;

4) SELECT 
	    COUNT(gpa) as american_students_with_gpa,
	    ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa_american_fall2024
	FROM application_data 
	WHERE us_or_international = 'American' 
	  AND term = 'Fall 2024' 
	  AND gpa IS NOT NULL;
5) SELECT 
    COUNT(*) as total_fall2024,
    COUNT(CASE WHEN status LIKE '%Accept%' THEN 1 END) as acceptances,
    ROUND(
        (COUNT(CASE WHEN status LIKE '%Accept%' THEN 1 END) * 100.0 / COUNT(*))::NUMERIC, 
        2
    ) as acceptance_percentage
FROM application_data 
WHERE term = 'Fall 2024';

6) SELECT 
    COUNT(gpa) as accepted_students_with_gpa,
    ROUND(AVG(gpa)::NUMERIC, 2) as avg_gpa_accepted_fall2024
FROM application_data 
WHERE term = 'Fall 2024' 
  AND status LIKE '%Accept%'
  AND gpa IS NOT NULL;

7) SELECT COUNT(*) as jhu_cs_masters_count
FROM application_data 
WHERE (program ILIKE '%johns hopkins%' OR program ILIKE '%jhu%')
  AND program ILIKE '%computer science%'
  AND degree ILIKE '%masters%';