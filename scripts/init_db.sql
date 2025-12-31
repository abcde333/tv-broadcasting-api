CREATE ROLE tv_user WITH LOGIN PASSWORD '12345678';
CREATE DATABASE tv_broadcasting OWNER tv_user;
GRANT ALL PRIVILEGES ON DATABASE tv_broadcasting TO tv_user;

\c tv_broadcasting tv_user;

CREATE TABLE satellites (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    service_life INT,
    orbit_radius FLOAT
);

CREATE TABLE tv_channels (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    broadcast_language VARCHAR(20) NOT NULL,
    country VARCHAR(50) NOT NULL,
    company VARCHAR(100),
    specifics VARCHAR(255),
    metadata_json JSON
);

CREATE TABLE broadcasts (
    id SERIAL PRIMARY KEY,
    satellite_id INT REFERENCES satellites(id),
    tv_channel_id INT REFERENCES tv_channels(id),
    frequency FLOAT NOT NULL,
    coverage_from INT,
    coverage_to INT
);

CREATE INDEX idx_satellites_country ON satellites(country);
CREATE INDEX idx_tv_channels_country ON tv_channels(country);
CREATE INDEX idx_broadcasts_satellite ON broadcasts(satellite_id);
CREATE INDEX idx_broadcasts_tv_channel ON broadcasts(tv_channel_id);