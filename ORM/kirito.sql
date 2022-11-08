SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for y_user
-- ----------------------------
DROP TABLE IF EXISTS `y_user`;
CREATE TABLE `y_user`  (
  `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '登录名，限20字',
  `pass` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '密码，限20字',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最近更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '用户表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of y_user
-- ----------------------------
INSERT INTO `y_user` VALUES (1, 'admin', '123456', '2022-10-10 09:12:12', '2022-10-10 09:12:33');

-- ----------------------------
-- Table structure for y_question
-- ----------------------------
DROP TABLE IF EXISTS `y_question`;
CREATE TABLE `y_question`  (
  `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `paper_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0 COMMENT '试卷id y_paper.id',
  `type` tinyint(255) UNSIGNED NOT NULL DEFAULT 1 COMMENT '试题类型 1:选择题; 2:判断题;',
  `question` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '题目，限255字',
  `correct_answer` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '正确答案',
  `score` tinyint(4) UNSIGNED NOT NULL DEFAULT 1 COMMENT '分值',
  `my_answer` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '我的答案',
  `my_score` tinyint(4) UNSIGNED NOT NULL DEFAULT 0 COMMENT '我的得分',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最近更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '试卷表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for y_paper
-- ----------------------------
DROP TABLE IF EXISTS `y_paper`;
CREATE TABLE `y_paper`  (
  `id` bigint(255) UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '试卷名称',
  `create_user_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0 COMMENT '创建用户id',
  `answer_user_id` bigint(20) UNSIGNED NOT NULL DEFAULT 0 COMMENT '答题用户id',
  `create_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime(0) NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP(0) COMMENT '最近更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '试卷表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;