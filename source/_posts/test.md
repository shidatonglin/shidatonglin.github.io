---
title: Hexo主题插入音乐之aplayer音乐播放器
copyright: true
date: 2019-05-28 21:39:08
categories:
tags:
---



Hello My Picture
![](https://i.loli.net/2019/05/28/5ced5141f25fa18202.jpg)


163 music

<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=1352962983&auto=1&height=66"></iframe>


使用meeting的一首歌
网易云音乐
{% meting "28754098" "netease" "song" "theme:#555" "mutex:true" "listmaxheight:340px" "preload:auto" %}

酷狗
{% meting "#hash=D351FD0A166BCC1DDDC8EE7D7ABBAAC2&album_id=15823139" "kugou" "song" "theme:#555" "mutex:true" "listmaxheight:340px" "preload:auto" %}

baidu的歌
{% meting "313341" "baidu" "song" "theme:#555" "mutex:true" "listmaxheight:340px" "preload:auto" %}

下面是歌单
{% meting "627070825" "netease" "playlist" "theme:#555" "mutex:true" "listmaxheight:340px" "preload:auto" %}


使用 hexo-tag-aplayer 插件
hexo-tag-aplayer 就是将 APlayer 内嵌入博客页面的 Hexo 插件。

安装执行：

$ npm install --save hexo-tag-aplayer
1
原先 hexo-tag-aplayer 不支持 MetingJS，使得需要图片url，音乐url等等参数，操作起来都很麻烦，需要去音乐网站扒音乐播放链接或者下载下来存储在七牛云或本地，要了解具体参数和使用可以查看其中文文档了解。

MeingJS 支持 (3.0 新功能)
MetingJS 是基于Meting API 的 APlayer 衍生播放器，引入 MetingJS 后，播放器将支持对于 QQ音乐、网易云音乐、虾米、酷狗、百度等平台的音乐播放。

如果想在本插件中使用 MetingJS，请在 Hexo 配置文件 _config.yml 中设置：

aplayer:
  meting: true
1
2
接着就可以 在文章中使用 MetingJS 播放器了，例如打开网易云音乐网站找到这首coldplay的《Viva la Vida》，从url中可以得到其id为3986040，按下面格式即可使用：

{% meting "3986040" "netease" "song" "theme:#555" "mutex:true" "listmaxheight:340px" "preload:auto" %}
1
​

再来一个歌单模板：

{% meting "627070825" "netease" "playlist" "theme:#555" "mutex:true" "listmaxheight:340px" "preload:auto" %}
1
​

有关选项列表如下:

选项	默认值	描述
id	必须值	歌曲 id / 播放列表 id / 相册 id / 搜索关键字
server	必须值	音乐平台: netease, tencent, kugou, xiami, baidu
type	必须值	song, playlist, album, search, artist
fixed	false	开启固定模式
mini	false	开启迷你模式
loop	all	列表循环模式：all, one,none
order	list	列表播放模式： list, random
volume	0.7	播放器音量
lrctype	0	歌词格式类型
listfolded	false	指定音乐播放列表是否折叠
storagename	metingjs	LocalStorage 中存储播放器设定的键名
autoplay	true	自动播放，移动端浏览器暂时不支持此功能
mutex	true	该选项开启时，如果同页面有其他 aplayer 播放，该播放器会暂停
listmaxheight	340px	播放列表的最大长度
preload	auto	音乐文件预载入模式，可选项： none, metadata, auto
theme	#ad7a86	播放器风格色彩设置
--------------------- 