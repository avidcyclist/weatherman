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
    temperature_f,
    RANK() OVER (PARTITION BY city ORDER BY temperature_f DESC) AS temperature_rank
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

### Average Temperature


SELECT
    city,
    AVG(temperature_f) AS average_temperature
FROM weather_temperatures
GROUP BY city;

### Maximum Temperature

SELECT
    city,
    MAX(temperature_f) AS max_temperature
FROM weather_temperatures
GROUP BY city;

-- Select all records from the weather_temperatures table
SELECT *
FROM weather_temperatures;

-- Select specific columns from the weather_temperatures table
SELECT city, temperature, temperature_f, recorded_at
FROM weather_temperatures;

-- Filter records for a specific city
SELECT *
FROM weather_temperatures
WHERE city = 'Bloomington';


-- Sort records by temperature in ascending order
SELECT *
FROM weather_temperatures
ORDER BY temperature ASC;

-- Sort records by temperature in descending order
SELECT *
FROM weather_temperatures
ORDER BY temperature DESC;

-- Sort records by recorded_at timestamp in ascending order
SELECT *
FROM weather_temperatures
ORDER BY recorded_at ASC;

-- Sort records by recorded_at timestamp in descending order
SELECT *
FROM weather_temperatures
ORDER BY recorded_at DESC;

-- Calculate the average temperature for each city
SELECT city, AVG(temperature) AS average_temperature
FROM weather_temperatures
GROUP BY city;

-- Calculate the maximum temperature for each city
SELECT city, MAX(temperature) AS max_temperature
FROM weather_temperatures
GROUP BY city;

-- Calculate the minimum temperature for each city
SELECT city, MIN(temperature) AS min_temperature
FROM weather_temperatures
GROUP BY city;

-- Calculate the sum of temperatures for each city
SELECT city, SUM(temperature) AS total_temperature
FROM weather_temperatures
GROUP BY city;

-- Temps between certain degrees
SELECT *
FROM weather_temperatures
WHERE temperature BETWEEN -10 AND 0;

-- Records by date
-- Ascending order
SELECT *
FROM weather_temperatures
ORDER BY recorded_at ASC;

-- Descending order
SELECT *
FROM weather_temperatures
ORDER BY recorded_at DESC;

-- Count Records By City
SELECT city, COUNT(*) AS record_count
FROM weather_temperatures
GROUP BY city;

-- Average Temperature by City
SELECT city, AVG(temperature) AS average_temperature
FROM weather_temperatures
GROUP BY city;