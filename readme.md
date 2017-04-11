
密码管理工具。

### 原理

思路来源于[花密](http://flowerpassword.com/)。  
算法[hmac](http://baike.baidu.com/item/hmac)。

签名字符串用命令行参数中的**域名**和**账号**拼接生成。签名秘钥来源于用户输入，生成签名后转为base64编码，基于一定规则生成一个包含大小写字母和数字的15位密码。


### 使用

##### 安装

`pip install pwm-tool`


#### 生成密码

默认使用空字符串作为签名秘钥。

`⇒  pwm -d github.com -a lovedboy`

使用自己的秘钥签名(**-k**):

```
⇒  pwm -d github.com -a lovedboy -k
your key:
```

#### 保存域名和账号

首先你需要配置数据库的保存路径。

```
echo "export PWM_DB_PATH=your_path" >> ~/.bashrc
source ~/.bashrc
```

`pwm -d github.com -a lovedboy -w`

这里只会保存域名和账号，方便搜索。密码都是通过密钥算出来的。

#### 搜索

可基于账号和域名模糊搜索：

```
pwm -s lovedboy
pwm -s github.com -k
```

#### 安全性

保证你签名秘钥的安全！！！

#### 在线生成

[https://lovedboy.github.io/pwm/](https://lovedboy.github.io/pwm/)



