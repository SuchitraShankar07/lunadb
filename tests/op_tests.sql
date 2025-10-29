SELECT Name, GetMissionDurationYears(launch_date) AS Mission_Duration_Years
FROM Missions
ORDER BY Mission_Duration_Years DESC
LIMIT 5;

SELECT researcher_id, GetResearcherEmail(researcher_id) AS Email_Address
FROM Researchers
LIMIT 5;

SELECT r.full_name, DiscoveryCountByResearcher(r.researcher_id) AS Total_Discoveries
FROM Researchers r
ORDER BY Total_Discoveries DESC
LIMIT 5;

INSERT INTO Researchers (researcher_id, full_name, affiliation, date_of_birth)
VALUES (300, 'Dr. Alice Newton', 'NASA', '1990-04-05');
SELECT * FROM Full_name WHERE researcher_id = 300;

DELETE FROM Missions WHERE mission_id = 1;

INSERT INTO Missions VALUES (99, 'Test Mission', '2025-01-01', 'TestAgency');
DELETE FROM Missions WHERE mission_id = 99;
SELECT * FROM Missions WHERE mission_id = 99;

UPDATE Observation_data 
SET value = value + 1
WHERE observation_id = 501;

SELECT * FROM Observation_Log WHERE observation_id = 501
ORDER BY modified_at DESC;

CALL AddDiscovery(500, 12, 101, 300, '2025-10-28');
SELECT * FROM Discoveries WHERE discovery_id = 500;

CALL AddDiscovery(500, 12, 101, 300, '2025-10-28');

CALL RegisterResearcher(301, 'Robert', 'King', 'ESA', '1988-06-18', 'robert.king', 'esa.int');

SELECT * FROM Researchers WHERE researcher_id = 301;
SELECT * FROM Full_name WHERE researcher_id = 301;
SELECT * FROM Email WHERE researcher_id = 301;

CALL GetObjectReport(101);

SELECT c.name AS Exoplanet, d.discovery_date, m.name AS Mission, r.full_name
FROM Discoveries d
JOIN Celestial_objects c ON d.object_id = c.object_id
JOIN Missions m ON d.mission_id = m.mission_id
JOIN Researchers r ON d.researcher_id = r.researcher_id
WHERE c.type = 'Exoplanet' AND d.discovery_date > '2015-01-01'
ORDER BY d.discovery_date;

SELECT r.full_name, COUNT(d.discovery_id) AS total_discoveries
FROM Researchers r
JOIN Discoveries d ON r.researcher_id = d.researcher_id
GROUP BY r.researcher_id
HAVING COUNT(d.discovery_id) > 2
ORDER BY total_discoveries DESC;

SELECT m.name AS Mission, COUNT(DISTINCT d.object_id) AS Objects_Discovered
FROM Missions m
LEFT JOIN Discoveries d ON m.mission_id = d.mission_id
GROUP BY m.mission_id
ORDER BY Objects_Discovered DESC;
