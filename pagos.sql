-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-10-2023 a las 04:06:35
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `pago_en_linea`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `ID CLIENTE` int(255) NOT NULL,
  `CUOTA` int(255) DEFAULT NULL,
  `MONTO` int(255) DEFAULT NULL,
  `FECHA PAGO` date DEFAULT NULL,
  `PAGOFECHAREALIZACION` date DEFAULT NULL,
  `ESTADO` varchar(250) DEFAULT NULL,
  `REFERENCIA` varchar(250) DEFAULT NULL,
  `MONTO_ANTERIOR` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`ID CLIENTE`, `CUOTA`, `MONTO`, `FECHA PAGO`, `PAGOFECHAREALIZACION`, `ESTADO`, `REFERENCIA`, `MONTO_ANTERIOR`) VALUES
(1001, 1, 200, '2023-10-01', NULL, 'A', NULL, 200),
(1001, 2, 200, '2023-11-01', NULL, 'A', '', 200),
(1001, 3, 200, '2023-12-01', NULL, 'A', NULL, 200),
(1002, 1, 500, '2023-10-01', NULL, 'A', '', 500),
(1002, 2, 500, '2023-11-01', NULL, 'A', '', 500),
(1002, 3, 500, '2023-12-01', NULL, 'A', '', 500),
(1003, 1, 700, '2023-10-01', NULL, 'A', '', 700),
(1003, 2, 700, '2023-11-01', NULL, 'A', '', 700),
(1003, 3, 700, '2023-12-01', NULL, 'A', '', 700);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
