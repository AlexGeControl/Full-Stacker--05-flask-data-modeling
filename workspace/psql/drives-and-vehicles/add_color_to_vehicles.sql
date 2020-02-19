ALTER TABLE vehicles 
ADD COLUMN color VARCHAR;


UPDATE vehicles
SET color = 'Red'
WHERE
   ID = 1;
 
UPDATE vehicles
SET color = 'Black'
WHERE
   ID = 2;
 
UPDATE vehicles
SET color = 'Black'
WHERE
   ID = 3;

UPDATE vehicles
SET color = 'Red'
WHERE
   ID = 4;


ALTER TABLE vehicles
ALTER COLUMN color SET NOT NULL;