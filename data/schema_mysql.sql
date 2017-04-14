-- MySQL dump 10.13  Distrib 5.5.54, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: quickandcleandb
-- ------------------------------------------------------
-- Server version	5.5.54-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `quickandcleandb`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `quickandcleandb` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `quickandcleandb`;

--
-- Table structure for table `Asset`
--

DROP TABLE IF EXISTS `Asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `assetable_id` int(11) DEFAULT NULL,
  `assetable_type` varchar(30) DEFAULT NULL,
  `data_file_name` varchar(255) DEFAULT NULL,
  `data_content_type` varchar(255) DEFAULT NULL,
  `data_file_size` int(11) DEFAULT NULL,
  `asset_type` varchar(30) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_Asset_assetable_type` (`assetable_type`),
  KEY `ix_Asset_is_active` (`is_active`),
  KEY `ix_Asset_assetable_id` (`assetable_id`),
  KEY `ix_Asset_asset_type` (`asset_type`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Asset`
--

LOCK TABLES `Asset` WRITE;
/*!40000 ALTER TABLE `Asset` DISABLE KEYS */;
INSERT INTO `Asset` VALUES (1,0,'','cheikhna2016.jpg','image/jpeg',35966,'',320,320,'Avatar picture','Photo avatar',1,1492138814,1492128000),(2,0,'','avatar-systemaker-01.jpg','image/jpeg',54370,'',458,458,'logo','logo',1,1492138814,1492128000);
/*!40000 ALTER TABLE `Asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Section`
--

DROP TABLE IF EXISTS `Section`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Section` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(255) DEFAULT NULL,
  `title_en_US` varchar(255) DEFAULT NULL,
  `title_fr_FR` varchar(255) DEFAULT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_Section_title_fr_FR` (`title_fr_FR`),
  UNIQUE KEY `ix_Section_slug` (`slug`),
  KEY `ix_Section_is_active` (`is_active`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Section`
--

LOCK TABLES `Section` WRITE;
/*!40000 ALTER TABLE `Section` DISABLE KEYS */;
INSERT INTO `Section` VALUES (1,'department1','Department 1','Catégorie 1','Department 1 description','Description de la catégorie 1',1,1492138814,1492128000),(2,'department2','Department 2','Catégorie 2','Department 2 description','Description de la catégorie 2',1,1492138814,1492128000);
/*!40000 ALTER TABLE `Section` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(60) DEFAULT NULL,
  `username` varchar(60) DEFAULT NULL,
  `password_hash` varchar(128) DEFAULT NULL,
  `asset_id` int(11) DEFAULT NULL,
  `is_admin` tinyint(1) DEFAULT NULL,
  `is_owner` tinyint(1) DEFAULT NULL,
  `is_member` tinyint(1) DEFAULT NULL,
  `is_authenticated` tinyint(1) DEFAULT NULL,
  `is_anonymous` tinyint(1) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  `locale` varchar(30) DEFAULT NULL,
  `timezone` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_User_username` (`username`),
  UNIQUE KEY `ix_User_email` (`email`),
  KEY `asset_id` (`asset_id`),
  KEY `ix_User_timezone` (`timezone`),
  KEY `ix_User_locale` (`locale`),
  KEY `ix_User_is_active` (`is_active`),
  CONSTRAINT `User_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `Asset` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (1,'admin@example.com','admin@example.com','pbkdf2:sha1:1000$NaxQwKoE$e84ab2618e896e061c818da85d12ca965611076c',1,1,0,1,1,0,1,1492138814,1492128000,'en_US','UTC'),(2,'editor@example.com','editor@example.com','pbkdf2:sha1:1000$oDvgCreA$de59ac764b5149a12d9d983b934c7a3a3611f5c6',2,1,0,1,1,0,1,1492138814,1492128000,'en_US','UTC');
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usersection`
--

DROP TABLE IF EXISTS `usersection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `usersection` (
  `user_id` int(11) NOT NULL,
  `section_id` int(11) NOT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`user_id`,`section_id`),
  KEY `section_id` (`section_id`),
  CONSTRAINT `usersection_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  CONSTRAINT `usersection_ibfk_2` FOREIGN KEY (`section_id`) REFERENCES `Section` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usersection`
--

LOCK TABLES `usersection` WRITE;
/*!40000 ALTER TABLE `usersection` DISABLE KEYS */;
INSERT INTO `usersection` VALUES (1,1,NULL,NULL,1492138814,1492138814),(2,2,NULL,NULL,1492138814,1492138814);
/*!40000 ALTER TABLE `usersection` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-14  3:22:44
