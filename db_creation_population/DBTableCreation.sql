CREATE TABLE `dog_animations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `animation_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=ascii;

CREATE TABLE `ethnicities` (
  `eth_id` int NOT NULL AUTO_INCREMENT,
  `eth_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`eth_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=ascii;

CREATE TABLE `familiarity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `familiarity_description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=ascii COMMENT='familiarities from completely unfamiliar to expert';

CREATE TABLE `game_data` (
  `data_key` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `user_input` varchar(255) DEFAULT NULL,
  `animation` int DEFAULT NULL,
  `input_is_correct` tinyint DEFAULT NULL,
  `event_time` datetime(3) DEFAULT NULL,
  PRIMARY KEY (`data_key`),
  KEY `user_id` (`user_id`),
  KEY `game_data_ibfk_2_idx` (`animation`),
  KEY `game_data_ibfk_3_idx` (`user_input`),
  CONSTRAINT `game_data_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `player_access` (`user_id`),
  CONSTRAINT `game_data_ibfk_2` FOREIGN KEY (`animation`) REFERENCES `dog_animations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=335 DEFAULT CHARSET=ascii;

CREATE TABLE `player_access` (
  `access_key` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `access_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  PRIMARY KEY (`access_key`),
  KEY `idx_player_access_user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=ascii;

CREATE TABLE `player_demographics` (
  `user_id` int NOT NULL,
  `age` int DEFAULT NULL,
  `eth_id` int DEFAULT NULL,
  `gender` varchar(255) DEFAULT NULL,
  `game_familiarity` int DEFAULT NULL,
  `dog_familiarity` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `eth_id` (`eth_id`),
  KEY `player_demographics_ibfk_3_idx` (`game_familiarity`),
  KEY `player_demographics_ibfk_4_idx` (`dog_familiarity`),
  CONSTRAINT `player_demographics_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `player_access` (`user_id`),
  CONSTRAINT `player_demographics_ibfk_2` FOREIGN KEY (`eth_id`) REFERENCES `ethnicities` (`eth_id`),
  CONSTRAINT `player_demographics_ibfk_3` FOREIGN KEY (`game_familiarity`) REFERENCES `familiarity` (`id`),
  CONSTRAINT `player_demographics_ibfk_4` FOREIGN KEY (`dog_familiarity`) REFERENCES `familiarity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=ascii;
