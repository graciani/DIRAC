-- $Header $

--------------------------------------------------------------------------------
--
--  Schema definition for the ProxyRepositoryDB database - containing the job status
--  history ( logging ) information
---
--------------------------------------------------------------------------------

DROP DATABASE IF EXISTS ProxyRepositoryDB;

CREATE DATABASE ProxyRepositoryDB;

--------------------------------------------------------------------------------
-- Database owner definition
--#TODO: Delete after complete migration to new proxy style
USE mysql;
DELETE FROM user WHERE user='Dirac';

--
-- Must set passwords for database user by replacing "must_be_set".
--

GRANT SELECT,INSERT,LOCK TABLES,UPDATE,DELETE,CREATE,DROP,ALTER ON ProxyRepositoryDB.* TO Dirac@localhost IDENTIFIED BY 'must_be_set';
GRANT SELECT,INSERT,LOCK TABLES,UPDATE,DELETE,CREATE,DROP,ALTER ON ProxyRepositoryDB.* TO Dirac@'%' IDENTIFIED BY 'must_be_set';

FLUSH PRIVILEGES;

-------------------------------------------------------------------------------
USE ProxyRepositoryDB;

--------------------------------------------------------------------------------
DROP TABLE IF EXISTS Proxies;
CREATE TABLE Proxies (
    UserDN VARCHAR(255) NOT NULL,
    UserGroup VARCHAR(128) NOT NULL DEFAULT '/lhcb',
    Proxy BLOB NOT NULL,
    ExpirationTime DATETIME,
    ProxyType VARCHAR(32) NOT NULL DEFAULT 'Unknown',
    ProxyAttributes VARCHAR(255),
    PersistentFlag ENUM ('True','False') NOT NULL DEFAULT 'True',
    PRIMARY KEY (UserDN, UserGroup)
);

