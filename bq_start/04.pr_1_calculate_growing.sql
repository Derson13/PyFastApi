CREATE OR REPLACE PROCEDURE `helios-tech-interview-project.result_test.pr_1_calculate_growing`(pr_h3_index INT64, pr_crop_id_or_name STRING)
BEGIN
  DECLARE table_exists BOOL;

  /** 
   * #### h3_index_param
   * This procedure needs to be run for each h3index_num (tied to a specific location) 
   * as each location has different climatic conditions affecting the growing season.
   **/

  /** 
   * #### pr_crop_id_or_name
   * Accepts either crop_id or crop name as a string to filter the crop information.
   **/
  
  CREATE TEMP TABLE TBL_TEMP AS
  
  WITH 
  CTE_CROP_TEMP AS (
    -- Fetch crop temperature range (min and max) based on provided crop_id or name
    SELECT DISTINCT
      1 AS id, crop_id, temp_min, temp_max 
    FROM `shared.crop_info`
    WHERE crop_id = pr_crop_id_or_name
    OR name = pr_crop_id_or_name
  )
  
  ,CTE_WEEKLY_AVG AS (
      -- Calculate weekly average min and max temperature for the given h3index_num and year range
      SELECT  
        wi.h3index_num,
        wi.date_on_year, 
        wi.date_on_week,
        AVG(wi.tempmin) AS tempmin_wk_avg,
        AVG(wi.tempmax) AS tempmax_wk_avg
      FROM `weather_data.historical_weather_raw_import` wi
      WHERE date_on_year >= (SELECT MIN(pr_year) FROM `result_test.vw_weight`)  -- Include data starting from the earliest year available for weight
      AND wi.h3index_num = pr_h3_index
      GROUP BY 1, 2, 3
  )
  
  ,CTE_WEIGHTED_WEEKLY_AVG AS (
    -- Compute weighted average temperature using the crop weight for each week
    SELECT 
      wk.h3index_num,
      wk.date_on_week,
      SUM(wk.tempmin_wk_avg * wg.pr_weight) AS weighted_mintemp_ten_yr_avg,
      SUM(wk.tempmax_wk_avg * wg.pr_weight) AS weighted_maxtemp_ten_yr_avg
    FROM CTE_WEEKLY_AVG wk
    LEFT JOIN `result_test.vw_weight` wg ON wg.pr_year = wk.date_on_year  
    GROUP BY 1, 2
  )
  
  ,CTE_IN_SEASON AS (
    -- Identify if the crop is in-season based on min/max temperatures
    SELECT 
      wa.h3index_num,
      cr.crop_id,
      wa.date_on_week,
      wa.weighted_mintemp_ten_yr_avg,
      wa.weighted_maxtemp_ten_yr_avg,
      CASE
        WHEN wa.weighted_mintemp_ten_yr_avg > cr.temp_min AND wa.weighted_maxtemp_ten_yr_avg < cr.temp_max 
        THEN 1  -- Crop is in-season
        ELSE 0   -- Crop is not in-season
      END AS in_season        
    FROM CTE_WEIGHTED_WEEKLY_AVG wa
    LEFT JOIN CTE_CROP_TEMP cr ON cr.id = 1  
  )

  ,CTE_PREV_IN_SEASON AS (
    -- Compare the current in_season with the previous week using LAG function
    SELECT 
        * EXCEPT(weighted_mintemp_ten_yr_avg, weighted_maxtemp_ten_yr_avg)
        ,LAG(in_season) OVER (PARTITION BY h3index_num, crop_id ORDER BY date_on_week) AS previous_in_season
    FROM CTE_IN_SEASON
  )
  
  ,CTE_RANK AS (
    -- Generate a rank sequence whenever there is a change in in_season (crop starts or ends season)
    SELECT 
        *    
        ,SUM(CASE WHEN in_season != previous_in_season THEN 1 ELSE 0 END) 
        OVER (PARTITION BY h3index_num, crop_id ORDER BY date_on_week) + 1 AS rank_group
    FROM CTE_PREV_IN_SEASON  
    ORDER BY 1, 2, 3
  )
  
  ,CTE_SEASON_WEEK AS (
    -- Calculate the start and end weeks of the growing season for each rank_group
    SELECT
      * EXCEPT(date_on_week, in_season, previous_in_season, rank_group)
      ,MIN(date_on_week) AS season_start_week
      ,MAX(date_on_week) AS season_end_week
    FROM CTE_RANK
    WHERE in_season = 1  -- Only consider rows where the crop is in-season
    GROUP BY h3index_num, crop_id, rank_group
  )
  
  ,CTE_SEASON_DATE AS (
    -- Calculate the exact start and end date of the season based on the week range
    SELECT
      *
      ,`result_test.fc_first_day_week_of_year`(EXTRACT(YEAR FROM CURRENT_DATE()), season_start_week) AS season_start_date
      ,`result_test.fc_end_day_week_of_year`(EXTRACT(YEAR FROM CURRENT_DATE()), season_end_week) AS season_end_date
      ,season_end_week - season_start_week AS length_of_season_weeks      
    FROM CTE_SEASON_WEEK
  )
  
  ,CTE_RESULT AS (
    -- Calculate the number of days the growing season lasts
    SELECT
      *
      ,DATE_DIFF(season_end_date, season_start_date, DAY) AS length_of_season_days
    FROM CTE_SEASON_DATE
  )

  -- Final result selection
  SELECT * FROM CTE_RESULT;

  -- Check if the destination table already exists
  SET table_exists = (
    SELECT COUNT(*) > 0
    FROM `result_test`.INFORMATION_SCHEMA.TABLES
    WHERE table_name = 'tb_1_growing_seasons'
  );

  IF NOT table_exists THEN
    -- Create the final table from the temporary table if it does not exist
    CREATE TABLE `result_test.tb_1_growing_seasons` AS
    SELECT * FROM TBL_TEMP;
  ELSE
    -- Delete existing records to avoid duplicates before inserting new data
    DELETE FROM `result_test.tb_1_growing_seasons`
    WHERE EXISTS (
        SELECT 1
        FROM TBL_TEMP tm
        WHERE tm.h3index_num = `result_test.tb_1_growing_seasons`.h3index_num
          AND tm.crop_id = `result_test.tb_1_growing_seasons`.crop_id
    );

    -- Insert the new data into the table
    INSERT INTO `result_test.tb_1_growing_seasons`
    SELECT * FROM TBL_TEMP;
  END IF;

END;