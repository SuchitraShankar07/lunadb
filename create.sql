DROP DATABASE IF EXISTS lunadb;
CREATE DATABASE lunadb;

use lunadb;

CREATE TABLE Missions (
    mission_id INT PRIMARY KEY,
    Name VARCHAR(100),
    launch_date DATE,
    agency VARCHAR(100)
);

CREATE TABLE Celestial_objects (
    object_id INT PRIMARY KEY,
    name VARCHAR(100),
    distance FLOAT,
    radius FLOAT,
    mass FLOAT,
    type VARCHAR(50)
);

CREATE TABLE Researchers (
    researcher_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    affiliation VARCHAR(100),
    date_of_birth DATE
);

CREATE TABLE Observation_data (
    observation_id INT NOT NULL,
    parameter VARCHAR(100),
    value FLOAT,
    object_id INT,
    PRIMARY KEY (observation_id, object_id),
    FOREIGN KEY (object_id)
        REFERENCES Celestial_objects(object_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Email (
    email_id INT NOT NULL,
    researcher_id INT,
    email_name VARCHAR(100),
    email_domain VARCHAR(100),
    PRIMARY KEY (email_id, researcher_id),
    FOREIGN KEY (researcher_id)
        REFERENCES Researchers(researcher_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Full_name (
    researcher_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    FOREIGN KEY (researcher_id)
        REFERENCES Researchers(researcher_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Discoveries (
    discovery_id INT PRIMARY KEY,
    mission_id INT,
    object_id INT,
    researcher_id INT,
    discovery_date DATE, 
    FOREIGN KEY (mission_id)
        REFERENCES Missions(mission_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (object_id)
        REFERENCES Celestial_objects(object_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (researcher_id)
        REFERENCES Researchers(researcher_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);