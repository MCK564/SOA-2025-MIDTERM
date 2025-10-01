-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Oct 01, 2025 at 06:01 AM
-- Server version: 8.0.28
-- PHP Version: 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `bank_auth`
--

-- --------------------------------------------------------

--
-- Table structure for table `auth`
--

CREATE TABLE `auth` (
  `id` varchar(36) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` enum('ADMIN','STUDENT') DEFAULT NULL,
  `login_type` enum('ROPC','FACEBOOK','GOOGLE') DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `auth`
--

INSERT INTO `auth` (`id`, `username`, `password`, `role`, `login_type`, `email`) VALUES
('000001', 'admin', '$2b$12$yUk.PmNP1QVpkBzAIQ.kEuo6UG437ugc/FZlGVCRIt3hq0sllqx6O', 'ADMIN', 'ROPC', 'stu03@example.com'),
('52200001', 'student01', '$2b$12$07TeX0ldy7sqQd67U74TRe3ZWcCjwvs37RnCXVqidvLAi75NL5jGy', 'STUDENT', 'ROPC', 'admin@example.com'),
('52200002', 'student02', '$2b$12$efq5Vz70LADvMRQK3AvpPelmp1s9invtJAf5SL6oP9NTucttgQkOi', 'STUDENT', 'ROPC', 'khamai05767@gmail.com'),
('52200003', 'student03', '$2b$12$b5xC2h9IrU57fZU5nuB3m.AhR89tAlwRDyRiB8eDEEX/bZsuTt8Gq', 'STUDENT', 'ROPC', 'chikha13122@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `auth`
--
ALTER TABLE `auth`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_auth_username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `ix_auth_id` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
