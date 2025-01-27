# SQL Cheat Sheet

## Basic SQL Commands

### SELECT
```sql
SELECT column1, column2
FROM table_name
WHERE condition;

-- Use a CTE to calculate the difference in temperature from the previous row
WITH TemperatureDifferences AS (
    SELECT
        id,
        city,
        timestamp,
        temperature,
        LAG(temperature) OVER (PARTITION BY city ORDER BY timestamp) AS previous_temperature,
        temperature - LAG(temperature) OVER (PARTITION BY city ORDER BY timestamp) AS temperature_difference
    FROM weather_temperatures
)
SELECT
    id,
    city,
    timestamp,
    temperature,
    previous_temperature,
    temperature_difference
FROM TemperatureDifferences
ORDER BY timestamp;

-- Use a window function to calculate the running average temperature
SELECT
    id,
    city,
    timestamp,
    temperature,
    AVG(temperature) OVER (PARTITION BY city ORDER BY timestamp ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg_temperature
FROM weather_temperatures
ORDER BY timestamp;

-- Use a ranking function to rank the temperatures within each city
SELECT
    id,
    city,
    timestamp,
    temperature,
    RANK() OVER (PARTITION BY city ORDER BY temperature DESC) AS temperature_rank
FROM weather_temperatures
ORDER BY timestamp;

-- Use a window function to calculate the cumulative sum of temperatures
SELECT
    id,
    city,
    timestamp,
    temperature,
    SUM(temperature) OVER (PARTITION BY city ORDER BY timestamp) AS cumulative_temperature
FROM weather_temperatures
ORDER BY timestamp;

WITH CTE AS (
    SELECT column1, column2
    FROM table_name
    WHERE condition
)
SELECT *
FROM CTE;

SELECT
    column1,
    LAG(column1) OVER (PARTITION BY column2 ORDER BY column3) AS previous_value
FROM table_name;

SELECT
    column1,
    AVG(column1) OVER (PARTITION BY column2 ORDER BY column3 ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_avg
FROM table_name;

SELECT
    column1,
    RANK() OVER (PARTITION BY column2 ORDER BY column3 DESC) AS rank
FROM table_name;