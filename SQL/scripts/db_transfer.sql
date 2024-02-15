
COPY art FROM '/pls/Art.csv' DELIMITER ',' CSV HEADER;
COPY art_owner FROM '/pls/Owner.csv' DELIMITER ',' CSV HEADER;
COPY author FROM '/pls/Author.csv' DELIMITER ',' CSV HEADER;
COPY author_and_art FROM '/pls/Author_And_Art.csv' DELIMITER ',' CSV HEADER;
COPY museum FROM '/pls/Museum.csv' DELIMITER ',' CSV HEADER;
COPY museum_storage_history FROM '/pls/MuseumHistory.csv' DELIMITER ',' CSV HEADER;
COPY owner_and_art FROM '/pls/Owner_And_Art.csv' DELIMITER ',' CSV HEADER;
COPY vandalism_case FROM '/pls/VandalismCase.csv' DELIMITER ',' CSV HEADER;
COPY expertise FROM '/pls/generated/Val.csv' DELIMITER ',' CSV HEADER;