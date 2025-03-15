CREATE OR REPLACE PROCEDURE `helios-tech-interview-project.result_test.pr_2_daily_risk`(pr_h3_index INT64, pr_crop_id_or_name STRING)
BEGIN
  /** 
   * #### h3_index_param
   * This procedure must be run for each h3index_num (linked to a specific lat/long) 
   * as each location has slightly different climatic conditions.
   **/
   
  /** 
   * #### pr_crop_id_or_name
   * Accepts either crop_id or crop name as a string to filter the crop information.
   **/
  
  CREATE OR REPLACE TABLE `helios-tech-interview-project.result_test.tb_2_daily_risk`
  AS
  WITH 
  CTE_Crop AS (
    -- Get crop info (id, name, temperature range) for the specified crop_id or name
    SELECT DISTINCT
        crop_id, name, temp_min, temp_max 
    FROM `helios-tech-interview-project.shared.crop_info`
    WHERE crop_id = pr_crop_id_or_name
    OR name = pr_crop_id_or_name
  )
  
  ,CTE_Supplier AS (
    -- Fetch suppliers for the given h3index_num and crop, joining with the crop info
    SELECT 
       sp.poi_id
      ,sp.supplier_name
      ,sp.h3index_num
      ,sp.crop_id
      ,cr.name as crop_name
      ,cr.temp_min
      ,cr.temp_max 
    FROM `helios-tech-interview-project.shared.places_of_interest` sp
    INNER JOIN CTE_Crop cr on cr.crop_id = sp.crop_id
    WHERE sp.h3index_num = pr_h3_index
  )
  
  ,CTE_Result AS (
    -- Calculate risk status by checking if the daily temperature is within the crop's min/max temperature range
    SELECT 
    sp.* 
    ,hs.date_on
    ,hs.temp
    ,CASE 
        WHEN hs.temp > sp.temp_min AND hs.temp < sp.temp_max
        THEN 0 -- Within the safe temperature range
        ELSE 1 -- Outside the safe temperature range
      END AS risk_status
    FROM CTE_Supplier sp
    INNER JOIN `helios-tech-interview-project.weather_data.historical_weather_raw_import` hs on hs.h3index_num = sp.h3index_num  
  )

  -- Final result selection, excluding some unnecessary columns for the final table
  SELECT 
    * EXCEPT(crop_name, temp_min, temp_max, temp) 
  FROM CTE_Result
  ;
END;