CREATE TABLE drivers (
  id SERIAL PRIMARY KEY,
  first_name VARCHAR,
  last_name VARCHAR
);

CREATE TABLE vehicles (
  id SERIAL PRIMARY KEY,
  make VARCHAR,
  model VARCHAR,
  driver_id INTEGER REFERENCES drivers(id)
);

INSERT INTO drivers (first_name, last_name) 
  VALUES ('Amy', 'Hua'),
         ('Bob', 'Dylan'),
         ('Sarah', 'Brightman'),
         ('Aditya', 'Birla');

INSERT INTO vehicles (make, model, driver_id) 
  VALUES ('Nissan', 'Altima', 4),
         ('Toyota', 'Camry', 3),
         ('Kawasaki', 'Ninja', 2),
         ('Honda', 'Civic', 1);