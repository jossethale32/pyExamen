/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 100413 (10.4.13-MariaDB)
 Source Host           : localhost:3308
 Source Schema         : pago_en_linea

 Target Server Type    : MySQL
 Target Server Version : 100413 (10.4.13-MariaDB)
 File Encoding         : 65001

 Date: 26/10/2023 02:12:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for clientes
-- ----------------------------
DROP TABLE IF EXISTS `clientes`;
CREATE TABLE `clientes`  (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  `balance` varchar(45) CHARACTER SET utf8 COLLATE utf8_bin NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of clientes
-- ----------------------------

-- ----------------------------
-- Table structure for pagos
-- ----------------------------
DROP TABLE IF EXISTS `pagos`;
CREATE TABLE `pagos`  (
  `ID CLIENTE` int NOT NULL,
  `CUOTA` int NULL DEFAULT NULL,
  `MONTO` int NULL DEFAULT NULL,
  `FECHA PAGO` date NULL DEFAULT NULL,
  `PAGOFECHAREALIZACION` date NULL DEFAULT NULL,
  `ESTADO` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `REFERENCIA` varchar(250) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of pagos
-- ----------------------------
INSERT INTO `pagos` VALUES (1001, 1, 200, '2023-10-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1001, 2, 200, '2023-11-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1001, 3, 200, '2023-12-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1002, 1, 500, '2023-10-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1002, 2, 500, '2023-11-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1002, 3, 500, '2023-12-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1003, 1, 700, '2023-10-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1003, 2, 700, '2023-11-01', NULL, 'A', '');
INSERT INTO `pagos` VALUES (1003, 3, 700, '2023-12-01', NULL, 'A', '');

SET FOREIGN_KEY_CHECKS = 1;
