/*
 Navicat Premium Data Transfer

 Source Server         : silumz
 Source Server Type    : MySQL
 Source Server Version : 50554
 Source Host           : 192.168.1.67:3306
 Source Schema         : silumz

 Target Server Type    : MySQL
 Target Server Version : 50554
 File Encoding         : 65001

 Date: 10/12/2018 22:09:06
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for images_image
-- ----------------------------
DROP TABLE IF EXISTS `images_image`;
CREATE TABLE `images_image`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pageid` int(11) NOT NULL,
  `imageurl` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_cover` tinyint(4) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1709 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for images_page
-- ----------------------------
DROP TABLE IF EXISTS `images_page`;
CREATE TABLE `images_page`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `typeid` int(11) NOT NULL,
  `sendtime` date NOT NULL,
  `title` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `firstimg` int(11) NOT NULL,
  `tagid` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 167 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of images_page
-- ----------------------------
INSERT INTO `images_page` VALUES (166, 1, '2018-12-10', '妩媚美少妇木木媚骨天成撩人心魄', 1673, '[92, 93, 94]');
INSERT INTO `images_page` VALUES (165, 1, '2018-12-10', '知性丽人佑熙连体高叉让人魂牵梦绕', 1632, '[86, 105, 106, 107]');

-- ----------------------------
-- Table structure for images_tag
-- ----------------------------
DROP TABLE IF EXISTS `images_tag`;
CREATE TABLE `images_tag`  (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `tag` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 110 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for images_type
-- ----------------------------
DROP TABLE IF EXISTS `images_type`;
CREATE TABLE `images_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of images_type
-- ----------------------------
INSERT INTO `images_type` VALUES (1, '性感美女');
INSERT INTO `images_type` VALUES (2, '靓丽腿模');
INSERT INTO `images_type` VALUES (3, '清纯美女');

SET FOREIGN_KEY_CHECKS = 1;
