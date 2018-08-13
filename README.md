# movie2345


**大家好，这是我的第二篇博文。这次，我想在第一篇的基础上，依旧使用BeautifulSoup和xlwt，但是这次我会使用python的字典，以此来获取更多的爬取内容。**

## 工具
参考我的[第一篇博文](http://blog.csdn.net/zhaodi_wen/article/details/77418268)


## 内容
**这次我爬取的页面是[2345电影](http://dianying.2345.com/list/------.html)，由于在该页面上存在一个年代选项，具体看下这个截图:**
![](https://github.com/zhaodi-Wen/movie2345/blob/master/img/1.png) 

**所以我之前写了一个只是爬取2017年的电影project（以下我暂且身为1.0版本）,大家可以看下我的[GitHub爬取豆瓣电影排行榜的代码](https://github.com/zhaodi-Wen/DouBanMovie)，他们的框架结构一样，我也把它保存成excel的格式，后来我想对这个代码进行改进，毕竟这里面有那么多个年份的选项，所以就有了一个2.0版本**



## 在1.0版本里

如图  

![](https://github.com/zhaodi-Wen/movie2345/blob/master/img/2.png)

大家可以看到

```
self.urlBase = 'http://dianying.2345.com/list/----2017--.html'  						   #是一个字符串
self.pages = self.getPages()       #是一个数字
self.urls = []                     #是一个list
self.items = [] 				   #同样也是一个list
```
这是单纯爬取一个页面的构造器的设置

## 在2.0版本里面
由于需要爬取2011~2017这7年的数据，所以每个年份就是构成了一个urlbase,每个urlbase对应着一个pages，每个urlbase对应着urls和items(这里的urls和items都是list)。所以在python中拥有1对1的语法很容易就联想到dict(字典)
所以我是这样设置的

```
self.urlbases = []
self.urlbasepages = {}
self.urlbaseurls = {}
self.urlbaseitems = {}
```



**当然在这两个版本里面，对于item的设置是一样的，都是**  

![](https://github.com/zhaodi-Wen/movie2345/blob/master/img/3.png)

所以在这个大方向确定之后，只需要将1.0版本的基础上增加一个

`def getUrlbase(self)`用来获取urlbases(它是一个list)

## **下面是1.0版本和2.0版本的在函数构造上的一些区别**
 

 ### 1. `getUrls():`

**1.0版本前面是这样的：**
```
for page in xrange(1,pages+1):
    url = 'http://dianying.2345.com/list/----2017---'+str(page)+'.html'
    self.urls.append(url)
    self.log.info(u'添加URL:%s到URLS成功'% url)
return self.urls
```
   **2.0版本：**

```
for urlbase,pages in self.urlbasepages.items():
	self.urlbaseurls[urlbase] = []
	for page in xrange(1,int(pages)+1):
	url = urlbase.split('-')[0]+'----'+urlbase.split('-')[4]+'---'+str(page)+'.html'
	self.urlbaseurls[urlbase].append(url)
	self.log.info(u'添加URL：%s到URL：%s成功'%(url,urlbase))
return self.urlbaseurls
```
相比于1.0版本就多了一轮迭代循环和将字典urlbasepages的每一个key对应的value初始化为一个list

 ### 2.`spider()`

**1.0版本前面是这样的：**
 

```
for url in urls:
     htmlContent = self.getResponseContent(url)
```
**2.0版本：**

```
for urlbase,urls in self.urlbaseurls.items():
	self.urlbaseitems[urlbase]=[]
	for url in urls:
		htmlContent = self.getResponseContent(url)
```
还是多了一行循环和一个初始化

### 3. `pipline()`

 **1.0版本前面是这样的：**
	 

```
def piplines(self,items):
    filename = u'2017热门电影.txt'.encode('GBK')
    with open(filename,'w') as fp:
        fp.write('电影名称     电影评分     电影主演  \r')
        for item in items:
```
**2.0版本：**

```
fileName = '电影.txt'.encode('GBK')
	with open(fileName,'w') as fp:
		fp.write('电影名称     电影评分     电影主演  \n')
		for  urlbase,items in self.urlbaseitems.items():
			i= 1
			for item in items:
```
还是一样多了一行循环和初始化

### 4.最后要说的是saveExcel这个自定义模块
 
 **1.0版本：**
```
def run(self,items):
	fileName = u'电影.xls'.encode('GBK')
	book = xlwt.Workbook(encoding='utf8')
	sheet = book.add_sheet('2017',cell_overwrite_ok=True)
```
这生成的只是一个带有一个sheet的excel文件

**2.0版本：**
```
def run(self,urlbaseitems):
	filename = u'电影.xls'.encode('GBK')
	book = xlwt.Workbook(encoding='utf8')
	for urlbase,items in urlbaseitems.items():
		sheetname = urlbase.split('-')[4]
		sheet = book.add_sheet(sheetname,cell_overwrite_ok=True)
```
在每次循环中用是split()将urlbase分割开，目的是为了得到其中的年份数字，作为sheetname，这样就可以得到多个表了。


当然这样运行完后得到的结果是这样的  
![](https://github.com/zhaodi-Wen/movie2345/blob/master/img/4.png)

可以看到评分是没有按照顺序的(当然我也不知道这评分是否可靠😂😂)，原因是该网站也没有按电影评分的高低对电影进行排序

所以为了按照评分进行排序
我在`spider()` 后面加了几行代码：

```
for urlbase in self.urlbaseitems.keys():
	self.urlbaseitems[urlbase].sort(key=lambda item:item.point,reverse= True)
return self.urlbaseitems
```
这里用到了lambda语法,其实他就是个迷你的函数，大家如果想要深入了解dict的各种类型的排序，可以参考[这篇博客](http://blog.csdn.net/ray_up/article/details/42084863)  

这样运行的结果是这样的  
![](https://github.com/zhaodi-Wen/movie2345/blob/master/img/5.png)


**具体的两个版本的源码我已经上传到我的Github上，大家可以参考下😘**

**如果有讲的不清楚的或者错误的，欢迎各位及时指出来，谢谢😀😊!**









