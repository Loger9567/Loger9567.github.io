### Python 代码片段

#### 处理带有 `\u`编码的字符串,转化为汉字

```python
import chardet
s = '[03]\u4fe1\u7528\u5631\u5ba1\u6279'
chardet.detect(s)  # 可以看到是ascii码, 不是unicode
s.decode('unicode-escape').encode('utf-8')  # [03]信用卡审批
# decode('unicode-escape') 将转义的ascii解码为unicode, 相当于在一个中文字符串前加一个 u
```




