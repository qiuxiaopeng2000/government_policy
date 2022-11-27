### 1. 获取某一城市的政策
http://127.0.0.1:8000/api/show_policy?city=<city_name>

> example: 查询安徽省政府的政策文件
> 
> http://127.0.0.1:8000/api/show_policy?city=安徽
> 


### 2. 更新某一城市的政策
http://127.0.0.1:8000/api/update_policy?city=<city_name>

> example：更新安徽省政府的政策文件
> 
> http://127.0.0.1:8000/api/update_policy?city=anhui
> 
> note: 重新爬虫，等待时间较长
> 


### 3. 注册账号
http://127.0.0.1:8000/api/user_register?username=<username>&password=<password>&email=<email>
> example:
> http://127.0.0.1:8000/api/user_register?username=qxp&password=123&email=2621099562@qq.com
> 
>

### 4. 用户登录
http://127.0.0.1:8000/api/user_login?username=<username>&password=<password>
> example:
> http://127.0.0.1:8000/api/user_login?username=qxp&password=1234567890
> 


### 5. 退出登录
http://127.0.0.1:8000/api/user_logout?username=<username>
> http://127.0.0.1:8000/api/user_logout?username=qxp

### 5. 修改密码
http://127.0.0.1:8000/api/user_change_password?username=<username>&old_password=<password>&new_password<password>
> example:
> http://127.0.0.1:8000/api/user_change_password?username=qxp&old_password=123&new_password=1234567890
> 


### 5. 修改email
http://127.0.0.1:8000/api/user_change_email?email=<email>
> example:
> http://127.0.0.1:8000/api/user_change_email?email=2621099562@qq.com
> 

### 5. 修改头像
http://127.0.0.1:8000/api/user_change_portrait?portrait=<portrait_url>
> example:
> http://127.0.0.1:8000/api/user_change_portrait?portrait=portrait/宝儿姐.jpg
> 
> 请注意：enctype="multipart/form-data"


### 5. 展示用户信息
http://127.0.0.1:8000/api/show_user_info
> example:
> http://127.0.0.1:8000/api/show_user_info
> 


### 6. 注销账户
http://127.0.0.1:8000/api/user_delete?username=<username>&password=<password>
> example:
> http://127.0.0.1:8000/api/user_delete?username=qxp&old_password=123&new_password=1234567890
> 


### 7. 关注城市
http://127.0.0.1:8000/api/follow_city?username=<username>&city=<city>
> example:
> http://127.0.0.1:8000/api/follow_city?username=qxp&city=anhui
> 


### 8. 关注列表
http://127.0.0.1:8000/api/show_follow?username=<username>
> example:
> http://127.0.0.1:8000/api/show_follow?username=qxp
> 


### 9. 取消关注
http://127.0.0.1:8000/api/delete_follow?username=<username>&city=<city>
> example:
> http://127.0.0.1:8000/api/delete_follow?username=qxp&city=anhui
