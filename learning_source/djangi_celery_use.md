# <center> Celery 介绍</center>
## 一、 简介
Celery是一个简单、灵活且可靠的，处理大量消息的分布式系统，它是一个专注于实时处理的任务队列，同时也支持任务调度。


中文官网：
[celery中文官网](http://docs.jinkan.org/docs/celery)

安装  

    pip install celery

    #查看是否存在
    pip freeze|grep -i 'celery'


## 二 名词解释
1. broker—消息传输的中间件，生产者一旦有消息发送，将发至broker【RQ,Redis】
2. backend-用于存储消息/任务结果，如果需要跟踪和查询任务状态，则需添加要配置相关。
3. worker-工作者-消费/执行broker中消息/任务的进程。

## 使用celery

```python
from celery import Celery
app = Celery('kqlproject',broker='redis://:password@127.0.0.1:6379/1')
#app = Celery('dadablog',broker='redis://:@127.0.0.1:6379/1')
#第一个参数为自定义名字，

#创建任务函数
@app.task
def task_test():
    print("task is running")
```
## 启动worker
ubuntu 终端中，task.py文件同级目录下执行下面命令：
    
    #此模式默认为前台启动，终端中会输出相关日志。
    celery -A tasks worker --loglevel=info


## 创建生产者-推送任务
在tasks.py 文件的同级目录下进入ipython3 执行如下代码：
```python
from tasks import task_test
task_test.delay()

执行完毕后，观察worker的日志。
```
## 存储执行结果-worker

Celery提供存储任务执行结果的方案，需借助redis或mysql或Memcached等。
```python
from celery import Celery
app = Celery(
   'demo',
   broker='redis://@127.0.0.1:6379/1',
   backend='redis://@127.0.0.1:6379/2',
)
#创建任务函数
@app.task
def test_tak(a,b):
    print("task is runing")
    return a+b
```




## Django中使用celery
1. 创建celery配置文件
   
      项目同名目录下创建celery.py
2. 应用下创建task.py集中定义对应的work函数。
3. 视图函数充当生产者，推送具体worker函数。
4. 项目目录下启动worker
    
   
    celery -A 项目同名目录名 worker -l info 

## 正式环境后台启动
   
      nohub celery -A projetname worker -P gevent -c 1000 > celery.log 2>&1 &

      #1. nohub 忽略所有挂断信号(sighup)
      #2. projectname 项目配置目录 
      #3. -P 使用python协程进行任务的开启，开启1000个协程
      #4. celery.log 在当前目录下生成日志文件，也可以使用绝对路径。
      #5. 标准输入输入是文件描述符0，它是命令的输入，缺省是键盘，也可以是文件或其他命令的输出。
      #6. 标准输出输出是文件描述符1，它是命令的输出，缺省是屏幕，也可以是文件。
      #7. 标准错误输入是文件描述符2，这是命令错误的输出，缺省是屏幕，也可以是文件。
      #8. &符号:代表将命令在后台启动。
      #9. 2>&1 将错误输出重定向给标准输出，中间加&f符号。    