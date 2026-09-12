-- CaddieOS Database Initialisation Script
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE professional_profiles (
    profile_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tour_license_id VARCHAR(50) UNIQUE NOT NULL,
    player_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE equipment_bags (
    bag_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES professional_profiles(profile_id) ON DELETE CASCADE,
    bag_name VARCHAR(100) NOT NULL,
    is_active_profile BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE club_loft_matrix (
    club_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    bag_id UUID REFERENCES equipment_bags(bag_id) ON DELETE CASCADE,
    club_identifier VARCHAR(10) NOT NULL,
    club_name VARCHAR(50) NOT NULL,
    stock_carry_yards INT NOT NULL,
    club_type VARCHAR(20) CHECK (club_type IN ('Wood', 'Hybrid', 'Iron', 'Wedge', 'Putter')),
    UNIQUE(bag_id, club_identifier)
);

CREATE TABLE courses (
    course_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_name VARCHAR(150) NOT NULL,
    location_city VARCHAR(100),
    stimpmeter_rating NUMERIC(3,1) DEFAULT 11.0
);

CREATE TABLE holes (
    hole_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    course_id UUID REFERENCES courses(course_id) ON DELETE CASCADE,
    hole_number INT NOT NULL,
    par_rating INT NOT NULL CHECK (par_rating BETWEEN 3 AND 5),
    tee_box_location GEOMETRY(Point, 4326),
    pin_target_location GEOMETRY(Point, 4326),
    green_complex_polygon GEOMETRY(Polygon, 4326),
    elevation_change_feet NUMERIC(5,2) DEFAULT 0.0,
    UNIQUE(course_id, hole_number)
);

CREATE TABLE historical_shot_logs (
    shot_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id UUID REFERENCES professional_profiles(profile_id),
    hole_id UUID REFERENCES holes(hole_id),
    club_used VARCHAR(50) NOT NULL,
    laser_distance_yards INT NOT NULL,
    calculated_plays_like_yards INT NOT NULL,
    wind_velocity_mph NUMERIC(4,2) NOT NULL,
    wind_direction_degrees INT NOT NULL,
    shot_outcome VARCHAR(100),
    fairway_in_regulation BOOLEAN DEFAULT false,
    green_in_regulation BOOLEAN DEFAULT false,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_holes_geom ON holes USING GIST(pin_target_location);
CREATE INDEX idx_green_poly ON holes USING GIST(green_complex_polygon);
CREATE INDEX idx_shot_logs_profile ON historical_shot_logs(profile_id);
