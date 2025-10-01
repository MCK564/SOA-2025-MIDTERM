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
-- Database: `bank_tuition`
--

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
(1, '52200001', '52200001', 15000000, 'IN_PROCESS', 'Tuition Semester 1 (2022-2023)', '2023-01-15 23:59:59'),
(2, '52200001', '52200001', 16000000, 'PAID', 'Tuition Semester 2 (2022-2023)', '2023-06-30 23:59:59'),
(3, '52200001', NULL, 16500000, 'EXPIRED', 'Tuition Semester 1 (2023-2024)', '2023-12-31 23:59:59'),
(4, '52200001', NULL, 17000000, 'IN_PROCESS', 'Tuition Semester 2 (2023-2024)', '2024-06-30 23:59:59'),
(5, '52200001', '52200001', 17500000, 'PAID', 'Tuition Semester 1 (2024-2025)', '2024-12-31 23:59:59'),
(6, '52200002', '52200002', 15000000, 'PAID', 'Tuition Semester 1 (2022-2023)', '2023-01-15 23:59:59'),
(7, '52200002', NULL, 16000000, 'EXPIRED', 'Tuition Semester 2 (2022-2023)', '2023-06-30 23:59:59'),
(8, '52200002', '52200002', 16500000, 'PAID', 'Tuition Semester 1 (2023-2024)', '2023-12-31 23:59:59'),
(9, '52200002', NULL, 17000000, 'IN_PROCESS', 'Tuition Semester 2 (2023-2024)', '2024-06-30 23:59:59'),
(10, '52200002', '52200001', 17500000, 'PAID', 'Tuition Semester 1 (2024-2025)', '2024-12-31 23:59:59'),
(11, '52200003', '52200003', 15000000, 'PAID', 'Tuition Semester 1 (2022-2023)', '2023-01-15 23:59:59'),
(12, '52200003', '52200003', 16000000, 'PAID', 'Tuition Semester 2 (2022-2023)', '2023-06-30 23:59:59'),
(13, '52200003', '52200003', 16500000, 'PAID', 'Tuition Semester 1 (2023-2024)', '2023-12-31 23:59:59'),
(14, '52200003', NULL, 17000000, 'EXPIRED', 'Tuition Semester 2 (2023-2024)', '2024-06-30 23:59:59'),
(15, '52200003', '52200001', 17500000, 'PAID', 'Tuition Semester 1 (2024-2025)', '2024-12-31 23:59:59');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tuitions`
--
ALTER TABLE `tuitions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ix_tuitions_id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tuitions`
--
ALTER TABLE `tuitions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
