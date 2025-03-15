CREATE OR REPLACE FUNCTION `helios-tech-interview-project.result_test.fc_end_day_week_of_year`(YEAR INT64, WEEK_NUM INT64) RETURNS DATE AS (
(    
    SELECT DATE(`helios-tech-interview-project.result_test.fc_first_day_week_of_year`(YEAR, WEEK_NUM) + INTERVAL 6 DAY)
  )
);