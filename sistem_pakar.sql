-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jun 13, 2024 at 08:00 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sistem_pakar`
--

-- --------------------------------------------------------

--
-- Stand-in structure for view `detail_variabel`
-- (See below for the actual view)
--
CREATE TABLE `detail_variabel` (
`id_tml` int(11)
,`id_tmv` int(11)
,`name_tmv` varchar(255)
,`label_tml` varchar(255)
);

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_desc_rule`
--

CREATE TABLE `tbl_m_desc_rule` (
  `id_tmdr` int(11) NOT NULL,
  `rule_ttfr` int(11) NOT NULL,
  `desc_tmdr` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_linguistic`
--

CREATE TABLE `tbl_m_linguistic` (
  `id_tml` int(11) NOT NULL,
  `id_tmv` int(11) NOT NULL,
  `label_tml` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_linguistic`
--

INSERT INTO `tbl_m_linguistic` (`id_tml`, `id_tmv`, `label_tml`) VALUES
(1, 1, 'rendah'),
(2, 1, 'sedang'),
(3, 1, 'tinggi'),
(4, 2, 'rendah'),
(5, 2, 'sedang'),
(6, 2, 'tinggi'),
(7, 3, 'rendah'),
(8, 3, 'sedang'),
(9, 3, 'tinggi'),
(10, 4, 'rendah'),
(11, 4, 'sedang'),
(12, 4, 'tinggi'),
(13, 5, 'rendah'),
(14, 5, 'sedang'),
(15, 5, 'tinggi'),
(16, 6, 'rendah'),
(17, 6, 'sedang'),
(18, 6, 'tinggi'),
(19, 7, 'rendah'),
(20, 7, 'sedang'),
(21, 7, 'tinggi');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_users`
--

CREATE TABLE `tbl_m_users` (
  `id_tmu` int(11) NOT NULL,
  `username_tmu` varchar(20) NOT NULL,
  `password_tmu` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_users`
--

INSERT INTO `tbl_m_users` (`id_tmu`, `username_tmu`, `password_tmu`) VALUES
(1, 'vikha', '4297f44b13955235245b2497399d7a93'),
(2, 'bayu', '202cb962ac59075b964b07152d234b70'),
(3, 't', 'e358efa489f58062f10dd7316b65649e');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_m_variabel`
--

CREATE TABLE `tbl_m_variabel` (
  `id_tmv` int(11) NOT NULL,
  `name_tmv` varchar(255) NOT NULL,
  `type_tmv` enum('input','output') NOT NULL,
  `question_tmv` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_m_variabel`
--

INSERT INTO `tbl_m_variabel` (`id_tmv`, `name_tmv`, `type_tmv`, `question_tmv`) VALUES
(1, 'kebahagian', 'input', 'Seberapa bahagia Anda dengan hidup Anda saat ini!'),
(2, 'prestasi_akademik', 'input', 'Bagaimana penilaian Anda terhadap prestasi akademik Anda?'),
(3, 'kemandirian', 'input', 'Seberapa mandiri Anda dalam melakukan aktivitas sehari-hari?'),
(4, 'keterampilan_sosial', 'input', 'Bagaimana Anda menilai keterampilan sosial Anda?'),
(5, 'tingkat_stres', 'input', 'Seberapa sering Anda merasa stres dalam keseharian Anda?'),
(6, 'kepercayaan_diri', 'input', 'Seberapa tinggi tingkat kepercayaan diri Anda?'),
(7, 'kedisiplinan', 'input', 'Bagaimana Anda menilai tingkat kedisiplinan Anda?'),
(11, 'rtt', 'output', 'rt');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_t_fuzzy_rules`
--

CREATE TABLE `tbl_t_fuzzy_rules` (
  `id_ttfr` int(11) NOT NULL,
  `id_tmv` int(11) NOT NULL,
  `id_tml` int(11) NOT NULL,
  `rule_ttfr` int(11) NOT NULL,
  `output_ttfr` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbl_t_fuzzy_rules`
--

INSERT INTO `tbl_t_fuzzy_rules` (`id_ttfr`, `id_tmv`, `id_tml`, `rule_ttfr`, `output_ttfr`) VALUES
(1, 1, 1, 1, 'otoriter'),
(2, 2, 5, 1, 'otoriter'),
(3, 3, 7, 1, 'otoriter'),
(4, 4, 10, 1, 'otoriter'),
(5, 5, 15, 1, 'otoriter'),
(6, 6, 16, 1, 'otoriter'),
(7, 7, 21, 1, 'otoriter'),
(8, 1, 1, 3, 'permisif'),
(9, 2, 4, 3, 'permisif'),
(10, 3, 8, 3, 'permisif'),
(11, 4, 11, 3, 'permisif'),
(12, 5, 14, 3, 'permisif'),
(13, 6, 17, 3, 'permisif'),
(14, 7, 19, 3, 'permisif'),
(15, 1, 3, 4, 'demokratis'),
(16, 2, 6, 4, 'demokratis'),
(17, 3, 9, 4, 'demokratis'),
(18, 4, 12, 4, 'demokratis'),
(19, 5, 13, 4, 'demokratis'),
(20, 6, 18, 4, 'demokratis'),
(21, 7, 20, 4, 'demokratis'),
(22, 1, 2, 2, 'tidak_terlibat'),
(23, 2, 4, 2, 'tidak_terlibat'),
(24, 3, 7, 2, 'tidak_terlibat'),
(25, 4, 10, 2, 'tidak_terlibat'),
(26, 5, 15, 2, 'tidak_terlibat'),
(27, 6, 16, 2, 'tidak_terlibat'),
(28, 7, 19, 2, 'tidak_terlibat');

-- --------------------------------------------------------

--
-- Stand-in structure for view `vw_fuzzy_rules`
-- (See below for the actual view)
--
CREATE TABLE `vw_fuzzy_rules` (
`id` int(11)
,`rule` int(11)
,`variabel` varchar(255)
,`linguistic` varchar(255)
,`output` varchar(30)
);

-- --------------------------------------------------------

--
-- Structure for view `detail_variabel`
--
DROP TABLE IF EXISTS `detail_variabel`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `detail_variabel`  AS SELECT `l`.`id_tml` AS `id_tml`, `v`.`id_tmv` AS `id_tmv`, `v`.`name_tmv` AS `name_tmv`, `l`.`label_tml` AS `label_tml` FROM (`tbl_m_linguistic` `l` join `tbl_m_variabel` `v` on(`l`.`id_tmv` = `v`.`id_tmv`)) ;

-- --------------------------------------------------------

--
-- Structure for view `vw_fuzzy_rules`
--
DROP TABLE IF EXISTS `vw_fuzzy_rules`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_fuzzy_rules`  AS SELECT `fr`.`id_ttfr` AS `id`, `fr`.`rule_ttfr` AS `rule`, `mv`.`name_tmv` AS `variabel`, `ml`.`label_tml` AS `linguistic`, `fr`.`output_ttfr` AS `output` FROM ((`tbl_t_fuzzy_rules` `fr` join `tbl_m_variabel` `mv` on(`fr`.`id_tmv` = `mv`.`id_tmv`)) join `tbl_m_linguistic` `ml` on(`fr`.`id_tml` = `ml`.`id_tml`)) ;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_m_desc_rule`
--
ALTER TABLE `tbl_m_desc_rule`
  ADD PRIMARY KEY (`id_tmdr`),
  ADD KEY `rule_ttfr` (`rule_ttfr`);

--
-- Indexes for table `tbl_m_linguistic`
--
ALTER TABLE `tbl_m_linguistic`
  ADD PRIMARY KEY (`id_tml`),
  ADD KEY `id_tmv` (`id_tmv`);

--
-- Indexes for table `tbl_m_users`
--
ALTER TABLE `tbl_m_users`
  ADD PRIMARY KEY (`id_tmu`);

--
-- Indexes for table `tbl_m_variabel`
--
ALTER TABLE `tbl_m_variabel`
  ADD PRIMARY KEY (`id_tmv`);

--
-- Indexes for table `tbl_t_fuzzy_rules`
--
ALTER TABLE `tbl_t_fuzzy_rules`
  ADD PRIMARY KEY (`id_ttfr`),
  ADD KEY `id_tmv` (`id_tmv`),
  ADD KEY `id_tml` (`id_tml`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_m_desc_rule`
--
ALTER TABLE `tbl_m_desc_rule`
  MODIFY `id_tmdr` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `tbl_m_linguistic`
--
ALTER TABLE `tbl_m_linguistic`
  MODIFY `id_tml` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `tbl_m_users`
--
ALTER TABLE `tbl_m_users`
  MODIFY `id_tmu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbl_m_variabel`
--
ALTER TABLE `tbl_m_variabel`
  MODIFY `id_tmv` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `tbl_t_fuzzy_rules`
--
ALTER TABLE `tbl_t_fuzzy_rules`
  MODIFY `id_ttfr` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbl_m_linguistic`
--
ALTER TABLE `tbl_m_linguistic`
  ADD CONSTRAINT `tbl_m_linguistic_ibfk_1` FOREIGN KEY (`id_tmv`) REFERENCES `tbl_m_variabel` (`id_tmv`);

--
-- Constraints for table `tbl_t_fuzzy_rules`
--
ALTER TABLE `tbl_t_fuzzy_rules`
  ADD CONSTRAINT `tbl_t_fuzzy_rules_ibfk_1` FOREIGN KEY (`id_tmv`) REFERENCES `tbl_m_variabel` (`id_tmv`),
  ADD CONSTRAINT `tbl_t_fuzzy_rules_ibfk_2` FOREIGN KEY (`id_tml`) REFERENCES `tbl_m_linguistic` (`id_tml`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
