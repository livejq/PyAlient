<h1 align="center">Pygame Demo</h1>

<br>

<p align="center">
  	<a href="http://hits.dwyl.io/livejq/alient_invasion"><img alt="HitCount" src="http://hits.dwyl.io/livejq/alient_invasion.svg"></a>
  	<a href="https://github.com/livejq/alient_invasion/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/livejq/alient_invasion.svg"></a>
  	<a href="https://www.pygame.org/docs/"><img alt="Struts2" src="https://img.shields.io/badge/Pygame-1.9.4-6aee28"></a>
  	<a href="https://www.python.org/downloads/release"><img alt="Hibernate" src="https://img.shields.io/badge/Python-3.x-254f72"></a>
	<a href="https://github.com/livejq/alient_invasion/blob/master/LICENSE"><img alt="GitHub license" src="https://img.shields.io/github/license/livejq/alient_invasion.svg"></a>
</p>

<br>

<p align="center">
<span>a simple Pygame Demo</span>
</p>

<hr>

对于刚掌握一门高级语言基础的人来说，来点实战来巩固基础是再好不过的了。为此，Python编程：从入门到实践这本书也是本着这个原则才收到了广泛的好评吧。好了，话不多说，来进行最有意思的环节吧。



## 实现效果

背景每次打开位置随机生成：
![attack.png](https://www.livejq.top/img/cut-pic/19-2-20/attack.jpg)

飞船与外星人相撞（飞船可上下左右移动）：
![collide.png](https://www.livejq.top/img/cut-pic/19-2-20/collide.jpg)

<hr>



- [环境配置](#环境配置)
- [项目分析](#项目分析)
  - [难点一：事件控制](#难点一：事件控制)
  - [难点二：群体控制](#难点二：群体控制)
  - [难点三：碰撞检测](#难点三：碰撞检测)
  - [难点四：声音和动画](#难点四：声音和动画)
- [PyInstaller打包exe](#PyInstaller打包exe)
- [致谢](#致谢)
- [参与贡献方式](#参与贡献方式)
- [许可证](#许可证)

<hr>

## 环境配置

上述介绍的书中详细介绍了如何运用pygame模块，不过作者也是考虑到了平均的水平，重点突出了整个项目的构建流程和设计模式，所以涉及到的知识层还是比较浅的。

<br>

- 书中介绍的外星人入侵的游戏书中提供了[源码链接](https://www.nostarch.com/pythoncrashcourse/)下载,不过直接运行一般是会报错的，原因大多是使用的python版本不一（所以不要想太多，还是老老实实自己写吧）。
- pip install --user pygame先安装主要的模块,pip list 查看第三方模块，我这里的pygame是1.9.4版本的，python3.6。
- 编译器有很多，看自己喜好，我用的是wing pro6，pycharm或vs code也还不错。
- 做游戏，找素材可以说是最麻烦的一件事了吧，音效、图标、背景等。我也是找了挺久的，网上很多得注册充钱才能下载，不过好人还是有的，这里我提供一两个。

<br>

[下载一](https://indienova.com/resource)：很精致，不过要钱,看看还行。

[下载二](http://www.aigei.com/)：这个是真的良心网站，不得不折服，得向他学习，不吝啬学习资源。大家都不是只靠自己就可以无所不能的，都是通过互相学习才能成长。



## 项目分析

其实整一个项目可以集中在一个文件，作者为了更加清晰的说明各个模块的作用，将其写成独立的文件。在这里只是分析原理，记录难点，[源码下载](https://github.com/livejq/alient_invasion)。

alien_invasion.py为主程序入口文件。一切与游戏相关的具体操作都在game_function.py，其它的则为其调用的各个模块，有子弹、飞船、外星人、修饰背景、按钮、数据记录面板、初始化设置、动画效果。除此之外还有资源文件目录，有字体、声音、图像和数据文件。

<br>

### 难点一：事件控制

事件有键盘事件和鼠标事件，键盘再细分为按下pygame.KEYDOWN和松开pygame.KEYUP。鼠标有点击事件pygame.MOUSEBUTTONDOWN（其中可以调用pressed_array = pygame.mouse.get_pressed()来去区分是哪个按键被点击了，for index in range(len(pressed_array))，0点击左键,1,2分别是wheel和right），其中键盘中的每个按键输出来其实都有一个唯一的数字表示（使用了ASCII码表，按下字母a输出为97），但它们都可以通过调用pygame.来判断是哪个键被按下或松开。pygame.QUIT叉叉掉、(k后面有个下划线，这里显示不了)K_RIGHT/K_LEFT/K_UP/K_DOWN/K_SPACE/K_q(键盘q)。

用这些可以让小飞船在屏幕里上下左右移动。哦，还有一个重要一点是每个图像都被看做是矩形，加载图像后返回一个矩形对象rect，此对象左上角为x,y。rect可调用-》中间centerx，centery，上下左右top,bottom,right,left，来返回具体位置信息

<br>

### 难点二：群体控制

这里不得不说的一个精灵类pygame.sprite.Sprite，其通常与pygame.sprite.Group一起使用，专门用来控制群体动作。都具有update()/draw()等方法,创建好了精灵之后可以通过Goup对象的add方法一个个加入到组里面。

<br>

### 难点三：碰撞检测

pygame的碰撞检测是建立在精灵间的，所以方法都写在与精灵同一个pygame.sprite包下面,通过提供一对多，多对多相应的检测方法。

多对多：
`collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)`
collisions 返回值是一个字典，每一个子弹对应于被其打中的外星人，所以值是一个列表，包含所有被打中的外星人

一对多：

`alien = pygame.sprite.spritecollideany(ship, aliens)`

<br>

### 难点四：声音和动画

这部分应该算是比较难的了，不过慢慢理解还是很好懂得呢，毕竟也是最有趣的部分。

- 背景音乐

```python
    else:
        print("游戏结束\n\n")
        status.game_active = False
        pygame.mixer.music.load('sound/fail.mp3')
        pygame.mixer.music.play(-1)
```

- 音效

```python
	elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
        shoot_wav = pygame.mixer.Sound('sound/shoot.wav')#加载，格式好像只能是wav
        shoot_wav.set_volume(0.5)#音量
        shoot_wav.play(0)`#播放，-1无限循环，0表示重复0次，即只放一遍
```



- 上述在开始之前还有最重要的一步是初始化（放在setting类中就可以一次初始化了）

```python
		pygame.mixer.init()
        pygame.mixer.music.set_volume(0.6) # 音量`
```



- 动画：就是写了个动画类，很重要

```python
import pygame

class MySprite(pygame.sprite.Sprite):
    def __init__(self, target, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = target
        self.image = None
        self.master_image = None
        self.rect = None
        self.topleft = 0,0
        self.frame = 0
        self.old_frame = -1
        self.frame_width = 1
        self.frame_height = 1
        self.first_frame = 0
        self.last_frame = 0
        self.columns = 1
        self.last_time = 0
        self.isLast = False
        
    def load(self, filename, x, y, width, height, columns):
        self.master_image = pygame.image.load(filename)
        self.frame_width = width
        self.frame_height = height
        self.rect = x,y,width,height
        self.columns = columns
        rect = self.master_image.get_rect()
        self.last_frame = (rect.width // width) * (rect.height // height) - 1 # 行列都是从下标0开始

    def update(self, current_time, rate=80):
        if current_time > self.last_time + rate: # 判断是否该更换帧,rate越大则更换得越慢
            self.frame += 1
            if self.frame > self.last_frame: # 判断此更换的帧是否超过最后一张
                self.isLast = True
            self.last_time = current_time

        if self.frame != self.old_frame and not self.isLast: # 判断若更换了帧且并不是最后一张，则替换原来的帧
            frame_x = (self.frame % self.columns) * self.frame_width
            frame_y = (self.frame // self.columns) * self.frame_height
            rect = ( frame_x, frame_y, self.frame_width, self.frame_height )
            self.image = self.master_image.subsurface(rect) # 新的Surface将从其父级继承调色板，颜色键和alpha设置
            self.old_frame = self.frame
```



## PyInstaller打包exe

- Windows 10下：

![pyinstaller_error.png](https://www.livejq.top/img/cut-pic/19-2-20/pyinstaller_error.png)
对其它文件试着打包可以成功，就这个游戏不行。这个有待研究。

<br>

- Linux Debian下：

```bash
74 INFO: PyInstaller: 3.5
74 INFO: Python: 3.7.4
74 INFO: Platform: Linux-4.19.0-kali5-amd64-x86_64-with-Kali-kali-rolling-kali-rolling
1855 INFO: wrote /media/root/livejq/Python/python36_test/alien_invasion/alien_invasion.spec
1868 INFO: UPX is available.
1870 INFO: Extending PYTHONPATH with paths
['/media/root/livejq/Python/python36_test/alien_invasion',
 '/media/root/livejq/Python/python36_test/alien_invasion']
1870 INFO: checking Analysis
1871 INFO: Building Analysis because Analysis-00.toc is non existent
1871 INFO: Initializing module dependency graph...
1873 INFO: Initializing module graph hooks...
1875 INFO: Analyzing base_library.zip ...
5169 INFO: running Analysis Analysis-00.toc
5207 INFO: Caching module hooks...
5211 INFO: Analyzing /media/root/livejq/Python/python36_test/alien_invasion/alien_invasion.py
6126 INFO: Processing pre-find module path hook   distutils
7428 INFO: Processing pre-safe import module hook   setuptools.extern.six.moves
7850 INFO: Processing pre-find module path hook   site
7851 INFO: site: retargeting to fake-dir '/usr/local/lib/python3.7/dist-packages/PyInstaller/fake-modules'
12214 INFO: Loading module hooks...
12214 INFO: Loading module hook "hook-numpy.py"...
12216 INFO: Loading module hook "hook-pkg_resources.py"...
12588 INFO: Processing pre-safe import module hook   win32com
12773 INFO: Loading module hook "hook-lib2to3.py"...
12776 INFO: Loading module hook "hook-numpy.core.py"...
12888 INFO: Loading module hook "hook-sysconfig.py"...
12898 INFO: Loading module hook "hook-setuptools.py"...
13435 INFO: Loading module hook "hook-OpenGL.py"...
13528 INFO: Loading module hook "hook-pygame.py"...
13529 WARNING: Hidden import "pygame._view" not found!
13529 INFO: Loading module hook "hook-scipy.py"...
13530 INFO: Loading module hook "hook-xml.py"...
13602 INFO: Loading module hook "hook-encodings.py"...
13655 INFO: Loading module hook "hook-distutils.py"...
13656 INFO: Loading module hook "hook-pydoc.py"...
13682 INFO: Looking for ctypes DLLs
14019 INFO: Analyzing run-time hooks ...
14028 INFO: Including run-time hook 'pyi_rth_pkgres.py'
14031 INFO: Including run-time hook 'pyi_rth_multiprocessing.py'
14049 INFO: Looking for dynamic libraries
14668 INFO: Looking for eggs
14668 INFO: Python library not in binary dependencies. Doing additional searching...
14710 INFO: Using Python library /lib/x86_64-linux-gnu/libpython3.7m.so.1.0
14725 INFO: Warnings written to /media/root/livejq/Python/python36_test/alien_invasion/build/alien_invasion/warn-alien_invasion.txt
14817 INFO: Graph cross-reference written to /media/root/livejq/Python/python36_test/alien_invasion/build/alien_invasion/xref-alien_invasion.html
14839 INFO: checking PYZ
14839 INFO: Building PYZ because PYZ-00.toc is non existent
14839 INFO: Building PYZ (ZlibArchive) /media/root/livejq/Python/python36_test/alien_invasion/build/alien_invasion/PYZ-00.pyz
15782 INFO: Building PYZ (ZlibArchive) /media/root/livejq/Python/python36_test/alien_invasion/build/alien_invasion/PYZ-00.pyz completed successfully.
15799 INFO: checking PKG
15799 INFO: Building PKG because PKG-00.toc is non existent
15799 INFO: Building PKG (CArchive) PKG-00.pkg
22935 INFO: Building PKG (CArchive) PKG-00.pkg completed successfully.
22937 INFO: Bootloader /usr/local/lib/python3.7/dist-packages/PyInstaller/bootloader/Linux-64bit/run
22938 INFO: checking EXE
22938 INFO: Building EXE because EXE-00.toc is non existent
22938 INFO: Building EXE from EXE-00.toc
22939 INFO: Appending archive to ELF section in EXE /media/root/livejq/Python/python36_test/alien_invasion/dist/alien_invasion
23120 INFO: Building EXE from EXE-00.toc completed successfully.
```

<br>

linux下打包成功(=H=)，真奇怪呀～

<br>

- pyinstaller命令说明：

![pyinstaller.png](https://www.livejq.top/img/cut-pic/19-2-20/pyinstaller.png)



## 致谢

<br>

感谢这本《Python编程：从入门到实践》的作者~



## 参与贡献方式

<br>

欢迎[issuess](https://github.com/livejq/ssh_demo/issues)



## 许可证

<br>

@[MIT](https://github.com/livejq/alient_invasion/blob/master/LICENSE) License
