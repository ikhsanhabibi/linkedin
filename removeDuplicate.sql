use indeed;

CREATE TABLE temp LIKE indeed;
INSERT INTO temp
    SELECT DISTINCT * FROM indeed;
DROP TABLE indeed;
RENAME TABLE temp TO indeed;