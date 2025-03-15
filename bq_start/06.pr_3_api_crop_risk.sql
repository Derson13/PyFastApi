CREATE OR REPLACE PROCEDURE `helios-tech-interview-project.result_test.pr_3_api_crop_risk`(pr_crop_id_or_name STRING, actual_temp FLOAT64)
BEGIN
  #### pr_crop_id_or_name: This parameter accepts only string values​ ​and can receive either the crop_id or the name of the crop.
  #### actual_temp:  Current temperature
    
  SELECT DISTINCT
      crop_id, name, temp_min, temp_max, actual_temp as temperature
      ,CASE 
        WHEN actual_temp > temp_min AND actual_temp < temp_max
        THEN 1 --Inside the Range
        ELSE 0 --Out of Range
      END AS risk_status
      ,CASE 
        WHEN actual_temp > temp_min AND actual_temp < temp_max
        THEN 'in season' --Inside the Range
        ELSE 'out of season' --Out of Range
      END AS risk_desc
  FROM `helios-tech-interview-project.shared.crop_info`
  WHERE crop_id = pr_crop_id_or_name
  OR name = pr_crop_id_or_name;  
END;