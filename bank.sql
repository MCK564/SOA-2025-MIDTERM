-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- Generation Time: Aug 29, 2025 at 07:09 AM
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
-- Database: `bank`
--

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int NOT NULL,
  `amount` double NOT NULL,
  `status` enum('SUCCESS','FAILED') DEFAULT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `tuition_id` int DEFAULT NULL,
  `date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tuitions`
--

CREATE TABLE `tuitions` (
  `id` int NOT NULL,
  `student_id` varchar(36) DEFAULT NULL,
  `payer_id` varchar(36) DEFAULT NULL,
  `amount` double NOT NULL,
  `status` enum('NOT_YET_PAID','PAID','EXPIRED','IN_PROCESS') DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `expires_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `tuitions`
--

INSERT INTO `tuitions` (`id`, `student_id`, `payer_id`, `amount`, `status`, `description`, `expires_at`) VALUES
(1, '52200001', '52200001', 15000000, 'PAID', 'Tuition Semester 1 (2022-2023)', '2023-01-15 23:59:59'),
(2, '52200001', '52200001', 16000000, 'PAID', 'Tuition Semester 2 (2022-2023)', '2023-06-30 23:59:59'),
(3, '52200001', NULL, 16500000, 'EXPIRED', 'Tuition Semester 1 (2023-2024)', '2023-12-31 23:59:59'),
(4, '52200001', NULL, 17000000, 'IN_PROCESS', 'Tuition Semester 2 (2023-2024)', '2024-06-30 23:59:59'),
(5, '52200001', NULL, 17500000, 'NOT_YET_PAID', 'Tuition Semester 1 (2024-2025)', '2024-12-31 23:59:59'),
(6, '52200002', '52200002', 15000000, 'PAID', 'Tuition Semester 1 (2022-2023)', '2023-01-15 23:59:59'),
(7, '52200002', NULL, 16000000, 'EXPIRED', 'Tuition Semester 2 (2022-2023)', '2023-06-30 23:59:59'),
(8, '52200002', '52200002', 16500000, 'PAID', 'Tuition Semester 1 (2023-2024)', '2023-12-31 23:59:59'),
(9, '52200002', NULL, 17000000, 'IN_PROCESS', 'Tuition Semester 2 (2023-2024)', '2024-06-30 23:59:59'),
(10, '52200002', NULL, 17500000, 'NOT_YET_PAID', 'Tuition Semester 1 (2024-2025)', '2024-12-31 23:59:59'),
(11, '52200003', '52200003', 15000000, 'PAID', 'Tuition Semester 1 (2022-2023)', '2023-01-15 23:59:59'),
(12, '52200003', '52200003', 16000000, 'PAID', 'Tuition Semester 2 (2022-2023)', '2023-06-30 23:59:59'),
(13, '52200003', '52200003', 16500000, 'PAID', 'Tuition Semester 1 (2023-2024)', '2023-12-31 23:59:59'),
(14, '52200003', NULL, 17000000, 'EXPIRED', 'Tuition Semester 2 (2023-2024)', '2024-06-30 23:59:59'),
(15, '52200003', NULL, 17500000, 'NOT_YET_PAID', 'Tuition Semester 1 (2024-2025)', '2024-12-31 23:59:59');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(36) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `fullname` varchar(255) DEFAULT NULL,
  `phone` varchar(10) DEFAULT NULL,
  `available_balance` double DEFAULT NULL,
  `role` enum('ADMIN','STUDENT') DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `email`, `fullname`, `phone`, `available_balance`, `role`, `address`) VALUES
('000001', 'admin', '123456', 'admin@example.com', 'System Administrator', '0909123456', 1000000, 'ADMIN', NULL),
('52200001', 'student01', '123456', 'chikha13122@gmail.com', 'Nguyen Van A', '0911222333', 50000000, 'STUDENT', NULL),
('52200002', 'student02', '123456', 'stu02@example.com', 'Tran Thi B', '0922333444', 30000000, 'STUDENT', NULL),
('52200003', 'student03', '123456', 'stu03@example.com', 'Le Van C', '0933444555', 2000000, 'STUDENT', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `tuition_id` (`tuition_id`),
  ADD KEY `ix_payments_id` (`id`);

--
-- Indexes for table `tuitions`
--
ALTER TABLE `tuitions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `payer_id` (`payer_id`),
  ADD KEY `ix_tuitions_id` (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `ix_users_email` (`email`),
  ADD UNIQUE KEY `ix_users_username` (`username`),
  ADD KEY `ix_users_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tuitions`
--
ALTER TABLE `tuitions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `payments_ibfk_2` FOREIGN KEY (`tuition_id`) REFERENCES `tuitions` (`id`);

--
-- Constraints for table `tuitions`
--
ALTER TABLE `tuitions`
  ADD CONSTRAINT `tuitions_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `tuitions_ibfk_2` FOREIGN KEY (`payer_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
