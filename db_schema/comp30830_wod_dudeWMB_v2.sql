-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: comp30830-wod.cndmh0rmccxq.eu-west-1.rds.amazonaws.com    Database: dudeWMB
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `import_log`
--

DROP TABLE IF EXISTS `import_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `import_log` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `jcdecaux` json DEFAULT NULL,
  `openweather` json DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Import Log for JSON from API: Testing';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `import_log`
--

LOCK TABLES `import_log` WRITE;
/*!40000 ALTER TABLE `import_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `import_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `station`
--

DROP TABLE IF EXISTS `station`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `station` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `number` int DEFAULT NULL,
  `contractName` varchar(45) DEFAULT NULL,
  `stationName` varchar(45) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `address` varchar(60) DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `banking` tinyint(1) DEFAULT NULL,
  `bonus` tinyint(1) DEFAULT NULL,
  `lastUpdate` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  UNIQUE KEY `Number_Contract` (`number`,`contractName`) COMMENT 'The Station Number and contract name are the primary identifiers on JCDecaux'
) ENGINE=InnoDB AUTO_INCREMENT=111 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='First Draft of Station Data: Most likely for storage, may need duplicate but all in JSON for API';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `station`
--

LOCK TABLES `station` WRITE;
/*!40000 ALTER TABLE `station` DISABLE KEYS */;
INSERT INTO `station` VALUES (1,42,'dublin','SMITHFIELD NORTH','Smithfield North',53.3496,-6.2782,0,0,NULL),(2,30,'dublin','PARNELL SQUARE NORTH','Parnell Square North',53.3535,-6.26531,0,0,NULL),(3,54,'dublin','CLONMEL STREET','Clonmel Street',53.336,-6.26298,0,0,NULL),(4,108,'dublin','AVONDALE ROAD','Avondale Road',53.3594,-6.27614,0,0,NULL),(5,56,'dublin','MOUNT STREET LOWER','Mount Street Lower',53.338,-6.24153,0,0,NULL),(6,6,'dublin','CHRISTCHURCH PLACE','Christchurch Place',53.3434,-6.27012,0,0,NULL),(7,18,'dublin','GRANTHAM STREET','Grantham Street',53.3341,-6.26544,0,0,NULL),(8,32,'dublin','PEARSE STREET','Pearse Street',53.3443,-6.25043,0,0,NULL),(9,52,'dublin','YORK STREET EAST','York Street East',53.3388,-6.262,0,0,NULL),(10,48,'dublin','EXCISE WALK','Excise Walk',53.3478,-6.24424,0,0,NULL),(11,13,'dublin','FITZWILLIAM SQUARE WEST','Fitzwilliam Square West',53.3361,-6.25282,0,0,NULL),(12,43,'dublin','PORTOBELLO ROAD','Portobello Road',53.3301,-6.26804,0,0,NULL),(13,31,'dublin','PARNELL STREET','Parnell Street',53.3509,-6.26512,0,0,NULL),(14,98,'dublin','FREDERICK STREET SOUTH','Frederick Street South',53.3415,-6.25685,0,0,NULL),(15,23,'dublin','CUSTOM HOUSE','Custom House',53.3483,-6.25466,0,0,NULL),(16,106,'dublin','RATHDOWN ROAD','Rathdown Road',53.3589,-6.28034,0,0,NULL),(17,112,'dublin','NORTH CIRCULAR ROAD (O\'CONNELL\'S)','North Circular Road (O\'Connell\'s)',53.3578,-6.25156,0,0,NULL),(18,68,'dublin','HANOVER QUAY','Hanover Quay',53.3441,-6.23715,0,0,NULL),(19,74,'dublin','OLIVER BOND STREET','Oliver Bond Street',53.3439,-6.28053,0,0,NULL),(20,87,'dublin','COLLINS BARRACKS MUSEUM','Collins Barracks Museum',53.3475,-6.28525,0,0,NULL),(21,84,'dublin','BROOKFIELD ROAD','Brookfield Road',53.339,-6.30022,0,0,NULL),(22,90,'dublin','BENSON STREET','Benson Street',53.3442,-6.23345,0,0,NULL),(23,11,'dublin','EARLSFORT TERRACE','Earlsfort Terrace',53.3343,-6.2585,0,0,NULL),(24,17,'dublin','GOLDEN LANE','Golden Lane',53.3408,-6.26773,0,0,NULL),(25,45,'dublin','DEVERELL PLACE','Deverell Place',53.3515,-6.25527,0,0,NULL),(26,114,'dublin','WILTON TERRACE (PARK)','Wilton Terrace (Park)',53.3337,-6.24834,0,0,NULL),(27,72,'dublin','JOHN STREET WEST','John Street West',53.3431,-6.27717,0,0,NULL),(28,63,'dublin','FENIAN STREET','Fenian Street',53.3414,-6.24672,0,0,NULL),(29,113,'dublin','MERRION SQUARE SOUTH','Merrion Square South',53.3386,-6.24861,0,0,NULL),(30,91,'dublin','SOUTH DOCK ROAD','South Dock Road',53.3418,-6.23129,0,0,NULL),(31,99,'dublin','CITY QUAY','City Quay',53.3466,-6.24615,0,0,NULL),(32,9,'dublin','EXCHEQUER STREET','Exchequer Street',53.343,-6.26358,0,0,NULL),(33,67,'dublin','THE POINT','The Point',53.3469,-6.23085,0,0,NULL),(34,116,'dublin','BROADSTONE','Broadstone',53.3547,-6.27231,0,0,NULL),(35,55,'dublin','HATCH STREET','Hatch Street',53.334,-6.26071,0,0,NULL),(36,62,'dublin','LIME STREET','Lime Street',53.346,-6.24358,0,0,NULL),(37,5,'dublin','CHARLEMONT PLACE','Charlemont Street',53.3307,-6.26018,0,0,NULL),(38,97,'dublin','KILMAINHAM GAOL','Kilmainham Gaol',53.3421,-6.31002,0,0,NULL),(39,61,'dublin','HARDWICKE PLACE','Hardwicke Place',53.357,-6.26323,0,0,NULL),(40,77,'dublin','WOLFE TONE STREET','Wolfe Tone Street',53.3489,-6.26746,0,0,NULL),(41,73,'dublin','FRANCIS STREET','Francis Street',53.3421,-6.27523,0,0,NULL),(42,4,'dublin','GREEK STREET','Greek Street',53.3469,-6.27298,0,0,NULL),(43,49,'dublin','GUILD STREET','Guild Street',53.3479,-6.24093,0,0,NULL),(44,19,'dublin','HERBERT PLACE','Herbert Place',53.3344,-6.24557,0,0,NULL),(45,7,'dublin','HIGH STREET','High Street',53.3436,-6.27507,0,0,NULL),(46,60,'dublin','NORTH CIRCULAR ROAD','North Circular Road',53.3596,-6.26035,0,0,NULL),(47,102,'dublin','WESTERN WAY','Western Way',53.3549,-6.26942,0,0,NULL),(48,38,'dublin','TALBOT STREET','Talbot Street',53.351,-6.25294,0,0,NULL),(49,53,'dublin','NEWMAN HOUSE','Newman House',53.3371,-6.26059,0,0,NULL),(50,58,'dublin','SIR PATRICK DUN\'S','Sir Patrick\'s Dun',53.3392,-6.24064,0,0,NULL),(51,66,'dublin','NEW CENTRAL BANK','New Central Bank',53.3471,-6.23475,0,0,NULL),(52,104,'dublin','GRANGEGORMAN LOWER (CENTRAL)','Grangegorman Lower (Central)',53.3552,-6.27842,0,0,NULL),(53,101,'dublin','KING STREET NORTH','King Street North',53.3503,-6.27351,0,0,NULL),(54,115,'dublin','KILLARNEY STREET','Killarney Street',53.3548,-6.24758,0,0,NULL),(55,47,'dublin','HERBERT STREET','Herbert Street',53.3357,-6.24551,0,0,NULL),(56,117,'dublin','HANOVER QUAY EAST','Hanover Quay East',53.3437,-6.23175,0,0,NULL),(57,8,'dublin','CUSTOM HOUSE QUAY','Custom House Quay',53.3479,-6.24805,0,0,NULL),(58,27,'dublin','MOLESWORTH STREET','Molesworth Street',53.3413,-6.25812,0,0,NULL),(59,16,'dublin','GEORGES QUAY','Georges Quay',53.3475,-6.25219,0,0,NULL),(60,96,'dublin','KILMAINHAM LANE','Kilmainham Lane',53.3418,-6.30509,0,0,NULL),(61,82,'dublin','MOUNT BROWN','Mount Brown',53.3416,-6.29719,0,0,NULL),(62,76,'dublin','MARKET STREET SOUTH','Market Street South',53.3423,-6.28766,0,0,NULL),(63,71,'dublin','KEVIN STREET','Kevin Street',53.3378,-6.2677,0,0,NULL),(64,79,'dublin','ECCLES STREET EAST','Eccles Street East',53.3581,-6.2656,0,0,NULL),(65,69,'dublin','GRAND CANAL DOCK','Grand Canal Dock',53.3426,-6.2387,0,0,NULL),(66,25,'dublin','MERRION SQUARE EAST','Merrion Square East',53.3394,-6.24655,0,0,NULL),(67,51,'dublin','YORK STREET WEST','York Street West',53.3393,-6.2647,0,0,NULL),(68,37,'dublin','ST. STEPHEN\'S GREEN SOUTH','St. Stephen\'s Green South',53.3375,-6.26199,1,0,NULL),(69,59,'dublin','DENMARK STREET GREAT','Denmark Street Great',53.3556,-6.2614,0,0,NULL),(70,95,'dublin','ROYAL HOSPITAL','Royal Hospital',53.3439,-6.29706,0,0,NULL),(71,94,'dublin','HEUSTON STATION (CAR PARK)','Heuston Station (Car Park)',53.347,-6.2978,0,0,NULL),(72,105,'dublin','GRANGEGORMAN LOWER (NORTH)','Grangegorman Lower (North)',53.356,-6.27838,0,0,NULL),(73,36,'dublin','ST. STEPHEN\'S GREEN EAST','St. Stephen\'s Green East',53.3378,-6.25603,0,0,NULL),(74,93,'dublin','HEUSTON STATION (CENTRAL)','Heuston Station (Central)',53.3466,-6.29692,0,0,NULL),(75,22,'dublin','TOWNSEND STREET','Townsend Street',53.3459,-6.25461,0,0,NULL),(76,50,'dublin','GEORGES LANE','George\'s Lane',53.3502,-6.2797,0,0,NULL),(77,110,'dublin','PHIBSBOROUGH ROAD','Phibsborough Road',53.3563,-6.27372,0,0,NULL),(78,12,'dublin','ECCLES STREET','Eccles Street',53.3592,-6.26978,0,0,NULL),(79,34,'dublin','PORTOBELLO HARBOUR','Portobello Harbour',53.3304,-6.26516,0,0,NULL),(80,78,'dublin','MATER HOSPITAL','Mater Hospital',53.36,-6.26483,0,0,NULL),(81,2,'dublin','BLESSINGTON STREET','Blessington Street',53.3568,-6.26814,0,0,NULL),(82,75,'dublin','JAMES STREET','James Street',53.3435,-6.28741,0,0,NULL),(83,111,'dublin','MOUNTJOY SQUARE EAST','Mountjoy Square East',53.3567,-6.25636,0,0,NULL),(84,26,'dublin','MERRION SQUARE WEST','Merrion Square West',53.3398,-6.25199,1,0,NULL),(85,65,'dublin','CONVENTION CENTRE','Convention Centre',53.3474,-6.23852,1,0,NULL),(86,15,'dublin','HARDWICKE STREET','Hardwicke Street',53.3555,-6.26442,0,0,NULL),(87,86,'dublin','PARKGATE STREET','Parkgate Street',53.348,-6.2918,0,0,NULL),(88,10,'dublin','DAME STREET','Dame Street',53.344,-6.2668,1,0,NULL),(89,100,'dublin','HEUSTON BRIDGE (SOUTH)','Heuston Bridge (South)',53.3471,-6.29204,0,0,NULL),(90,24,'dublin','CATHAL BRUGHA STREET','Cathal Brugha Street',53.3521,-6.26053,0,0,NULL),(91,64,'dublin','SANDWITH STREET','Sandwith Street',53.3452,-6.24716,0,0,NULL),(92,109,'dublin','BUCKINGHAM STREET LOWER','Buckingham Street Lower',53.3533,-6.24932,0,0,NULL),(93,85,'dublin','ROTHE ABBEY','Rothe Abbey',53.3388,-6.30395,0,0,NULL),(94,107,'dublin','CHARLEVILLE ROAD','Charleville Road',53.3592,-6.28187,0,0,NULL),(95,33,'dublin','PRINCES STREET / O\'CONNELL STREET','Princes Street / O\'Connell Street',53.349,-6.26031,1,0,NULL),(96,44,'dublin','UPPER SHERRARD STREET','Upper Sherrard Street',53.3584,-6.26064,0,0,NULL),(97,89,'dublin','FITZWILLIAM SQUARE EAST','Fitzwilliam Square East',53.3352,-6.2509,0,0,NULL),(98,57,'dublin','GRATTAN STREET','Grattan Street',53.3396,-6.24378,0,0,NULL),(99,80,'dublin','ST JAMES HOSPITAL (LUAS)','St James Hospital (Luas)',53.3414,-6.29295,0,0,NULL),(100,41,'dublin','HARCOURT TERRACE','Harcourt Terrace',53.3328,-6.25794,0,0,NULL),(101,3,'dublin','BOLTON STREET','Bolton Street',53.3512,-6.26986,0,0,NULL),(102,40,'dublin','JERVIS STREET','Jervis Street',53.3483,-6.26665,0,0,NULL),(103,29,'dublin','ORMOND QUAY UPPER','Ormond Quay Upper',53.3461,-6.268,0,0,NULL),(104,103,'dublin','GRANGEGORMAN LOWER (SOUTH)','Grangegorman Lower (South)',53.3547,-6.27868,0,0,NULL),(105,28,'dublin','MOUNTJOY SQUARE WEST','Mountjoy Square West',53.3563,-6.25859,0,0,NULL),(106,39,'dublin','WILTON TERRACE','Wilton Terrace',53.3324,-6.25272,0,0,NULL),(107,83,'dublin','EMMET ROAD','Emmet Road',53.3407,-6.30819,0,0,NULL),(108,92,'dublin','HEUSTON BRIDGE (NORTH)','Heuston Bridge (North)',53.3478,-6.29243,0,0,NULL),(109,21,'dublin','LEINSTER STREET SOUTH','Leinster Street South',53.3422,-6.25449,0,0,NULL),(110,88,'dublin','BLACKHALL PLACE','Blackhall Place',53.3488,-6.28164,0,0,NULL);
/*!40000 ALTER TABLE `station` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stationState`
--

DROP TABLE IF EXISTS `stationState`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stationState` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `stationId` int NOT NULL,
  `status` varchar(45) DEFAULT NULL,
  `bike_stands` int DEFAULT NULL,
  `available_bike_stands` int DEFAULT NULL,
  `available_bikes` int DEFAULT NULL,
  `lastUpdate` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`),
  KEY `fk_stationState_station` (`stationId`),
  CONSTRAINT `fk_stationState_station` FOREIGN KEY (`stationId`) REFERENCES `station` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='First Draft of Station Data: Most likely for storage, may need duplicate but all in JSON for API';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stationState`
--

LOCK TABLES `stationState` WRITE;
/*!40000 ALTER TABLE `stationState` DISABLE KEYS */;
/*!40000 ALTER TABLE `stationState` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weatherHistory`
--

DROP TABLE IF EXISTS `weatherHistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weatherHistory` (
  `weatherTime` datetime NOT NULL,
  `latitude` float NOT NULL,
  `longitude` float NOT NULL,
  `main` varchar(45) DEFAULT NULL,
  `description` varchar(256) DEFAULT NULL,
  `temp` float DEFAULT NULL,
  `feels_like` float DEFAULT NULL,
  `temp_min` float DEFAULT NULL,
  `temp_max` float DEFAULT NULL,
  `pressure` int DEFAULT NULL,
  `humidity` int DEFAULT NULL,
  `sea_level` int DEFAULT NULL,
  `grnd_level` int DEFAULT NULL,
  `wind_speed` float DEFAULT NULL,
  `wind_deg` int DEFAULT NULL,
  `wind_gust` float DEFAULT NULL,
  `clouds_all` int DEFAULT NULL,
  PRIMARY KEY (`weatherTime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weatherHistory`
--

LOCK TABLES `weatherHistory` WRITE;
/*!40000 ALTER TABLE `weatherHistory` DISABLE KEYS */;
/*!40000 ALTER TABLE `weatherHistory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'dudeWMB'
--

--
-- Dumping routines for database 'dudeWMB'
--
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-02-18  9:25:05
