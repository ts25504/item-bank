# Test paper generator
一个帮助教师维护题库和自动组卷的Web app，使用MVC模式。

## 如何使用
1. 安装Python：
[`Python官方网站`](www.python.org)

2. 安装Virtual env
Linux用户：
``` sh
$ sudo apt-get install python-virtualenv
```

Mac用户
``` sh
$ sudo easy_install virtualenv
```

安装完成后，在源码相应的文件夹中进行以下操作：
``` sh
$ virtualenv venv
New python executable in venv/bin/python2.7
Also creating executable in venv/bin/python
Installing setuptools............done.
Installing pip...............done.
```

目前已经加载了虚拟环境，然后我们在执行虚拟环境运行脚本：
``` sh
$ source venv/bin/activate
```

微软用户需要执行
``` sh
$ venv\Scripts\activate
```

3. 根据requirements.txt安装依赖
``` sh
(venv) $ pip install -r requirements.txt
```

4. 根据config.py中设置mysql相关的环境变量，执行
``` sh
python manage.py db upgrade
```
