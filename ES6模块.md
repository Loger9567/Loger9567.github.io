ES6 模块
---

### Overview
+ JavaScript很早就有模块的概念了, 但是在之前是通过第三方库实现的, ES6将模块内置的JavaScript 语言中.
+ 在 ES6中模块和文件一一对应, 有2种方式可以从模块到处变量和函数, 并且这两种方式可以混用, 不过推荐分开使用

#### 一个模块中多个 export
```JavaScript
//lib.js
export const sqrt = Math.sqrt;
export funciton square(x){
	return x*x;
}
export funciotn diag(x,y){
	return sqrt(squart(x) + squart(y));
}
//main.js
import {square, diag} from 'lib';   //引用方式1
import * from 'lib';  //引用方式2
```

#### 一个模块单个 export
+ 可以只有一个默认的 export
+ 注意没有分号, 可以是匿名的
```JavaScript
export default funciton(){} //导出函数,注意没有分号
export default class{}  //导出类, 注意没有分号
```

#### 浏览器中: 使用 script 标签和使用模块对比
|      | Scripts          | Modules  |
| ------------- |:-------------:| -----:|
| Html element     | \<script\>| \<script type="module"\> |
| Default mode      | non-strict      |   strict |
| Top-level variables  are| global      |   local to module |
| Value of this at top level| window | undefined|
| Executed | synchronously | asynchronously | 
| Declarative imports (import statement) | no | yes|
| Programmatic imports (Promise-based API) | yes | yes |
| File extension	 | .js	| .js | 


### JavaScript中的模块

+ 一个模块就是一段代码, 在加载的时候执行
+ 这段代码中可以有变量和函数声明, 这些声明默认作用域属于这个模块, 可以使用 export给其他模块导入
+ 一个模块可以从其他模块中导入内容, 可以通过如下方式(都是字符串)导入, 默认是 js 文件
 + 相对路径 ('../model/user')
 + 绝对路径 ('/lib/js/utils')
 + 已经配置的模块名 ('utils')
+ 多次导入同一个模块, 以第一次导入的为准







> 注明: 本文由笔者从[原文](http://exploringjs.com/es6/ch_modules.html)翻译而来, 加上一些个人理解, 引用请注明出处.