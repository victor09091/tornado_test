数据库采用的是tornadb,

CREATE TABLE IF NOT EXISTS `user`(
   `id` INT UNSIGNED AUTO_INCREMENT,
   `name` VARCHAR(100) NOT NULL,
   `password` VARCHAR(40) NOT NULL,
   `email` VARCHAR(40) NOT NULL,
   PRIMARY KEY ( `id` )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

简单实现用户注册登录系统，图片验证码及邮件验证码。使用tornado, nsq实现。支持服务随时重启不丢失邮件。api接口不阻塞

存储及缓存可以使用mysql,redis,

前端用户界面用bootstrap+ajax实现
