## 一、ISP-CDU 疫情打卡自动化工具

### 1. ISP-CDU简介

`isp-cdu`为成都大学ISP系统学生端疫情打卡自动化工具。结合腾讯云函数实现`每天定时打卡`。每天的打卡情况会在打开完成后最后推送到你的微信，实时反馈每日打卡情况。无需人工操作。 **特别提醒** ：请保证在使用本工具的前一天，你自己在isp系统上进行过疫情打卡，`isp-cdu`只会同步前一天的登记信息。若不满足该条件请手动登录isp系统打卡后再使用本项目。

GitHub链接： https://github.com/ahaox/isp-cdu
Gitee链接： https://gitee.com/ahaox/isp-cdu

作者：`ahao`。

### 2. 发布初心

`让ISP疫情打卡不再烦扰每一位小橙子`

### 3. 注意事项

① 本脚本完全免费，如果您通过其他渠道消费购买，请一定口吐芬芳对方！！！

② 本脚本不设计第三方信息收集，不存在保存使用者的账号密码等信息。

③ 本仓库发布的`isp-cdu`项目中涉及的任何脚本，仅用于`CDU-ISP`系统疫情打卡，禁止用于商业用途，不能保证其合法性，准确性，完整性和有效性，请根据情况自行判断。

④ `ahao` 对任何脚本问题概不负责，包括但不限于由任何脚本错误导致的任何损失或损害.

⑤ 请勿将`isp-cdu`项目的任何内容用于商业或非法目的，否则后果自负。

⑥ 如果任何单位或个人认为该项目的脚本可能涉嫌侵犯其权利，则应及时通知并提供身份证明，所有权证明，我们将在收到认证文件后删除相关脚本。

⑦ 以任何方式查看此项目的人或直接或间接使用`isp-cdu`项目的任何脚本的使用者都应仔细阅读此声明。`ahao` 保留随时更改或补充此免责声明的权利。一旦使用并复制了任何相关脚本或`isp-cdu`项目，则视为您已接受此免责声明。

⑧ 您必须在下载后的24小时内从计算机或手机中完全删除以上内容。



## 二、主要功能

### 1. 自动登录CDU-ISP系统

### 2. 自动进行疫情信息打卡



## 三、使用教程（小白版）

### 1. 下载项目代码

进入本项目代码仓下载ZIP压缩包到本地，并解压到桌面。

![image-20210208221338099](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208221338.png)

<img src="https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208221635.png" alt="image-20210208221635404" style="zoom:50%;" /> 

### 2. 进入云函数

腾讯云函数免费开通地址，地址：https://console.cloud.tencent.com/scf/list-create?rid=1&ns=default

登录以后按照流程自行开通。

### 3. 新建函数

函数名称随意，运行环境选**Python 3.6**，创建方式选择 **自定义创建** 

<img src="https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208220551.png" alt="image-20210208220544755" style="zoom:50%;" />

### 4. 上传代码

确保环境为**python 3.6**，执行方法改为：`index.main`，提交方式一定要选 **本地上传文件夹** ，然后选择解压到桌面的文件夹 **isp-cdu-master** ，然后点击这个上传把文件夹上传进来。

![image-20210208221947302](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208221947.png)

文件夹上传成功后，点击高级配置

<img src="https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208222031.png" alt="image-20210208222031676" style="zoom:50%;" />

### 5. 高级配置

内存用不了太大，**64MB**就够了，超时时间改为最大的**900秒**，然后点击最下面的完成。

<img src="https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208222509.png" alt="image-20210208222509238" style="zoom:50%;" />

### 6. 安装依赖

点击终端，然后选择新终端，显示终端窗口，在终端窗口里面输入：

```bash
cd src/ && /var/lang/python3/bin/python3 -m pip install -r requirements.txt -t .
```

![image-20210208223921155](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208231109.png)

输入命令后回车执行，等待安装完成。大概1分钟左右。

### 7. 配置账号

自己改下`init.config`里的`账号密码`以及`Server酱密匙`，更改完后点击保存，部署并测试。如果你的配置没有错，稍等几分钟便可以看到结果，在此期间不要刷新页面。结果会在执行日志里。 

**Server酱密匙** 用于微信推送打卡情况，需要自己申请，申请地址： http://sc.ftqq.com/

![image-20210208222917450](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208222917.png)

![image-20210208224125911](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208230157.png)

### 8. 设置定时

新建触发器，触发周期为自定义，表达式就是每天的什么时候做任务，我选择的早上8点30分，可以自行修改，填好后点击提交即可，到此你的ISP-CDU疫情自动打卡项目便部署完成，感谢使用！！

![image-20210208230222605](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208230222.png)



## 四、使用教程（专业人士）

专业人士是指：有过python开发的胖友们。

本项目开发ide为**pycharm**， 环境为：**python3.6** + **requests** + **lxml** + **beautifulsoup4**

pycharm直接打开本项目,  安装**requirements**指定的环境依赖，运行main.py方法即可。

```
pip3 install -r requirements -i https://pypi.tuna.tsinghua.edu.cn/simple/
```



## 五、打赏作者

![pay](https://cdn.jsdelivr.net/gh/ahaox/pictures/image20210208232946.png "在这里输入图片标题")

 **金额不论大小。一分也是爱。** 

