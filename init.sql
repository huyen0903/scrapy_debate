-- init.sql

-- CREATE TABLE IF NOT EXISTS city
-- (
--     city_id VARCHAR NOT NULL,
--     city_name VARCHAR NOT NULL,
--     PRIMARY KEY (city_id)
-- );

-- CREATE TABLE IF NOT EXISTS Poster
-- (
--     poster_id INT NOT NULL,
--     name VARCHAR NOT NULL,
--     PRIMARY KEY (poster_id)
-- );

-- CREATE TABLE IF NOT EXISTS Description
-- (
--     description_id INT NOT NULL,
--     content VARCHAR NOT NULL,
--     PRIMARY KEY (description_id)
-- );

-- CREATE TABLE IF NOT EXISTS District
-- (
--     district_id VARCHAR NOT NULL,
--     district_name VARCHAR NOT NULL,
--     city_id VARCHAR NOT NULL,
--     PRIMARY KEY (district_id),
--     FOREIGN KEY (city_id) REFERENCES City(city_id)
-- );

-- CREATE TABLE IF NOT EXISTS Ward
-- (
--     ward_id VARCHAR NOT NULL,
--     ward_name VARCHAR NOT NULL,
--     district_id VARCHAR NOT NULL,
--     PRIMARY KEY (ward_id),
--     FOREIGN KEY (district_id) REFERENCES District(district_id)
-- );

-- CREATE TABLE IF NOT EXISTS Street
-- (
--     street_id VARCHAR NOT NULL,
--     street_name VARCHAR NOT NULL,
--     ward_id VARCHAR NOT NULL,
--     PRIMARY KEY (street_id),
--     FOREIGN KEY (ward_id) REFERENCES Ward(ward_id)
-- );

-- CREATE TABLE IF NOT EXISTS Amenity_Category
-- (
--     category_id VARCHAR NOT NULL,
--     category_name VARCHAR NOT NULL,
--     PRIMARY KEY (category_id)
-- );

CREATE TABLE IF NOT EXISTS house
(
    house_id VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    num_bedrooms INT NOT NULL,
    num_toilets INT NOT NULL,
    room_area INT NOT NULL,
    city VARCHAR NOT NULL,
    district VARCHAR NOT NULL,
    ward VARCHAR NOT NULL,
    street VARCHAR NOT NULL,
    PRIMARY KEY (house_id)
);

CREATE TABLE IF NOT EXISTS post
(
    post_id VARCHAR NOT NULL,
    views INT NOT NULL,
    type_listing VARCHAR NOT NULL,
    rental_price INT NOT NULL,
    title VARCHAR NOT NULL,
    poster VARCHAR NOT NULL, 
    content TEXT NOT NULL,
    house_id VARCHAR NOT NULL,  -- Thêm cột house_id
    PRIMARY KEY (post_id),
    FOREIGN KEY (house_id) REFERENCES house(house_id)  -- Định nghĩa khóa ngoại
);

CREATE TABLE IF NOT EXISTS amenity
(
    amenity_id VARCHAR NOT NULL,
    amenity_name VARCHAR NOT NULL,
    amenity_category VARCHAR NOT NULL,
    PRIMARY KEY (amenity_id)
);

CREATE TABLE IF NOT EXISTS post_amenity
(
    post_id VARCHAR NOT NULL,
    amenity_id VARCHAR NOT NULL,
    amenity_name VARCHAR NOT NULL,
    PRIMARY KEY (post_id, amenity_id),
    FOREIGN KEY (post_id) REFERENCES Post(post_id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity(amenity_id)
);
