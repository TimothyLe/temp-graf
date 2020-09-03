--Temperature
SELECT 
	"temperature" 
FROM 
	"pi_system_info" 
WHERE 
	("host" = 'raspberrypi') 

--Voltage
SELECT 
	mean("voltage") 
FROM 
	"pi_system_info" 
WHERE 
	$timeFilter 
GROUP BY 
	time($__interval) 
	fill(null)

--ARM CPU Speed
SELECT 
	mean("cpu_speed") 
FROM 
	"pi_system_info" 
WHERE 
	$timeFilter 
GROUP BY 
	time($__interval) 
	fill(null)

--Core Clock
SELECT 
	mean("core_clk") 
FROM 
	"pi_system_info" 
WHERE 
	$timeFilter 
GROUP BY 
	time($__interval) 
	fill(null)
