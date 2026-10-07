-- 数据库初始化脚本。本地和 CI 都用这一个文件。
-- 用法：mysql -uroot -p < db/household_db.sql
CREATE DATABASE IF NOT EXISTS household_db
  DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE household_db;

/*
 Navicat Premium Data Transfer

 Source Server         : web_final
 Source Server Type    : MySQL
 Source Server Version : 80032 (8.0.32)
 Source Host           : localhost:3306
 Source Schema         : household_db

 Target Server Type    : MySQL
 Target Server Version : 80032 (8.0.32)
 File Encoding         : 65001

 Date: 02/01/2026 00:06:39
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for resident
-- ----------------------------
DROP TABLE IF EXISTS `resident`;
CREATE TABLE `resident`  (
  `r_id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '姓名',
  `id_card` varchar(18) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '身份证号',
  `gender` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '性别',
  `birthday` date NULL DEFAULT NULL COMMENT '出生日期',
  `phone` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '联系电话',
  `address` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '户籍地址',
  `h_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '户口类型(农业/非农业)',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '录入时间',
  `photo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT 'default.jpg',
  `account_id` int NULL DEFAULT NULL COMMENT '关联的账号ID',
  PRIMARY KEY (`r_id`) USING BTREE,
  UNIQUE INDEX `id_card`(`id_card` ASC) USING BTREE,
  UNIQUE INDEX `account_id`(`account_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resident
-- ----------------------------
INSERT INTO `resident` VALUES (1, '王伟', '33010619850310123X', '男', '1985-03-10', '13857110001', '浙江省杭州市西湖区文一西路88号', '农村家庭户口', '2025-12-25 17:03:42', 'default.jpg', 2);
INSERT INTO `resident` VALUES (2, '王芳', '330102199211058888', '女', '1992-11-05', '13957110002', '浙江省杭州市上城区延安路205号', '城市家庭户口', '2025-12-25 17:03:42', '38aea2f2-f89e-47e6-b3a9-3cb896826b32.webp', 3);
INSERT INTO `resident` VALUES (3, '李强', '330105198807206666', '男', '1988-07-20', '13757110003', '浙江省杭州市拱墅区莫干山路100号', '农村家庭户口', '2025-12-25 17:03:42', NULL, 4);
INSERT INTO `resident` VALUES (4, '李娜', '330108199509122222', '女', '1995-09-12', '13657110004', '浙江省杭州市滨江区江南大道588号', '城市家庭户口', '2025-12-25 17:03:42', NULL, 5);
INSERT INTO `resident` VALUES (5, '张鹏', '330110199002283333', '男', '1990-02-28', '13557110005', '浙江省杭州市余杭区五常大道1号', '农村家庭户口', '2025-12-25 17:03:42', NULL, 6);
INSERT INTO `resident` VALUES (6, '刘洋', '330106198705159999', '男', '1987-05-15', '13357110006', '浙江省杭州市西湖区古墩路300号', '城市家庭户口', '2025-12-25 17:03:42', NULL, 7);
INSERT INTO `resident` VALUES (7, '陈杰', '330109199812017777', '男', '1998-12-01', '13157110007', '浙江省杭州市萧山区市心南路66号', '农村家庭户口', '2025-12-25 17:03:42', NULL, 8);
INSERT INTO `resident` VALUES (8, '赵雷', '330106200205051234', '男', '2002-05-05', '13966667777', '浙江省杭州市江干区凯旋路10号', '城市家庭户口', '2025-12-25 20:26:28', NULL, 9);
INSERT INTO `resident` VALUES (9, '孙艺珍', '330105200511118888', '女', '2005-11-11', '13888889999', '浙江省杭州市拱墅区湖州街50号', '农村家庭户口', '2025-12-25 20:26:28', NULL, 10);
INSERT INTO `resident` VALUES (10, '周杰', '330108200808086666', '男', '2008-08-08', '13777776666', '浙江省杭州市滨江区长河路88号', '城市家庭户口', '2025-12-25 20:26:28', NULL, 11);
INSERT INTO `resident` VALUES (11, '吴非', '330102200101019999', '男', '2001-01-01', '13655554444', '浙江省杭州市上城区复兴南街2号', '农村家庭户口', '2025-12-25 20:26:28', NULL, 12);

-- ----------------------------
-- Table structure for resident_user
-- ----------------------------
DROP TABLE IF EXISTS `resident_user`;
CREATE TABLE `resident_user`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '账号',
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  `reg_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of resident_user
-- ----------------------------
INSERT INTO `resident_user` VALUES (2, '33010619850310123X', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (3, '330102199211058888', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (4, '330105198807206666', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (5, '330108199509122222', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (6, '330110199002283333', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (7, '330106198705159999', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (8, '330109199812017777', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (9, '330106200205051234', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (10, '330105200511118888', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (11, '330108200808086666', '123456', '2025-12-26 18:10:23');
INSERT INTO `resident_user` VALUES (12, '330102200101019999', '123456', '2025-12-26 18:10:23');

-- ----------------------------
-- Table structure for sys_user
-- ----------------------------
DROP TABLE IF EXISTS `sys_user`;
CREATE TABLE `sys_user`  (
  `uid` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '用户名',
  `password` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '密码',
  `real_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '真实姓名',
  PRIMARY KEY (`uid`) USING BTREE,
  UNIQUE INDEX `username`(`username` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of sys_user
-- ----------------------------
INSERT INTO `sys_user` VALUES (1, 'admin', '123456', '系统管理员');

SET FOREIGN_KEY_CHECKS = 1;
