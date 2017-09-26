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
-- Table structure for table `Address`
--

DROP TABLE IF EXISTS `Address`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Address` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `title_en_US` varchar(255) DEFAULT NULL,
  `title_fr_FR` varchar(255) DEFAULT NULL,
  `address_line1` varchar(255) DEFAULT NULL,
  `address_line2` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `postal_code` varchar(255) DEFAULT NULL,
  `state_region` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `country_code` varchar(255) DEFAULT NULL,
  `full` varchar(255) DEFAULT NULL,
  `time_zone` varchar(255) DEFAULT NULL,
  `latitude` decimal(9,6) NOT NULL,
  `longitude` decimal(9,6) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_Address_title_en_US` (`title_en_US`),
  UNIQUE KEY `ix_Address_title_fr_FR` (`title_fr_FR`),
  KEY `user_id` (`user_id`),
  KEY `item_id` (`item_id`),
  KEY `ix_Address_longitude` (`longitude`),
  KEY `ix_Address_type` (`type`),
  KEY `ix_Address_latitude` (`latitude`),
  KEY `ix_Address_is_active` (`is_active`),
  KEY `ix_Address_state_region` (`state_region`),
  KEY `ix_Address_address_line2` (`address_line2`),
  KEY `ix_Address_time_zone` (`time_zone`),
  KEY `ix_Address_country` (`country`),
  KEY `ix_Address_status` (`status`),
  KEY `ix_Address_city` (`city`),
  KEY `ix_Address_country_code` (`country_code`),
  KEY `ix_Address_full` (`full`),
  KEY `ix_Address_postal_code` (`postal_code`),
  KEY `ix_Address_address_line1` (`address_line1`),
  CONSTRAINT `Address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  CONSTRAINT `Address_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Address`
--

LOCK TABLES `Address` WRITE;
/*!40000 ALTER TABLE `Address` DISABLE KEYS */;
/*!40000 ALTER TABLE `Address` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Asset`
--

DROP TABLE IF EXISTS `Asset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Asset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `data_file_name` varchar(255) DEFAULT NULL,
  `data_content_type` varchar(255) DEFAULT NULL,
  `data_file_size` int(11) DEFAULT NULL,
  `asset_type` varchar(30) DEFAULT NULL,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `user_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_Asset_is_active` (`is_active`),
  KEY `ix_Asset_asset_type` (`asset_type`),
  CONSTRAINT `Asset_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Asset`
--

LOCK TABLES `Asset` WRITE;
/*!40000 ALTER TABLE `Asset` DISABLE KEYS */;
/*!40000 ALTER TABLE `Asset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Creditcard`
--

DROP TABLE IF EXISTS `Creditcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Creditcard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(30) DEFAULT NULL,
  `key_id` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `encrypted_number` text,
  `expire_month` int(11) DEFAULT NULL,
  `expire_year` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `params` text,
  `comments` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_Creditcard_first_name` (`first_name`),
  KEY `ix_Creditcard_is_active` (`is_active`),
  KEY `ix_Creditcard_status` (`status`),
  KEY `ix_Creditcard_type` (`type`),
  KEY `ix_Creditcard_last_name` (`last_name`),
  KEY `ix_Creditcard_expire_month` (`expire_month`),
  KEY `ix_Creditcard_key_id` (`key_id`),
  KEY `ix_Creditcard_expire_year` (`expire_year`),
  CONSTRAINT `Creditcard_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Creditcard`
--

LOCK TABLES `Creditcard` WRITE;
/*!40000 ALTER TABLE `Creditcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `Creditcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Event`
--

DROP TABLE IF EXISTS `Event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `title_en_US` varchar(255) DEFAULT NULL,
  `title_fr_FR` varchar(255) DEFAULT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `amount` decimal(10,2) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `address_id` int(11) DEFAULT NULL,
  `start` int(11) DEFAULT NULL,
  `end` int(11) DEFAULT NULL,
  `days` int(11) DEFAULT NULL,
  `allday` tinyint(1) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_Event_title_en_US` (`title_en_US`),
  UNIQUE KEY `ix_Event_title_fr_FR` (`title_fr_FR`),
  KEY `user_id` (`user_id`),
  KEY `item_id` (`item_id`),
  KEY `address_id` (`address_id`),
  KEY `ix_Event_type` (`type`),
  KEY `ix_Event_status` (`status`),
  KEY `ix_Event_days` (`days`),
  KEY `ix_Event_is_active` (`is_active`),
  KEY `ix_Event_start` (`start`),
  KEY `ix_Event_end` (`end`),
  KEY `ix_Event_allday` (`allday`),
  CONSTRAINT `Event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  CONSTRAINT `Event_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`),
  CONSTRAINT `Event_ibfk_3` FOREIGN KEY (`address_id`) REFERENCES `Address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Event`
--

LOCK TABLES `Event` WRITE;
/*!40000 ALTER TABLE `Event` DISABLE KEYS */;
/*!40000 ALTER TABLE `Event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Item`
--

DROP TABLE IF EXISTS `Item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `slug` varchar(255) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `title_en_US` varchar(255) DEFAULT NULL,
  `title_fr_FR` varchar(255) DEFAULT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `amount` decimal(10,2) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_Item_slug` (`slug`),
  UNIQUE KEY `ix_Item_title_fr_FR` (`title_fr_FR`),
  UNIQUE KEY `ix_Item_title_en_US` (`title_en_US`),
  KEY `user_id` (`user_id`),
  KEY `ix_Item_type` (`type`),
  KEY `ix_Item_is_active` (`is_active`),
  CONSTRAINT `Item_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Item`
--

LOCK TABLES `Item` WRITE;
/*!40000 ALTER TABLE `Item` DISABLE KEYS */;
/*!40000 ALTER TABLE `Item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Order`
--

DROP TABLE IF EXISTS `Order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(30) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `params` text,
  `comments` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `ix_Order_status` (`status`),
  KEY `ix_Order_is_active` (`is_active`),
  CONSTRAINT `Order_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Order`
--

LOCK TABLES `Order` WRITE;
/*!40000 ALTER TABLE `Order` DISABLE KEYS */;
/*!40000 ALTER TABLE `Order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Payment`
--

DROP TABLE IF EXISTS `Payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Payment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(30) DEFAULT NULL,
  `key_id` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `creditcard_id` int(11) DEFAULT NULL,
  `ip_address` varchar(255) DEFAULT NULL,
  `intent` varchar(255) DEFAULT NULL,
  `return_url` varchar(255) DEFAULT NULL,
  `cancel_url` varchar(255) DEFAULT NULL,
  `payment_method` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(255) DEFAULT NULL,
  `params` text,
  `comments` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `order_id` (`order_id`),
  KEY `creditcard_id` (`creditcard_id`),
  KEY `ix_Payment_key_id` (`key_id`),
  KEY `ix_Payment_status` (`status`),
  KEY `ix_Payment_is_active` (`is_active`),
  CONSTRAINT `Payment_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `User` (`id`),
  CONSTRAINT `Payment_ibfk_2` FOREIGN KEY (`order_id`) REFERENCES `Order` (`id`),
  CONSTRAINT `Payment_ibfk_3` FOREIGN KEY (`creditcard_id`) REFERENCES `Creditcard` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Payment`
--

LOCK TABLES `Payment` WRITE;
/*!40000 ALTER TABLE `Payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `Payment` ENABLE KEYS */;
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
  `parent_id` int(11) DEFAULT NULL,
  `title_en_US` varchar(255) DEFAULT NULL,
  `title_fr_FR` varchar(255) DEFAULT NULL,
  `description_en_US` text,
  `description_fr_FR` text,
  `is_active` tinyint(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_Section_slug` (`slug`),
  UNIQUE KEY `ix_Section_title_en_US` (`title_en_US`),
  UNIQUE KEY `ix_Section_title_fr_FR` (`title_fr_FR`),
  KEY `ix_Section_is_active` (`is_active`),
  KEY `ix_Section_parent_id` (`parent_id`),
  CONSTRAINT `Section_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `Section` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Section`
--

LOCK TABLES `Section` WRITE;
/*!40000 ALTER TABLE `Section` DISABLE KEYS */;
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
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
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
  KEY `ix_User_locale` (`locale`),
  KEY `ix_User_last_name` (`last_name`),
  KEY `ix_User_is_active` (`is_active`),
  KEY `ix_User_timezone` (`timezone`),
  KEY `ix_User_first_name` (`first_name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assetitem`
--

DROP TABLE IF EXISTS `assetitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assetitem` (
  `asset_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `options` text,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`asset_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `assetitem_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `Asset` (`id`),
  CONSTRAINT `assetitem_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assetitem`
--

LOCK TABLES `assetitem` WRITE;
/*!40000 ALTER TABLE `assetitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `assetitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `creditcard`
--

DROP TABLE IF EXISTS `creditcard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `creditcard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `status` varchar(30) DEFAULT NULL,
  `key_id` varchar(255) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `encrypted_number` text,
  `expire_month` int(11) DEFAULT NULL,
  `expire_year` int(11) DEFAULT NULL,
  `first_name` varchar(255) DEFAULT NULL,
  `last_name` varchar(255) DEFAULT NULL,
  `params` text,
  `comments` text,
  `is_active` bit(1) DEFAULT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ix_Creditcard_expire_month` (`expire_month`),
  KEY `ix_Creditcard_expire_year` (`expire_year`),
  KEY `ix_Creditcard_first_name` (`first_name`),
  KEY `ix_Creditcard_is_active` (`is_active`),
  KEY `ix_Creditcard_key_id` (`key_id`),
  KEY `ix_Creditcard_last_name` (`last_name`),
  KEY `ix_Creditcard_status` (`status`),
  KEY `ix_Creditcard_type` (`type`),
  KEY `user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `creditcard`
--

LOCK TABLES `creditcard` WRITE;
/*!40000 ALTER TABLE `creditcard` DISABLE KEYS */;
/*!40000 ALTER TABLE `creditcard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orderitem`
--

DROP TABLE IF EXISTS `orderitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orderitem` (
  `order_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `options` text,
  `unit_amount` decimal(10,2) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`order_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `orderitem_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `Order` (`id`),
  CONSTRAINT `orderitem_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orderitem`
--

LOCK TABLES `orderitem` WRITE;
/*!40000 ALTER TABLE `orderitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `orderitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sectionitem`
--

DROP TABLE IF EXISTS `sectionitem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sectionitem` (
  `section_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `options` text,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`section_id`,`item_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `sectionitem_ibfk_1` FOREIGN KEY (`section_id`) REFERENCES `Section` (`id`),
  CONSTRAINT `sectionitem_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `Item` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sectionitem`
--

LOCK TABLES `sectionitem` WRITE;
/*!40000 ALTER TABLE `sectionitem` DISABLE KEYS */;
/*!40000 ALTER TABLE `sectionitem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `useraddress`
--

DROP TABLE IF EXISTS `useraddress`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `useraddress` (
  `guest_id` int(11) NOT NULL,
  `in_address_id` int(11) NOT NULL,
  `options` text,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`guest_id`,`in_address_id`),
  KEY `in_address_id` (`in_address_id`),
  CONSTRAINT `useraddress_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `User` (`id`),
  CONSTRAINT `useraddress_ibfk_2` FOREIGN KEY (`in_address_id`) REFERENCES `Address` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `useraddress`
--

LOCK TABLES `useraddress` WRITE;
/*!40000 ALTER TABLE `useraddress` DISABLE KEYS */;
/*!40000 ALTER TABLE `useraddress` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userevent`
--

DROP TABLE IF EXISTS `userevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `userevent` (
  `guest_id` int(11) NOT NULL,
  `in_event_id` int(11) NOT NULL,
  `options` text,
  `updated_at` int(11) DEFAULT NULL,
  `created_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`guest_id`,`in_event_id`),
  KEY `in_event_id` (`in_event_id`),
  CONSTRAINT `userevent_ibfk_1` FOREIGN KEY (`guest_id`) REFERENCES `User` (`id`),
  CONSTRAINT `userevent_ibfk_2` FOREIGN KEY (`in_event_id`) REFERENCES `Event` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userevent`
--

LOCK TABLES `userevent` WRITE;
/*!40000 ALTER TABLE `userevent` DISABLE KEYS */;
/*!40000 ALTER TABLE `userevent` ENABLE KEYS */;
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
  `options` text,
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

-- Dump completed on 2017-09-26 20:43:04
