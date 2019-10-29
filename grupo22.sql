-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 29-10-2019 a las 18:30:31
-- Versión del servidor: 10.4.6-MariaDB
-- Versión de PHP: 7.3.9

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
(1, 'Orquesta Escuela de Berisso', 'Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas \"Letraset\", las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum.', 'Teléfono: 2216598741 // 4578996', 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permiso`
--

CREATE TABLE `permiso` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(22, 'config_update');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

CREATE TABLE `rol` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(1, 'admin'),
(2, 'preceptor'),
(3, 'docente'),
(4, 'estudiante');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol_tiene_permiso`
--

CREATE TABLE `rol_tiene_permiso` (
  `rol_id` int(11) NOT NULL,
  `permiso_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(2, 1),
(2, 2),
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
(3, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `activo` tinyint(1) NOT NULL,
  `updated_at` datetime NOT NULL,
  `created_at` datetime NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `borrado_logico` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id`, `email`, `username`, `password`, `activo`, `updated_at`, `created_at`, `first_name`, `last_name`, `borrado_logico`) VALUES
(1, 'admin@test.com', 'admin_principal', '123456', 1, '2019-10-23 20:40:44', '2019-10-23 20:40:44', 'Admin', 'Admin', 0),
(2, 'test1@test.com', 'test1', '123456', 1, '2019-10-23 20:50:05', '2019-10-23 20:50:05', 'Estudiante1', 'Estudiante1', 0),
(3, 'test2@test.com', 'test2', '123456', 1, '2019-10-23 20:50:34', '2019-10-23 20:50:34', 'Estudiante2', 'Estudiante2', 0),
(4, 'test3@test.com', 'test3', '123456', 1, '2019-10-23 20:50:54', '2019-10-23 20:50:54', 'Estudiante3', 'Estudiante3', 0),
(5, 'test4@test.com', 'test4', '123456', 1, '2019-10-23 20:51:08', '2019-10-23 20:51:08', 'Estudiante4', 'Estudiante4', 0),
(6, 'test5@test.com', 'test5', '123456', 1, '2019-10-23 20:51:28', '2019-10-23 20:51:28', 'Estudiante5', 'Estudiante5', 0),
(7, 'test6@test.com', 'test6', '123456', 1, '2019-10-23 20:52:01', '2019-10-23 20:52:01', 'Preceptor1', 'Preceptor1', 0),
(8, 'test7@test.com', 'test7', '123456', 1, '2019-10-23 20:52:13', '2019-10-23 20:52:13', 'Preceptor2', 'Preceptor2', 0),
(9, 'test8@test.com', 'test8', '123456', 1, '2019-10-23 20:54:18', '2019-10-23 20:54:18', 'Preceptor3', 'Preceptor3', 0),
(10, 'test9@test.com', 'test9', '123456', 1, '2019-10-23 20:54:56', '2019-10-23 20:54:56', 'Docente1', 'Docente1', 0),
(11, 'test10@test.com', 'test10', '123456', 1, '2019-10-23 20:55:08', '2019-10-23 20:55:08', 'Docente2', 'Docente2', 0),
(12, 'test11@test.com', 'test11', '123456', 1, '2019-10-23 20:55:22', '2019-10-23 20:55:22', 'Docente3', 'Docente3', 0),
(13, 'test12@test.com', 'test12', '123456', 1, '2019-10-23 20:55:34', '2019-10-23 20:55:34', 'Docente4', 'Docente4', 0),
(14, 'test13@test.com', 'test13', '123456', 1, '2019-10-23 20:56:26', '2019-10-23 20:56:26', 'Preceptor y Docente 1', 'Preceptor y Docente 1', 0),
(15, 'test14@test.com', 'test14', '123456', 1, '2019-10-23 20:56:45', '2019-10-23 20:56:45', 'Preceptor y Docente 2', 'Preceptor y Docente 2', 0),
(16, 'test15@test.com', 'test15', '123456', 1, '2019-10-23 20:57:10', '2019-10-23 20:57:10', 'Estudiante y Docente 1', 'Estudiante y Docente 1', 0),
(17, 'test16@test.com', 'test16', '123456', 1, '2019-10-23 20:57:26', '2019-10-23 20:57:26', 'Estudiante y Docente 2', 'Estudiante y Docente 2', 0),
(18, 'test17@test.com', 'test17', '123456', 1, '2019-10-23 20:58:07', '2019-10-23 20:58:07', 'Admin y Preceptor 1', 'Admin y Preceptor 1', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario_tiene_rol`
--

CREATE TABLE `usuario_tiene_rol` (
  `usuario_id` int(11) NOT NULL,
  `rol_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuario_tiene_rol`
--

INSERT INTO `usuario_tiene_rol` (`usuario_id`, `rol_id`) VALUES
(1, 1),
(2, 4),
(3, 4),
(4, 4),
(5, 4),
(6, 4),
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
(16, 4),
(17, 3),
(17, 4),
(18, 1),
(18, 2);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `config`
--
ALTER TABLE `config`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `permiso`
--
ALTER TABLE `permiso`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `config`
--
ALTER TABLE `config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `permiso`
--
ALTER TABLE `permiso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
