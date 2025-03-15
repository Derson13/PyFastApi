CREATE OR REPLACE FUNCTION `helios-tech-interview-project.result_test.fc_first_day_week_of_year`(YEAR INT64, WEEK_NUM INT64) RETURNS DATE AS (
(    
    WITH 
    -- Capturing the 7 days prior to the 1st day of the year
    CTE_DATES AS (
      SELECT
        DATE_ADD(DATE(YEAR, 1, 1), INTERVAL -x DAY) AS date_in_range
      FROM UNNEST(GENERATE_ARRAY(0, 7)) AS x -- Generates an array with 8 elements, representing the days from 0 to 7
      ORDER BY 1
    )
    ,CTE_WEEK_NUMBER AS (
      SELECT 
        * 
        ,EXTRACT(ISOWEEK FROM date_in_range) AS week_number -- Extracts the ISO week number from the date_in_range
      FROM CTE_DATES
    )
    ,CTE_FIRST_DAY AS (
      SELECT 
        MIN(date_in_range) AS first_day_of_week -- Finds the first day of the week
      FROM CTE_WEEK_NUMBER 
      WHERE week_number = 1 -- Filters to find the first week of the year
    )

    -- Adds the specified number of weeks (WEEK_NUM) to the first day of the first week
    SELECT 
      DATE_ADD(
        (SELECT first_day_of_week FROM CTE_FIRST_DAY), -- Gets the first day of the first week
        INTERVAL (WEEK_NUM - 1) WEEK -- Adds the number of weeks specified by WEEK_NUM
      ) AS first_day_of_week -- Returns the first day of the desired week

  )
);