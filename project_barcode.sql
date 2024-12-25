-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 29, 2024 at 10:05 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project_barcode`
--

-- --------------------------------------------------------

--
-- Table structure for table `dang_ky_mon_hoc`
--

CREATE TABLE `dang_ky_mon_hoc` (
  `id` int(11) NOT NULL,
  `mssv` varchar(100) NOT NULL,
  `ma_mon` varchar(100) NOT NULL,
  `nhom` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dang_ky_mon_hoc`
--

INSERT INTO `dang_ky_mon_hoc` (`id`, `mssv`, `ma_mon`, `nhom`) VALUES
(146, 'B2013481', 'ct173', '1');

-- --------------------------------------------------------

--
-- Table structure for table `diem_danh`
--

CREATE TABLE `diem_danh` (
  `id` int(11) NOT NULL,
  `mssv` varchar(100) NOT NULL,
  `ma_mon` varchar(100) NOT NULL,
  `nhom` varchar(100) NOT NULL,
  `tuan_hoc` varchar(100) NOT NULL,
  `trang_thai` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `mon_hoc`
--

CREATE TABLE `mon_hoc` (
  `ma_mon` varchar(100) NOT NULL,
  `ten_mon` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mon_hoc`
--

INSERT INTO `mon_hoc` (`ma_mon`, `ten_mon`) VALUES
('ct173', 'kien truc may tinh'),
('ct176', 'lap trinh huong doi tuong'),
('ct177', 'cau truc du lieu'),
('ct221', 'lap trinh mang'),
('ct225', 'lap trinh python');

-- --------------------------------------------------------

--
-- Table structure for table `nhom`
--

CREATE TABLE `nhom` (
  `id` int(11) NOT NULL,
  `stt_nhom` varchar(100) NOT NULL,
  `so_luong_sv` varchar(100) NOT NULL,
  `ma_mon` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nhom`
--

INSERT INTO `nhom` (`id`, `stt_nhom`, `so_luong_sv`, `ma_mon`) VALUES
(15, '1', '20', 'ct173'),
(17, '2', '30', 'ct173'),
(18, '1', '20', 'ct176'),
(19, '1', '30', 'ct177'),
(20, '1', '20', 'ct221'),
(21, '1', '20', 'ct225');

-- --------------------------------------------------------

--
-- Table structure for table `sinh_vien`
--

CREATE TABLE `sinh_vien` (
  `ma_so_sinh_vien` varchar(100) NOT NULL,
  `ho_ten` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `gioi_tinh` varchar(100) NOT NULL,
  `so_dien_thoai` varchar(100) NOT NULL,
  `anh_sinh_vien` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sinh_vien`
--

INSERT INTO `sinh_vien` (`ma_so_sinh_vien`, `ho_ten`, `email`, `gioi_tinh`, `so_dien_thoai`, `anh_sinh_vien`) VALUES
('B2013481', 'tuan loc', 'loc@student.ctu.edu.vn', 'Nam', '1111-111-111', 'E:/CTU/HK2_nam_4_2023-2024/NLMMT/img/u1.jpg'),
('B2013482', 'lam', 'lam@student.ctu.edu.vn', 'Nam', '2222-222-222', 'E:/CTU/HK2_nam_4_2023-2024/NLMMT/img/lam.jpg'),
('B2013483', 'cam tien', 'tien@student.ctu.edu.vn', 'Nữ', '3333-333-333', 'E:/CTU/HK2_nam_4_2023-2024/NLMMT/img/tien.jpg'),
('B2013484', 'thanh phuong', 'phuong@student.ctu.edu.vn', 'Nam', '4444-444-444', 'E:/CTU/HK2_nam_4_2023-2024/NLMMT/img/phuong.jpg'),
('B2013485', 'huu thang', 'thang@student.ctu.edu.vn', 'Nam', '5555-555-555', 'E:/CTU/HK2_nam_4_2023-2024/NLMMT/img/u2.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dang_ky_mon_hoc`
--
ALTER TABLE `dang_ky_mon_hoc`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ma_so_sinh_vien` (`mssv`),
  ADD KEY `ma_mon` (`ma_mon`);

--
-- Indexes for table `diem_danh`
--
ALTER TABLE `diem_danh`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ma_mon` (`ma_mon`);

--
-- Indexes for table `mon_hoc`
--
ALTER TABLE `mon_hoc`
  ADD PRIMARY KEY (`ma_mon`);

--
-- Indexes for table `nhom`
--
ALTER TABLE `nhom`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ma_mon` (`ma_mon`);

--
-- Indexes for table `sinh_vien`
--
ALTER TABLE `sinh_vien`
  ADD PRIMARY KEY (`ma_so_sinh_vien`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dang_ky_mon_hoc`
--
ALTER TABLE `dang_ky_mon_hoc`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=147;

--
-- AUTO_INCREMENT for table `diem_danh`
--
ALTER TABLE `diem_danh`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=334;

--
-- AUTO_INCREMENT for table `nhom`
--
ALTER TABLE `nhom`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dang_ky_mon_hoc`
--
ALTER TABLE `dang_ky_mon_hoc`
  ADD CONSTRAINT `dang_ky_mon_hoc_ibfk_1` FOREIGN KEY (`mssv`) REFERENCES `sinh_vien` (`ma_so_sinh_vien`),
  ADD CONSTRAINT `dang_ky_mon_hoc_ibfk_2` FOREIGN KEY (`ma_mon`) REFERENCES `mon_hoc` (`ma_mon`);

--
-- Constraints for table `diem_danh`
--
ALTER TABLE `diem_danh`
  ADD CONSTRAINT `diem_danh_ibfk_1` FOREIGN KEY (`ma_mon`) REFERENCES `mon_hoc` (`ma_mon`);

--
-- Constraints for table `nhom`
--
ALTER TABLE `nhom`
  ADD CONSTRAINT `nhom_ibfk_1` FOREIGN KEY (`ma_mon`) REFERENCES `mon_hoc` (`ma_mon`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
