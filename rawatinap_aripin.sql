-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 26, 2026 at 04:28 AM
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
-- Database: `rawatinap_aripin`
--

-- --------------------------------------------------------

--
-- Table structure for table `kamar_aripin`
--

CREATE TABLE `kamar_aripin` (
  `id_kamar_aripin` varchar(5) NOT NULL,
  `no_kamar_aripin` int(11) NOT NULL,
  `kelas_aripin` varchar(5) NOT NULL,
  `status_kamar_aripin` varchar(15) NOT NULL,
  `harga_aripin` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kamar_aripin`
--

INSERT INTO `kamar_aripin` (`id_kamar_aripin`, `no_kamar_aripin`, `kelas_aripin`, `status_kamar_aripin`, `harga_aripin`) VALUES
('K001', 1, 'A', 'sudah diisi', 150000),
('K002', 2, 'B', 'belum diisi', 100000),
('K003', 3, 'C', 'sudah diisi', 50000),
('K004', 4, 'B', 'sudah diisi', 100000),
('K005', 5, 'A', 'belum diisi', 150000);

-- --------------------------------------------------------

--
-- Table structure for table `pasien_aripin`
--

CREATE TABLE `pasien_aripin` (
  `id_pasien_aripin` varchar(5) NOT NULL,
  `nama_aripin` varchar(50) NOT NULL,
  `alamat_aripin` varchar(100) NOT NULL,
  `kontak_aripin` varchar(13) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pasien_aripin`
--

INSERT INTO `pasien_aripin` (`id_pasien_aripin`, `nama_aripin`, `alamat_aripin`, `kontak_aripin`) VALUES
('P001', 'gavin', 'cipageran', '089652417423'),
('P002', 'ipin', 'cikendal', '089652417411'),
('P003', 'iting', 'kamarung', '089652417424'),
('P004', 'riki', 'cimahi', '089652417231'),
('P005', 'lal', 'cimahi', '089652417276');

-- --------------------------------------------------------

--
-- Table structure for table `rawat_inap_aripin`
--

CREATE TABLE `rawat_inap_aripin` (
  `id_rawat_aripin` varchar(5) NOT NULL,
  `id_pasien_aripin` varchar(5) NOT NULL,
  `id_kamar_aripin` varchar(5) NOT NULL,
  `tgl_masuk_aripin` date NOT NULL,
  `tgl_keluar_aripin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `rawat_inap_aripin`
--

INSERT INTO `rawat_inap_aripin` (`id_rawat_aripin`, `id_pasien_aripin`, `id_kamar_aripin`, `tgl_masuk_aripin`, `tgl_keluar_aripin`) VALUES
('R001', 'P001', 'K001', '2026-01-01', '2026-01-13'),
('R002', 'P002', 'K002', '2025-01-01', '2025-01-20'),
('R003', 'P003', 'K003', '2025-02-02', '2025-02-20'),
('R004', 'P004', 'K004', '2025-05-01', '2025-05-25'),
('R005', 'P005', 'K005', '2025-12-01', '2025-12-30');

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_aripin`
--

CREATE TABLE `transaksi_aripin` (
  `id_transaksi_aripin` varchar(5) NOT NULL,
  `id_pasien_aripin` varchar(5) NOT NULL,
  `total_biaya_aripin` int(11) NOT NULL,
  `status_pembayaran_aripin` varchar(15) NOT NULL,
  `tgl_aripin` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi_aripin`
--

INSERT INTO `transaksi_aripin` (`id_transaksi_aripin`, `id_pasien_aripin`, `total_biaya_aripin`, `status_pembayaran_aripin`, `tgl_aripin`) VALUES
('2', 'P002', 1900000, 'sudah lunas', '2026-01-06'),
('3', 'P004', 2400000, 'belum lunas', '2026-01-04');

-- --------------------------------------------------------

--
-- Table structure for table `user_aripin`
--

CREATE TABLE `user_aripin` (
  `id_user_aripin` varchar(5) NOT NULL,
  `username_aripin` varchar(50) NOT NULL,
  `password_aripin` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_aripin`
--

INSERT INTO `user_aripin` (`id_user_aripin`, `username_aripin`, `password_aripin`) VALUES
('U001', 'rrnnndii', 'rendi123'),
('U002', 'asep', 'asep111'),
('U003', 'asep2', 'asep222'),
('U004', 'asep3', 'asep333'),
('U005', 'asep4', 'asep444');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kamar_aripin`
--
ALTER TABLE `kamar_aripin`
  ADD PRIMARY KEY (`id_kamar_aripin`);

--
-- Indexes for table `pasien_aripin`
--
ALTER TABLE `pasien_aripin`
  ADD PRIMARY KEY (`id_pasien_aripin`);

--
-- Indexes for table `rawat_inap_aripin`
--
ALTER TABLE `rawat_inap_aripin`
  ADD PRIMARY KEY (`id_rawat_aripin`),
  ADD KEY `id_pasien_grandy` (`id_pasien_aripin`),
  ADD KEY `id_kamar_grandy` (`id_kamar_aripin`);

--
-- Indexes for table `transaksi_aripin`
--
ALTER TABLE `transaksi_aripin`
  ADD PRIMARY KEY (`id_transaksi_aripin`),
  ADD KEY `id_pasien_grandy` (`id_pasien_aripin`);

--
-- Indexes for table `user_aripin`
--
ALTER TABLE `user_aripin`
  ADD PRIMARY KEY (`id_user_aripin`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `rawat_inap_aripin`
--
ALTER TABLE `rawat_inap_aripin`
  ADD CONSTRAINT `rawat_inap_aripin_ibfk_1` FOREIGN KEY (`id_pasien_aripin`) REFERENCES `pasien_aripin` (`id_pasien_aripin`),
  ADD CONSTRAINT `rawat_inap_aripin_ibfk_2` FOREIGN KEY (`id_kamar_aripin`) REFERENCES `kamar_aripin` (`id_kamar_aripin`);

--
-- Constraints for table `transaksi_aripin`
--
ALTER TABLE `transaksi_aripin`
  ADD CONSTRAINT `transaksi_aripin_ibfk_1` FOREIGN KEY (`id_pasien_aripin`) REFERENCES `rawat_inap_aripin` (`id_pasien_aripin`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
