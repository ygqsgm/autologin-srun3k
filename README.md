# autologin-srun3k 
# 运行环境:
校园网环境:河南工业大学haut.edu.cn srun3k登陆 

   (其它学校使用srun3K方案 应该 类似可能需要修改认证服务器地址)

运行环境:openwrt chaos_calmer 15.05.1 （Lenovo Y1 测试通过 ）

   至少需要安装 python3 (python3-base python3-codecs python3-email ), coreutils-nohup
         
# 如何使用：

下载至路由器端

    wget https://github.com/ygqsgm/autologin-srun3k/raw/master/autologin.py    
    
修改 学号，密码

    VIM autologin.py

    nohup python3 autologin.py &
    
原理简介：

1.模拟校园网客户端发包(HTTP POST登陆，以及 UDP 心跳包)

2.通过读取/proc/net/arp 0x2  -1 获取在线人数>0时登陆
