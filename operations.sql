DROP FUNCTION IF EXISTS GetMissionDurationYears;
DROP FUNCTION IF EXISTS GetResearcherEmail;
DROP FUNCTION IF EXISTS DiscoveryCountByResearcher;

DELIMITER $$

CREATE FUNCTION GetMissionDurationYears(launch_date DATE)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN TIMESTAMPDIFF(YEAR, launch_date, CURDATE());
END$$

CREATE FUNCTION GetResearcherEmail(rid INT)
RETURNS VARCHAR(255)
DETERMINISTIC
BEGIN
    DECLARE user_part VARCHAR(100);
    DECLARE domain_part VARCHAR(100);
        SELECT email_name, email_domain INTO user_part, domain_part
    FROM Email
    WHERE researcher_id = rid
    LIMIT 1;
    RETURN CONCAT(user_part, '@', domain_part);
END$$

CREATE FUNCTION DiscoveryCountByResearcher(rid INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT DEFAULT 0;
    SELECT COUNT(*) INTO total
    FROM Discoveries
    WHERE researcher_id = rid;
    RETURN total;
END$$

DELIMITER ;

DROP TRIGGER IF EXISTS SplitFullName;
DROP TRIGGER IF EXISTS PreventMissionDelete;
DROP TRIGGER IF EXISTS LogObservationUpdate;

DELIMITER $$

CREATE TRIGGER SplitFullName
AFTER INSERT ON Researchers
FOR EACH ROW
BEGIN
    INSERT INTO Full_name (researcher_id, first_name, last_name)
    VALUES (
        NEW.researcher_id,
        SUBSTRING_INDEX(REPLACE(NEW.full_name, 'Dr. ', ''), ' ', 1),
        SUBSTRING_INDEX(REPLACE(NEW.full_name, 'Dr. ', ''), ' ', -1)
    );
END$$

CREATE TRIGGER PreventMissionDelete
BEFORE DELETE ON Missions
FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*) FROM Discoveries WHERE mission_id = OLD.mission_id) > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Cannot delete mission with existing discoveries.';
    END IF;
END$$


DELIMITER ;

DROP PROCEDURE IF EXISTS AddDiscovery;
DROP PROCEDURE IF EXISTS RegisterResearcher;
DROP PROCEDURE IF EXISTS GetObjectReport;

DELIMITER $$

CREATE PROCEDURE AddDiscovery(
    IN d_id INT,
    IN m_id INT,
    IN o_id INT,
    IN r_id INT,
    IN d_date DATE
)
BEGIN
    IF EXISTS (
        SELECT 1 FROM Discoveries
        WHERE mission_id = m_id AND object_id = o_id AND researcher_id = r_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Duplicate discovery record.';
    ELSE
        INSERT INTO Discoveries (discovery_id, mission_id, object_id, researcher_id, discovery_date)
        VALUES (d_id, m_id, o_id, r_id, d_date);
    END IF;
END$$

CREATE PROCEDURE GetObjectReport(IN objid INT)
BEGIN
    SELECT 
        c.name AS Object_Name,
        c.type AS Object_Type,
        c.distance,
        c.mass,
        c.radius,
        o.parameter,
        o.value
    FROM Celestial_objects c
    JOIN Observation_data o ON c.object_id = o.object_id
    WHERE c.object_id = objid;
END$$

DELIMITER ;

