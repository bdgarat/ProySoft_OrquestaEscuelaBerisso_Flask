-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 29-11-2019 a las 02:40:36
-- Versión del servidor: 10.4.8-MariaDB
-- Versión de PHP: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `grupo22`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `asistencia_estudiante_taller`
--

CREATE TABLE `asistencia_estudiante_taller` (
  `id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL,
  `fecha` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `barrio`
--

CREATE TABLE `barrio` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `barrio`
--

INSERT INTO `barrio` (`id`, `nombre`) VALUES
(1, 'Barrio Náutico'),
(2, 'Barrio Obrero'),
(3, 'Berisso'),
(4, 'Barrio Solidaridad'),
(5, 'Barrio Obrero'),
(6, 'Barrio Bco. Pcia.'),
(7, 'Barrio J.B. Justo'),
(8, 'Barrio Obrero'),
(9, 'El Carmen'),
(10, 'El Labrador'),
(11, 'Ensenada'),
(12, 'La Hermosura'),
(13, 'La PLata'),
(14, 'Los Talas'),
(15, 'Ringuelet'),
(16, 'Tolosa'),
(17, 'Villa Alba'),
(18, 'Villa Arguello'),
(19, 'Villa B. C'),
(20, 'Villa Elvira'),
(21, 'Villa Nueva'),
(22, 'Villa Paula'),
(23, 'Villa Progreso'),
(24, 'Villa San Carlos'),
(25, 'Villa Zula');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo_lectivo`
--

CREATE TABLE `ciclo_lectivo` (
  `id` int(11) NOT NULL,
  `fecha_ini` date DEFAULT NULL,
  `fecha_fin` date DEFAULT NULL,
  `semestre` tinyint(1) NOT NULL DEFAULT 1,
  `borrado_logico` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `ciclo_lectivo`
--

INSERT INTO `ciclo_lectivo` (`id`, `fecha_ini`, `fecha_fin`, `semestre`, `borrado_logico`) VALUES
(1, '2019-11-05', '2019-11-16', 1, 1),
(2, '2020-04-04', '2020-07-15', 1, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ciclo_lectivo_taller`
--

CREATE TABLE `ciclo_lectivo_taller` (
  `taller_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `config`
--

CREATE TABLE `config` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) COLLATE utf8_spanish_ci NOT NULL,
  `descripcion` text COLLATE utf8_spanish_ci NOT NULL,
  `contacto` varchar(255) COLLATE utf8_spanish_ci NOT NULL,
  `paginacion` int(100) NOT NULL,
  `sitio_habilitado` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `config`
--

INSERT INTO `config` (`id`, `titulo`, `descripcion`, `contacto`, `paginacion`, `sitio_habilitado`) VALUES
(1, 'Orquesta Escuela de Berisso', 'La Orquesta Escuela de Berisso comenzó a funcionar en septiembre del 2005 en el barrio de El Carmen de la localidad de Berisso bajo la dirección del Mtro. Juan Carlos Herrero, orientada especialmente a la atención de chicos en situación de vulnerabilidad socio-cultural.\r\nDesde sus 20 alumnos iniciales fue creciendo hasta atender actualmente una matrícula de aproximadamente 530 chicos, distribuidos en los 15 núcleos que la conforman y dirigida a una franja etaria de 5 a 23 años, cubriendo en su accionar a la casi totalidad de los barrios de Berisso más los espacios cedidos por el Club Español y el Teatro Argentino', 'contacto@contacto.com', 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docente`
--

CREATE TABLE `docente` (
  `id` int(11) NOT NULL,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `borrado_logico` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `docente`
--

INSERT INTO `docente` (`id`, `apellido`, `nombre`, `fecha_nac`, `localidad_id`, `domicilio`, `genero_id`, `tipo_doc_id`, `numero`, `tel`, `borrado_logico`) VALUES
(2, 'Soria', 'Valeria', '1989-03-16', 4, 'Pergamino 1234', 2, 1, 35013548, '2221-411842', 0),
(3, 'Pagano', 'Matías', '1982-03-16', 9, 'Azul 1124', 1, 1, 31013548, '2221-411843', 0),
(4, 'Banchoff', 'Claudia', '1978-05-08', 11, 'Ensenada 8746', 2, 1, 29846134, '2221-418461', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `docente_responsable_taller`
--

CREATE TABLE `docente_responsable_taller` (
  `docente_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `escuela`
--

CREATE TABLE `escuela` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `telefono` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `escuela`
--

INSERT INTO `escuela` (`id`, `nombre`, `direccion`, `telefono`) VALUES
(1, '502', NULL, NULL),
(2, 'Albert Thomas', NULL, NULL),
(3, 'Anexa', NULL, NULL),
(4, 'Anexo T. Speroni', NULL, NULL),
(5, 'Basiliana', NULL, NULL),
(6, 'Basiliano', NULL, NULL),
(7, 'Bellas Artes', NULL, NULL),
(8, 'Canossiano', NULL, NULL),
(9, 'Castañeda', NULL, NULL),
(10, 'Col. Nacional', NULL, NULL),
(11, 'Conquista Cristiana', NULL, NULL),
(12, 'Dardo Rocha N° 24', NULL, NULL),
(13, 'E.E.M.N° 2', NULL, NULL),
(14, 'E.M. N°26', NULL, NULL),
(15, 'E.P. Municipal N° 2', NULL, NULL),
(16, 'EE N° 2', NULL, NULL),
(17, 'EEE N° 501', NULL, NULL),
(18, 'EEE N°501', NULL, NULL),
(19, 'EEM N° 1', NULL, NULL),
(20, 'EEM N° 26 L.P', NULL, NULL),
(21, 'EEM N°128', NULL, NULL),
(22, 'EEM N°2', NULL, NULL),
(23, 'EES N° 10', NULL, NULL),
(24, 'EES N° 14', NULL, NULL),
(25, 'EES N° 4', NULL, NULL),
(26, 'EES N° 4 Berisso', NULL, NULL),
(27, 'EES N° 4 El Pino', NULL, NULL),
(28, 'EEST N° 1 bsso', NULL, NULL),
(29, 'EET Nº 1', NULL, NULL),
(30, 'EET Nº1', NULL, NULL),
(31, 'EGB N°25', NULL, NULL),
(32, 'EM N° 2', NULL, NULL),
(33, 'EMM N° 3', NULL, NULL),
(34, 'EP N° 1 L.P-', NULL, NULL),
(35, 'EP N° 11', NULL, NULL),
(36, 'EP N° 129', NULL, NULL),
(37, 'EP N° 14', NULL, NULL),
(38, 'EP N° 15', NULL, NULL),
(39, 'EP N° 17', NULL, NULL),
(40, 'EP N° 18', NULL, NULL),
(41, 'EP N° 19', NULL, NULL),
(42, 'EP N° 2', NULL, NULL),
(43, 'EP N° 20', NULL, NULL),
(44, 'EP N° 22', NULL, NULL),
(45, 'EP N° 25', NULL, NULL),
(46, 'EP N° 27', NULL, NULL),
(47, 'EP N° 3', NULL, NULL),
(48, 'EP N° 37 LP', NULL, NULL),
(49, 'EP N° 43', NULL, NULL),
(50, 'EP N° 45', NULL, NULL),
(51, 'EP N° 5', NULL, NULL),
(52, 'EP N° 6', NULL, NULL),
(53, 'EP N° 65 La Plata', NULL, NULL),
(54, 'EP N° 7', NULL, NULL),
(55, 'EPB N° 10', NULL, NULL),
(56, 'EPB N° 14', NULL, NULL),
(57, 'EPB N° 15', NULL, NULL),
(58, 'EPB N° 19', NULL, NULL),
(59, 'EPB N° 2', NULL, NULL),
(60, 'EPB N° 20', NULL, NULL),
(61, 'EPB N° 24', NULL, NULL),
(62, 'EPB N° 25', NULL, NULL),
(63, 'EPB N° 45', NULL, NULL),
(64, 'EPB N° 5', NULL, NULL),
(65, 'EPB N° 55', NULL, NULL),
(66, 'EPB N° 6', NULL, NULL),
(67, 'EPB N° 65', NULL, NULL),
(68, 'EPB N° 8', NULL, NULL),
(69, 'ESB N° 10', NULL, NULL),
(70, 'ESB N° 11', NULL, NULL),
(71, 'ESB N° 14', NULL, NULL),
(72, 'ESB N° 3', NULL, NULL),
(73, 'ESB N° 61', NULL, NULL),
(74, 'ESB N° 66', NULL, NULL),
(75, 'ESB N° 8', NULL, NULL),
(76, 'ESB N° 9', NULL, NULL),
(77, 'ESC N° 10', NULL, NULL),
(78, 'ESC N° 13', NULL, NULL),
(79, 'ESC N° 19', NULL, NULL),
(80, 'ESC N° 2', NULL, NULL),
(81, 'ESC N° 20', NULL, NULL),
(82, 'ESC N° 22', NULL, NULL),
(83, 'ESC N° 23', NULL, NULL),
(84, 'ESC N° 24', NULL, NULL),
(85, 'ESC N° 25', NULL, NULL),
(86, 'ESC N° 27', NULL, NULL),
(87, 'ESC N° 3', NULL, NULL),
(88, 'ESC N° 43', NULL, NULL),
(89, 'ESC N° 45', NULL, NULL),
(90, 'ESC N° 5', NULL, NULL),
(91, 'ESC N° 501', NULL, NULL),
(92, 'ESC N° 6', NULL, NULL),
(93, 'ESC N° 66', NULL, NULL),
(94, 'ESC N° 7', NULL, NULL),
(95, 'ESC N° 8', NULL, NULL),
(96, 'ESC N°11', NULL, NULL),
(97, 'ESC N°17', NULL, NULL),
(98, 'ESC N°19', NULL, NULL),
(99, 'ESC N°3', NULL, NULL),
(100, 'ESC N°7', NULL, NULL),
(101, 'ESC de Arte', NULL, NULL),
(102, 'ESS N° 4', NULL, NULL),
(103, 'Enseñanza Media', NULL, NULL),
(104, 'Especial N° 502', NULL, NULL),
(105, 'Estrada', NULL, NULL),
(106, 'FACULTAD', NULL, NULL),
(107, 'INDUSTRIAL', NULL, NULL),
(108, 'Italiana', NULL, NULL),
(109, 'J 904', NULL, NULL),
(110, 'J. Manuel Strada', NULL, NULL),
(111, 'Jacarandá', NULL, NULL),
(112, 'Jardín Euforion', NULL, NULL),
(113, 'Jardín N° 903', NULL, NULL),
(114, 'Jardín N° 907', NULL, NULL),
(115, 'JoaquinV.Gonzalez', NULL, NULL),
(116, 'Lola Mora sec', NULL, NULL),
(117, 'Lujan Sierra', NULL, NULL),
(118, 'MUNICIOAL 11', NULL, NULL),
(119, 'María Auxiliadora', NULL, NULL),
(120, 'María Reina', NULL, NULL),
(121, 'Media 2 España', NULL, NULL),
(122, 'Media N 1', NULL, NULL),
(123, 'Mercedita de S.Martin', NULL, NULL),
(124, 'Monseñor Alberti', NULL, NULL),
(125, 'Mtro Luis MKEY', NULL, NULL),
(126, 'Mñor. Rasore', NULL, NULL),
(127, 'N1 Francisco', NULL, NULL),
(128, 'Normal 2', NULL, NULL),
(129, 'Normal 3 LP', NULL, NULL),
(130, 'Normal n 2', NULL, NULL),
(131, 'Ntra Sra Lourdes', NULL, NULL),
(132, 'Ntra. Sra. del Valle', NULL, NULL),
(133, 'PSICOLOGIA', NULL, NULL),
(134, 'Parroquial', NULL, NULL),
(135, 'Pasos del Libertedor', NULL, NULL),
(136, 'Ped 61', NULL, NULL),
(137, 'Pedagogica', NULL, NULL),
(138, 'SEC N° 8', NULL, NULL),
(139, 'SEC N°17', NULL, NULL),
(140, 'San Simón', NULL, NULL),
(141, 'Santa Rosa', NULL, NULL),
(142, 'Sra de Fátima', NULL, NULL),
(143, 'Sta Margarita', NULL, NULL),
(144, 'Sta Ro. de Lima', NULL, NULL),
(145, 'Sta Rosa', NULL, NULL),
(146, 'Sta Rosa Lima', NULL, NULL),
(147, 'Sta. R. de Lima', NULL, NULL),
(148, 'Sta. Rosa de lima', NULL, NULL),
(149, 'Técnica N° 1', NULL, NULL),
(150, 'Técnica N° 1 Berisso', NULL, NULL),
(151, 'Técnica N° 5', NULL, NULL),
(152, 'Técnica N° 7', NULL, NULL),
(153, 'UCALP', NULL, NULL),
(154, 'UNLP', NULL, NULL),
(155, 'UTN', NULL, NULL),
(156, 'Universitas', NULL, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante`
--

CREATE TABLE `estudiante` (
  `id` int(11) NOT NULL,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `nivel_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `escuela_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` varchar(11) COLLATE utf8_unicode_ci NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `barrio_id` int(11) NOT NULL,
  `borrado_logico` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `estudiante`
--

INSERT INTO `estudiante` (`id`, `apellido`, `nombre`, `fecha_nac`, `localidad_id`, `nivel_id`, `domicilio`, `genero_id`, `escuela_id`, `tipo_doc_id`, `numero`, `tel`, `barrio_id`, `borrado_logico`) VALUES
(6, 'Onofri', 'Melisa', '1999-11-05', 8, 4, 'City Bell', 2, 5, 1, '29846135', '2221-411514', 13, 0),
(7, 'Garat', 'Braian', '1998-04-13', 10, 3, 'Chascomus 1945', 1, 16, 1, '24841235', '2221-411233', 5, 0),
(8, 'Repetto', 'Lorenzo', '1994-04-28', 12, 12, 'San Martín 1430', 1, 30, 1, '37880905', '2221-411872', 25, 0),
(9, 'Tufillaro', 'Pierina', '1999-04-28', 6, 2, 'Lomas 1452', 2, 7, 1, '29874513', '2221-411841', 16, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estudiante_taller`
--

CREATE TABLE `estudiante_taller` (
  `estudiante_id` int(11) NOT NULL,
  `ciclo_lectivo_id` int(11) NOT NULL,
  `taller_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `genero`
--

CREATE TABLE `genero` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `genero`
--

INSERT INTO `genero` (`id`, `nombre`) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Otro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `instrumento`
--

CREATE TABLE `instrumento` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `numero_inventario` varchar(50) COLLATE utf8_unicode_ci NOT NULL,
  `tipo_id` int(11) NOT NULL,
  `foto` mediumblob DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nivel`
--

CREATE TABLE `nivel` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `nivel`
--

INSERT INTO `nivel` (`id`, `nombre`) VALUES
(1, 'I'),
(2, 'II'),
(3, 'III'),
(4, 'IV'),
(5, 'V'),
(6, 'VI'),
(7, 'VII'),
(8, 'VIII'),
(9, 'IX'),
(10, 'X'),
(11, 'XI'),
(12, 'XII');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nucleo`
--

CREATE TABLE `nucleo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `direccion` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

CREATE TABLE `permiso` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `permiso`
--

INSERT INTO `permiso` (`id`, `nombre`) VALUES
(1, 'estudiante_index'),
(2, 'estudiante_new'),
(3, 'estudiante_destroy'),
(4, 'estudiante_update'),
(5, 'estudiante_show'),
(6, 'docente_index'),
(7, 'docente_new'),
(8, 'docente_destroy'),
(9, 'docente_update'),
(10, 'docente_show'),
(11, 'preceptor_index'),
(12, 'preceptor_new'),
(13, 'preceptor_destroy'),
(14, 'preceptor_update'),
(15, 'preceptor_show'),
(16, 'admin_index'),
(17, 'admin_new'),
(18, 'admin_destroy'),
(19, 'admin_update'),
(20, 'admin_show'),
(21, 'config_index'),
(22, 'config_update'),
(23, 'ciclo_lectivo_index'),
(24, 'ciclo_lectivo_new'),
(25, 'ciclo_lectivo_destroy'),
(26, 'ciclo_lectivo_update'),
(27, 'ciclo_lectivo_show'),
(28, 'instrumento_new'),
(29, 'instrumento_show'),
(30, 'instrumento_update'),
(31, 'instrumento_destroy'),
(32, 'instrumento_index');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preceptor`
--

CREATE TABLE `preceptor` (
  `id` int(11) NOT NULL,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `borrado_logico` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `preceptor_nucleo`
--

CREATE TABLE `preceptor_nucleo` (
  `preceptor_id` int(11) NOT NULL,
  `nucleo_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsable`
--

CREATE TABLE `responsable` (
  `id` int(11) NOT NULL,
  `apellido` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nac` date NOT NULL,
  `localidad_id` int(11) NOT NULL,
  `domicilio` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `genero_id` int(11) NOT NULL,
  `tipo_doc_id` int(11) NOT NULL,
  `numero` int(11) NOT NULL,
  `tel` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `responsable`
--

INSERT INTO `responsable` (`id`, `apellido`, `nombre`, `fecha_nac`, `localidad_id`, `domicilio`, `genero_id`, `tipo_doc_id`, `numero`, `tel`) VALUES
(1, 'Responsable', 'Juan', '1987-02-19', 5, 'San Martín', 1, 1, 37880906, '2221-411872'),
(2, 'Responsable', 'María', '1990-11-05', 3, 'Junín 1021', 2, 1, 39517834, '2221-4115148');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsable_estudiante`
--

CREATE TABLE `responsable_estudiante` (
  `responsable_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `tipo_responsable_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `responsable_estudiante`
--

INSERT INTO `responsable_estudiante` (`responsable_id`, `estudiante_id`, `tipo_responsable_id`) VALUES
(1, 6, 1),
(1, 8, 3),
(2, 7, 2),
(2, 9, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(1, 'admin'),
(2, 'preceptor'),
(3, 'docente');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE `rol_tiene_permiso` (
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `rol_tiene_permiso`
--

INSERT INTO `rol_tiene_permiso` (`rol_id`, `permiso_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 7),
(1, 8),
(1, 9),
(1, 10),
(1, 11),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 19),
(1, 20),
(1, 21),
(1, 22),
(1, 23),
(1, 24),
(1, 25),
(1, 26),
(1, 27),
(1, 28),
(1, 29),
(1, 30),
(1, 31),
(1, 32),
(2, 1),
(2, 3),
(2, 4),
(2, 5),
(2, 6),
(2, 7),
(2, 8),
(2, 9),
(2, 10),
(2, 11),
(2, 15),
(3, 1),
(3, 2),
(3, 3),
(3, 4),
(3, 5),
(3, 6),
(3, 10),
(3, 23),
(3, 27),
(3, 29),
(3, 32);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `taller`
--

CREATE TABLE `taller` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `nombre_corto` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `taller`
--

INSERT INTO `taller` (`id`, `nombre`, `nombre_corto`) VALUES
(1, 'Guitarra', 'GC'),
(2, 'Percusión', 'PC'),
(3, 'Coro', 'CC'),
(4, 'Viento', 'VC'),
(5, 'Orquesta', 'OC'),
(6, 'Cuerda', 'CUC');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_instrumento`
--

CREATE TABLE `tipo_instrumento` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `tipo_instrumento`
--

INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES
(1, 'Viento'),
(2, 'Cuerda'),
(3, 'Percusión');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_responsable`
--

CREATE TABLE `tipo_responsable` (
  `id` int(11) NOT NULL,
  `nombre` varchar(50) COLLATE utf8_spanish_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

--
-- Volcado de datos para la tabla `tipo_responsable`
--

INSERT INTO `tipo_responsable` (`id`, `nombre`) VALUES
(1, 'padre'),
(2, 'madre'),
(3, 'tutor'),
(4, 'otro');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT 1,
  `updated_at` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `first_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `borrado_logico` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `email`, `username`, `password`, `activo`, `updated_at`, `created_at`, `first_name`, `last_name`, `borrado_logico`) VALUES
(1, 'admin@test.com', 'admin_principal', '123456', 1, '2019-10-23 20:40:44', '2019-10-23 20:40:44', 'Admin', 'Admin', 0),
(7, 'test6@test.com', 'test6', '123456', 1, '2019-11-05 14:54:27', '2019-10-23 20:52:01', 'Preceptor1', 'Preceptor1', 0),
(8, 'test7@test.com', 'test7', '123456', 1, '2019-11-05 14:58:16', '2019-10-23 20:52:13', 'Preceptor2', 'Preceptor2', 0),
(9, 'test8@test.com', 'test8', '123456', 1, '2019-10-23 20:54:18', '2019-10-23 20:54:18', 'Preceptor3', 'Preceptor3', 0),
(10, 'test9@test.com', 'test9', '123456', 1, '2019-10-23 20:54:56', '2019-10-23 20:54:56', 'Docente1', 'Docente1', 0),
(11, 'test10@test.com', 'test10', '123456', 1, '2019-10-23 20:55:08', '2019-10-23 20:55:08', 'Docente2', 'Docente2', 0),
(12, 'test11@test.com', 'test11', '123456', 1, '2019-10-23 20:55:22', '2019-10-23 20:55:22', 'Docente3', 'Docente3', 0),
(13, 'test12@test.com', 'test12', '123456', 1, '2019-10-23 20:55:34', '2019-10-23 20:55:34', 'Docente4', 'Docente4', 0),
(14, 'test13@test.com', 'test13', '123456', 1, '2019-10-23 20:56:26', '2019-10-23 20:56:26', 'Preceptor y Docente 1', 'Preceptor y Docente 1', 0),
(15, 'test14@test.com', 'test14', '123456', 1, '2019-10-23 20:56:45', '2019-10-23 20:56:45', 'Preceptor y Docente 2', 'Preceptor y Docente 2', 0),
(18, 'test17@test.com', 'test17', '123456', 1, '2019-11-05 14:55:31', '2019-10-23 20:58:07', 'Admin y Preceptor 1', 'Admin y Preceptor 1', 0),
(19, 'test19@test.com', 'test19', '123456', 1, '2019-10-30 16:17:54', '2019-10-30 15:55:23', 'PreceptorPrueba', 'PreceptorPrueba', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_tiene_rol`
--

CREATE TABLE `usuario_tiene_rol` (
  `usuario_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Volcado de datos para la tabla `usuario_tiene_rol`
--

INSERT INTO `usuario_tiene_rol` (`usuario_id`, `rol_id`) VALUES
(1, 1),
(7, 2),
(8, 2),
(9, 2),
(10, 3),
(11, 3),
(12, 3),
(13, 3),
(14, 2),
(14, 3),
(15, 2),
(15, 3),
(16, 3),
(17, 3),
(18, 1),
(18, 2),
(19, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `asistencia_estudiante_taller`
--
ALTER TABLE `asistencia_estudiante_taller`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_asistencia_estudiante_id` (`estudiante_id`),
  ADD KEY `FK_asistencia_ciclo_lectivo_id` (`ciclo_lectivo_id`),
  ADD KEY `FK_asistencia_taller_id` (`taller_id`);

--
-- Indices de la tabla `barrio`
--
ALTER TABLE `barrio`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ciclo_lectivo`
--
ALTER TABLE `ciclo_lectivo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `ciclo_lectivo_taller`
--
ALTER TABLE `ciclo_lectivo_taller`
  ADD PRIMARY KEY (`ciclo_lectivo_id`,`taller_id`),
  ADD KEY `FK_ciclo_lectivo_taller_taller_id` (`taller_id`);

--
-- Indices de la tabla `config`
--
ALTER TABLE `config`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `docente`
--
ALTER TABLE `docente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_genero_docente_id` (`genero_id`);

--
-- Indices de la tabla `docente_responsable_taller`
--
ALTER TABLE `docente_responsable_taller`
  ADD PRIMARY KEY (`docente_id`,`ciclo_lectivo_id`,`taller_id`),
  ADD KEY `FK_docente_responsable_taller_ciclo_lectivo_id` (`ciclo_lectivo_id`),
  ADD KEY `FK_docente_responsable_taller_taller_id` (`taller_id`);

--
-- Indices de la tabla `escuela`
--
ALTER TABLE `escuela`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_nivel_id` (`nivel_id`),
  ADD KEY `FK_genero_estudiante_id` (`genero_id`),
  ADD KEY `FK_escuela_id` (`escuela_id`),
  ADD KEY `FK_barrio_id` (`barrio_id`);

--
-- Indices de la tabla `estudiante_taller`
--
ALTER TABLE `estudiante_taller`
  ADD PRIMARY KEY (`estudiante_id`,`ciclo_lectivo_id`,`taller_id`),
  ADD KEY `FK_estudiante_taller_ciclo_lectivo_id` (`ciclo_lectivo_id`),
  ADD KEY `FK_estudiante_taller_taller_id` (`taller_id`);

--
-- Indices de la tabla `genero`
--
ALTER TABLE `genero`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `instrumento`
--
ALTER TABLE `instrumento`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_tipo_instrumento_id` (`tipo_id`);

--
-- Indices de la tabla `nivel`
--
ALTER TABLE `nivel`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `nucleo`
--
ALTER TABLE `nucleo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `permiso`
--
ALTER TABLE `permiso`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `preceptor`
--
ALTER TABLE `preceptor`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `preceptor_nucleo`
--
ALTER TABLE `preceptor_nucleo`
  ADD PRIMARY KEY (`preceptor_id`,`nucleo_id`),
  ADD KEY `FK_nucleo_id` (`nucleo_id`);

--
-- Indices de la tabla `responsable`
--
ALTER TABLE `responsable`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FK_genero_responsable_id` (`genero_id`);

--
-- Indices de la tabla `responsable_estudiante`
--
ALTER TABLE `responsable_estudiante`
  ADD PRIMARY KEY (`responsable_id`,`estudiante_id`),
  ADD KEY `FK_estudiante_id` (`estudiante_id`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `rol_tiene_permiso`
--
ALTER TABLE `rol_tiene_permiso`
  ADD PRIMARY KEY (`rol_id`,`permiso_id`),
  ADD KEY `FK_permiso_id` (`permiso_id`);

--
-- Indices de la tabla `taller`
--
ALTER TABLE `taller`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_instrumento`
--
ALTER TABLE `tipo_instrumento`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tipo_responsable`
--
ALTER TABLE `tipo_responsable`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario_tiene_rol`
--
ALTER TABLE `usuario_tiene_rol`
  ADD PRIMARY KEY (`usuario_id`,`rol_id`),
  ADD KEY `FK_rol_utp_id` (`rol_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `asistencia_estudiante_taller`
--
ALTER TABLE `asistencia_estudiante_taller`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `barrio`
--
ALTER TABLE `barrio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `ciclo_lectivo`
--
ALTER TABLE `ciclo_lectivo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `config`
--
ALTER TABLE `config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `docente`
--
ALTER TABLE `docente`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `escuela`
--
ALTER TABLE `escuela`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=157;

--
-- AUTO_INCREMENT de la tabla `estudiante`
--
ALTER TABLE `estudiante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `genero`
--
ALTER TABLE `genero`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `instrumento`
--
ALTER TABLE `instrumento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `nivel`
--
ALTER TABLE `nivel`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `nucleo`
--
ALTER TABLE `nucleo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `permiso`
--
ALTER TABLE `permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT de la tabla `preceptor`
--
ALTER TABLE `preceptor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `responsable`
--
ALTER TABLE `responsable`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `taller`
--
ALTER TABLE `taller`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `tipo_instrumento`
--
ALTER TABLE `tipo_instrumento`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `tipo_responsable`
--
ALTER TABLE `tipo_responsable`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `asistencia_estudiante_taller`
--
ALTER TABLE `asistencia_estudiante_taller`
  ADD CONSTRAINT `FK_asistencia_ciclo_lectivo_id` FOREIGN KEY (`ciclo_lectivo_id`) REFERENCES `ciclo_lectivo` (`id`),
  ADD CONSTRAINT `FK_asistencia_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `FK_asistencia_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `taller` (`id`);

--
-- Filtros para la tabla `ciclo_lectivo_taller`
--
ALTER TABLE `ciclo_lectivo_taller`
  ADD CONSTRAINT `FK_ciclo_lectivo_taller_ciclo_lectivo_id` FOREIGN KEY (`ciclo_lectivo_id`) REFERENCES `ciclo_lectivo` (`id`),
  ADD CONSTRAINT `FK_ciclo_lectivo_taller_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `taller` (`id`);

--
-- Filtros para la tabla `docente`
--
ALTER TABLE `docente`
  ADD CONSTRAINT `FK_genero_docente_id` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`);

--
-- Filtros para la tabla `docente_responsable_taller`
--
ALTER TABLE `docente_responsable_taller`
  ADD CONSTRAINT `FK_docente_responsable_taller_ciclo_lectivo_id` FOREIGN KEY (`ciclo_lectivo_id`) REFERENCES `ciclo_lectivo` (`id`),
  ADD CONSTRAINT `FK_docente_responsable_taller_docente_id` FOREIGN KEY (`docente_id`) REFERENCES `docente` (`id`),
  ADD CONSTRAINT `FK_docente_responsable_taller_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `taller` (`id`);

--
-- Filtros para la tabla `estudiante`
--
ALTER TABLE `estudiante`
  ADD CONSTRAINT `FK_barrio_id` FOREIGN KEY (`barrio_id`) REFERENCES `barrio` (`id`),
  ADD CONSTRAINT `FK_escuela_id` FOREIGN KEY (`escuela_id`) REFERENCES `escuela` (`id`),
  ADD CONSTRAINT `FK_genero_estudiante_id` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`),
  ADD CONSTRAINT `FK_nivel_id` FOREIGN KEY (`nivel_id`) REFERENCES `nivel` (`id`);

--
-- Filtros para la tabla `estudiante_taller`
--
ALTER TABLE `estudiante_taller`
  ADD CONSTRAINT `FK_estudiante_taller_ciclo_lectivo_id` FOREIGN KEY (`ciclo_lectivo_id`) REFERENCES `ciclo_lectivo` (`id`),
  ADD CONSTRAINT `FK_estudiante_taller_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `FK_estudiante_taller_taller_id` FOREIGN KEY (`taller_id`) REFERENCES `taller` (`id`);

--
-- Filtros para la tabla `instrumento`
--
ALTER TABLE `instrumento`
  ADD CONSTRAINT `FK_tipo_instrumento_id` FOREIGN KEY (`tipo_id`) REFERENCES `tipo_instrumento` (`id`);

--
-- Filtros para la tabla `preceptor_nucleo`
--
ALTER TABLE `preceptor_nucleo`
  ADD CONSTRAINT `FK_nucleo_id` FOREIGN KEY (`nucleo_id`) REFERENCES `nucleo` (`id`),
  ADD CONSTRAINT `FK_preceptor_id` FOREIGN KEY (`preceptor_id`) REFERENCES `preceptor` (`id`);

--
-- Filtros para la tabla `responsable`
--
ALTER TABLE `responsable`
  ADD CONSTRAINT `FK_genero_responsable_id` FOREIGN KEY (`genero_id`) REFERENCES `genero` (`id`);

--
-- Filtros para la tabla `responsable_estudiante`
--
ALTER TABLE `responsable_estudiante`
  ADD CONSTRAINT `FK_estudiante_id` FOREIGN KEY (`estudiante_id`) REFERENCES `estudiante` (`id`),
  ADD CONSTRAINT `FK_responsable_id` FOREIGN KEY (`responsable_id`) REFERENCES `responsable` (`id`);

--
-- Filtros para la tabla `rol_tiene_permiso`
--
ALTER TABLE `rol_tiene_permiso`
  ADD CONSTRAINT `FK_permiso_id` FOREIGN KEY (`permiso_id`) REFERENCES `permiso` (`id`),
  ADD CONSTRAINT `FK_rol_id` FOREIGN KEY (`rol_id`) REFERENCES `rol` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
