### Python 代码片段

#### 处理带有 `\u`编码的字符串,转化为汉字

```python
import chardet
s = '[03]\u4fe1\u7528\u5631\u5ba1\u6279'
chardet.detect(s)  # 可以看到是ascii码, 不是unicode
s.decode('unicode-escape').encode('utf-8')  # [03]信用卡审批
# decode('unicode-escape') 将转义的ascii解码为unicode, 相当于在一个中文字符串前加一个 u
# python encode成utf-8如果还是不能在utf-8的网页上显示, 那只用 decode()就可以了.
```




#### windows下文本编辑器读取文件会带一个BOM, 代码去除

```python
import codecs
with open(filepath) as file:
	content = file.read()
	if(content[:3] = condecs.BOM_UTF8:
		content = content[3:]
```