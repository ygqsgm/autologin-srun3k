# autologin-srun3k
校园网环境:河南工业大学haut.edu.cn srun3k登陆 

          (其它学校使用srun3K方案应该类似可能需要修改)

运行环境:openwrt chaos_calmer 15.05.1 （Lenovo Y1 测试通过 ）

  需安装 python3 (python3-base python3-codecs python3-email)
              
              coreutils-nohup
         
如何使用：

    下载至路由器端
    
    修改 学号，路由器WAN口MAC，密码
    
    nohup python3 autologin.py &
    
