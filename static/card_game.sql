CREATE TABLE `users` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `username` varchar(255) UNIQUE,
  `email` varchar(255) UNIQUE,
  `password` varchar(255),
  `rating` integer DEFAULT 0,
  `scrap` integer DEFAULT 0,
  `created_at` timestamp
);

CREATE TABLE `tokens` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `user_id` bigint,
  `token` varchar(255) UNIQUE,
  `created_at` timestamp,
  `valid_until` timestamp
);

CREATE TABLE `cards` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `java_class` varchar(255) UNIQUE,
  `name` varchar(255) UNIQUE,
  `description` varchar(255),
  `image` varchar(255)
);

CREATE TABLE `builds` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `name` varchar(255),
  `user_id` bigint
);

CREATE TABLE `build_card` (
  `build_id` bigint,
  `card_id` bigint,
  `amount` int DEFAULT 1,
  PRIMARY KEY (`build_id`, `card_id`)
);

CREATE TABLE `characters` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `build_id` bigint,
  `name` varchar(255),
  `stamina` int,
  `strength` int,
  `dexterity` int,
  `intellect` int
);

ALTER TABLE `tokens` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `builds` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `build_card` ADD FOREIGN KEY (`build_id`) REFERENCES `builds` (`id`);

ALTER TABLE `build_card` ADD FOREIGN KEY (`card_id`) REFERENCES `cards` (`id`);

ALTER TABLE `characters` ADD FOREIGN KEY (`build_id`) REFERENCES `builds` (`id`);

