# 随便什么的笔记.jpg

这里是给桐人酱补的教程.jpg（其实我也忘了都要啥环境包了）
```
我直接（大概率有不少没用的包） 
pip freeze > requirements.txt
环境你就 
pip install -r requirements.txt
对了 py版本好像也要3.10+ 
3.6+ 有几个地方需要改一下格式 x
以及我把sqlite也扔上去了
```
目前手头没有闲置的云了

双十一考虑国内再搞一台服务器放db吧，不然上班摸鱼db同步也是个问题... 
接下来还要学习orm的语句（sqlalchemy），sql好像不太用学（优先度不高），但是数据库相关的理论知识要补... （还有个表的迁移工具 alembic 也要学？） 
以及... 我好像能干活了？（错觉）

希望今年能搞一个延迟低一点的... （别3306 晚高峰ping一下500+了

## day13

今天在忙别的（指写文案），没咋看。咕咕咕... 
看了个环境变量和事件，后端事件。虽然不知道和js那个event有啥关系。

## day12

本来打算看orm的 跑去看了一下 fastapi和静态页面。。。不用jinja2好像就是不能传回值，不过有其他方式。
以及又学了一下框架的高级用法？挺有意思的。
知道了提交表单的流程，（对于登陆页面又近了一步） x 。
已到了一个basic auth（不知道原理）。
请求返回页面，以及websockets的简单应用。。

哎 慢慢来吧。真是急不来。。

---

## day11

追加一个桐人酱给我做的 dolist.jpg （md我也直接毛过来了）

```
https://www.yuque.com/kirito-666/cpyl2g/wpkwtg?
```

今天把 sqlalchemy1.4版本的入门语句看了一下

然后简单的试了试用orm建了个sqlite库

好像不能增加字段 要配合alembic （以后在学

用户的注册登录登出页面打算开始做了.jpg

我好像还需要个jinja2的模板库来放页面？ 不确定，不懂.jpg

总之 摸了 充实的一天 x

## day10？（大概吧）

看了一天 sqlalchemy 人是懵的 没有db的前置知识 看着有点累

---

## day9

摸了一上午，下午睡醒看了一下官网文档的部署，于是乎想先学一下docker了.jpg

另外官方的高级文档里，好像都是看不太懂的东西... 
打算先找个项目开始一点点啃啃看 
还是在2选1的阶段，都同时看看吧...
```
一个国人项目，跑了一下demo还行
./fastapi_amis_admin/admin/admin.py
这个文件看着很头疼... 
https://github.com/amisadmin/fastapi_amis_admin
```

```
以及这个是作者自己的项目
看起来好复杂，配了好多库... 学习成本好像挺高的...
我还没部署出来，环境就把我卡住了.jpg
https://github.com/tiangolo/full-stack-fastapi-postgresql
```

不知道还有没有什么适合新人的项目，第一次学这种东西最困扰的还是好多第三方库的学习成本... 

---
## day8

入门文档都看完了，接下来打算试试找个项目跟一下了.jpg

进阶教程，同时看吧.jpg

找了三个项目，筛了一下 应该是2选1了.jpg

路由看完了，似懂非懂.jpg 和我理解的分配urls的意思不太一样？ 
一会打算问一下群友那个路径问题.jpg

/app/main.py 

不知道有啥好的解决方案.jpg

## day7
开始学db，应该是学orm？
说起来db我好像看到外键还是啥来着就放一边了 = =

~~另外有个乐子，keyword: 金花姐~~

感觉这段期间就用这个当随便记录好了.jpg

晚间补充： 算是把整套流程过了一遍在sql_app里面。抽时间把这个和security组合起来 应该就是一个能用的东西了 x

另外今天遇到个坑 是包的相对路径问题 看了个一知半解 反正解决了.jpg
```
import os
import sys

# 包的结构问题的莫名其妙解决方案... 
# https://stackoverflow.com/questions/16981921
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine

# 包的结构问题，相对路径
# from . import crud, models, schemas
# from .database import SessionLocal, engine
# 用下面这个没问题
# import crud, models, schemas
# from database import SessionLocal, engine
```

对了，还要追加一点。我的翻译之魂moemoe（误）起来了 x

转念一想，学这个的人多少都会点英语吧... 对吧... 是吧... 没错... 
不过好多技术名词我不知道啥意思，不太好意思给社区文档做汉化 x

等我再学一学的吧.jpg

---
## day6 

非常愉悦的周末，lgd回家了。好似喵，好似。（问就是败人品

新的一周，新的摸鱼。开始继续学习fastapi.jpg
本周计划把新手教程看完，能开始写桐人酱的那个项目吧.jpg
但愿如此 x

（还要学一下xss白名单）

存个私货，py生成文档，自动化。
```
https://cloud.tencent.com/developer/article/1678252
```

富文本
```
https://github.com/phith0n/python-xss-filter
```
---

## day5

```
昨天比赛前看到超哥那一抹微笑，我对着屏幕也笑了，扫去了这两天的阴霾，谁能想到... 
```

难受，昨晚的比赛鏖战将近两小时，还是输了，不甘心啊。
比去年的决赛还要不甘。
从天胡开局的9-1到阳了之后的0-8，昨晚的一轮游，哎。
今年小组赛，那个抗局势的火猫，让我看到了希望。
昨天比赛前看到超哥那一抹微笑，我对着屏幕也笑了，扫去了这两天的阴霾，谁能想到...
结束后又看到超哥的微博，意难平。
去年ti结束后，我就决定今年是我最后一次接触dota了。
无论结果如何，都要回归生活了，不能再这样吊儿郎当。

超哥和我算是同一时期在90016活跃的一批人，年纪也相仿。
那个时候他是天才少年，我是‘网瘾少年’，可笑又可悲。 
11平台出来的时候，大家都在冲分。
我一直和超哥差200多分，那个时候第一次意识到这个分数的差距不是努力能弥补的。
也奠定了我没有步入这个圈子的主要原因，现在的我很庆幸当初自己的选择。
印象很深的是一次接训练之后的对黑，细节记不清了。
他是卡尔，我是VS，赢了。
后来的我退圈了，那就是另一个故事了。
这就是我和超哥仅有的交集。

~~写了删，删了写。这么多年的流水账，记录下来也没意义。就到这里吧，算是给自己一个阶段的总结。~~
我也要为了自己的下一个阶段去努力了。
小超人的夏天彻底结束了，但我的夏天还有很长。

写于翌日清晨
~~- -.-- .-.. --- --- .()~~

---
## day3

### 黑菊指导

譬如http的基础，浏览器的基础什么的
http还是要认真提前补一下。
因为这是对后端来说的直接需求 
或者说是“问题” 本身，
就像刷题时你要先看懂题目 
才能看懂别人的解题报告

**http和浏览器基础，不知道是啥.jpg**

首先知道tcp是流式协议，
知道什么是流式协议。
然后知道http 1.1和2的大致格式，（不知道）
因为1.1是文本格式，
能基本手动拼写出http 1.1的请求和响应。
对于2，知道组成成分，
能看懂浏览器的请求数据和响应数据。
熟练使用一个http请求调试工具（swagger UI也算一个）

**流式协议？ http1.1? 2? 也不知道.jpg** 

**正在学的fastapi有在用swagger ui**

其余的 譬如什么浏览器策略啊 cors啊 可以单独再补 
最好从tcp开始自己实现一遍 http的服务端和客户端 
不用支持所有的特性，主要是基础协议的实现 
这个目的是，能够弄懂“框架之下到底做了什么”，
之后在排查问题或性能优化等场合不至于束手无策 
其中有很多细节，譬如说，服务端生成html的过程中，
前端能否逐步展示，这个是怎么实现的；
前端在下载文件时，如何确定文件的下载进度 
也更能深入理解http2在很多地方为什么要做各种改进

**这部分我如果不咕咕咕再说**

**实现tcp，好像就是socket，细节不知道**

## 总之先学框架.jpg
