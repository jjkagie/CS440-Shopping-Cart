-- Create Database Start
CREATE DATABASE ShoppingDB;
USE ShoppingDB;

-- GRANT ALL PRIVILEGES ON ShoppingDB.* TO 'msv68'@'localhost';

CREATE TABLE Account
	( username VARCHAR(64) PRIMARY KEY, 
      password VARCHAR(64)
	);
DESCRIBE Account;

CREATE TABLE ShoppingCart
	( id VARCHAR(64),  
      PRIMARY KEY(id), 
      FOREIGN KEY(id) REFERENCES Account(username)
	);
DESCRIBE ShoppingCart;

CREATE TABLE Item
	( id int, 
      item_name VARCHAR(64), 
      item_source VARCHAR(256), 
      PRIMARY KEY( id )
	);
DESCRIBE Item;

CREATE TABLE ItemSelection
	( item_id int, 
      cart_id VARCHAR(64), 
      quantity int, 
      PRIMARY KEY (item_id, cart_id), 
      FOREIGN KEY (item_id) REFERENCES Item(id), 
      FOREIGN KEY (cart_id) REFERENCES ShoppingCart(id)
	);
DESCRIBE ItemSelection;
SHOW TABLES;
-- Create Database End

-- Delete Database Start
DROP TABLE ItemSelection;
DROP TABLE Item;
DROP TABLE ShoppingCart;
DROP TABLE Account;
-- Delete Database End

-- Empty Database Start
SET SQL_SAFE_UPDATES = 0;
DELETE FROM ItemSelection;
DELETE FROM Item;
DELETE FROM ShoppingCart;
DELETE FROM Account;
SET SQL_SAFE_UPDATES = 1;
-- Empty Database End





-- DAO.Load()
-- Get data to load Account DAO using username and password
SELECT * FROM Account WHERE username="<username>" AND password="<password>";
	-- password will be treated as a key for write access
-- Get data to load Cart DAO using Account DAO
SELECT * FROM ShoppingCart WHERE id="<username>";
-- Get data to load ItemSelections DAO using ShoppingCart DAO
SELECT * FROM ItemSelection WHERE cart_id="<username>";
-- Get data to load Item DAO using ItemSelection DAO
SELECT * FROM ITEM WHERE id="<ID#>";

-- DAO.Create()
-- INSERT INTO <TABLE_NAME> VALUES <VALUES>
--   (VALUES are the keys and values shown in DAO.Load)

-- DAO.Update()
-- UPDATE <TableName> SET <VALUES> WHERE <CONDITIONS>
--   (CONDITIONS are the keys shown in DAO.Load)
--   (VALUES are the values shown in DAO.Load)

-- DAO.Remove()
-- DELETE FROM <TABLE_NAME> WHERE <CONDITIONS>;
--   (CONDITIONS are the keys shown in DAO.Load)
