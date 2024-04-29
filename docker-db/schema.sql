CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `email` varchar(255) COLLATE utf8_bin NOT NULL,
    `password` varchar(255) COLLATE utf8_bin NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `timestamp` datetime NOT NULL,
  `status` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `total_paid` int NOT NULL,
  `monday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `tuesday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `wednesday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `thursday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `friday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

DROP TABLE IF EXISTS `sessions`;
CREATE TABLE `sessions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `monday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `tuesday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `wednesday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `thursday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `friday` varchar(256) COLLATE utf8mb4_bin NOT NULL,
  `total_paid` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

