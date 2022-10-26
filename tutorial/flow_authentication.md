# 认证流程

ssl -> http -> jwt

ssl: passlib

jwt: python-jose

ssl上传之前，前端应该也要哈希加盐一下？（猜测）  

以下操作和ssl都没关系.jpg

登录认证
1. 收到请求后先认证用户（账号和密码）
2. 创建后续通信需要的token以及有效时间
3. 返回token

```
post -> authenticate_user -> get_user -> verify_password -> create_access_token
```
* authenticate_user 认证部分拆成两块
* get_user 先从db获取用户信息
* verify_password 通过 passlib.context库的CryptContext，返回T/F
* create_access_token 通过 jose库的jwt创建token，返回字符串

后续通信
1. 通过token确认用户身份
2. 处理业务
3. 返回信息
```
get -> get_current_user -> get_user -> get_current_active_user
```

* get_current_user 自定义了一个异常，通过jwt解码确认用户身份
* get_user 通过db获取用户信息
* get_current_active_user 某个业务环节, 这个是判断用户是否活跃 DB里的一个值，返回T/F
