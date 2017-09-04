ES6 模块
---

### 1.Overview
+ JavaScript很早就有模块的概念了, 但是在之前是通过第三方库(CommonJS,AMD)实现的, ES6将模块内置的JavaScript 语言中.
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


### 2.JavaScript中的模块

+ 一个模块就是一段代码, 在加载的时候执行
+ 这段代码中可以有变量和函数声明, 这些声明默认作用域属于这个模块, 可以使用 export给其他模块导入
+ 一个模块可以从其他模块中导入内容, 可以通过如下方式(都是字符串)导入, 默认是 js 文件
	+ 相对路径 ('../model/user')
	+ 绝对路径 ('/lib/js/utils')
	+ 已经配置的模块名 ('utils')
+ 多次导入同一个模块, 以第一次导入的为准

#### ECMAScript5中的模块
+ ECMAScript5 中最重要的2中不互相兼容的模块标准:
	+ CommonJS
	+ AMD (Asynchronous Module Definition)

+ CommonJS
	+ Node.js 中主要采用了这个标准, 只有很少部分 feature 没有使用
	+ 主要特点: 
		+ 语法简介; 
		+ 适合服务器和同步加载

+ AMD
	+ 最流行的实现是 RequireJS
	+ 主要特点: 
		+ 略复杂的语法, 使得 AMD 不需要使用 eval(); 
		+ 适用于浏览器和异步加载

#### ECMAScript6中的模块
+ ECMAScript6的目标是创建 CommonJS 和 AMD 用户都能接受的方式:
	+ 像 CommonJS 一样简洁的语法, 单个exports优先并且能解决循环依赖
	+ 像 AMD 一样直接支持异步加载和配置模块加载
+ 将模块内置到语言中让ES6拥有比 CommonJS 和 AMD 更强大的能力
	+ 比 CommonJS 语法更简洁
	+ 结构可以被静态分析(用作静态检查和优化等)
	+ 循环依赖检查比 CommonJS 更加强大
+ ES6模块标准分为2个部分
	+ 声明语法部分(用来 import 和 export)
	+ 程序化加载API(用来配置模块如何加载以及条件化加载)

### 3.ES6模块基础
+ 有2种export 方式
	+ named export : several per module
	+ default export : one per module
#### Named Module
+ 在一个模块中通过在前面加上 export 前缀导出多个变量,函数或者类, export 通过它们的名字来区分这些需要导出的 item, 所以称为 named export 

```JavaScript
/*ES6的方式*/
//lib.js
export const sqrt = Math.sqrt;
export function square(x){
	return x*x;
}
export function diag(x,y){
	return sqrt(square(x) + square(y));
}
//main.js
import {square, diag} from 'lib';
console.log(square(11));  //121
console.log(diag(3,4)); //5

/*CommonJS的方式*/
//lib.js
var sqrt = Math.sqrt;
function square(x){
	return x*x;
}
function diag(x,y){
	return sqrt(square(x) + square(y));
}
module.exports = {
	sqrt: sqrt,
	square: square,
	diag: diag
};
//main.js
var square = require('lib').square;
var diag = require('lib').diag;
console.log(square(11));
console.log(diag(3,4));
```

#### Default exports
+ 一个 ES6 模块可以选择一个 default export, default exports 特别容易 import

```JavaScript
//myFunc.js
export default function(){}
//MyClass.js
export default class {}
//main.js
import myFunc from 'myFunc';
import MyClass from 'MyClass';
myFunc();
const inst = new MyClass();

```
+ 有2种 default export style
	- labeling declaration : 如上面myFunc 和 MyClass 中 function 和 Class 的名字可以去掉也可以加上, 但是建议匿名, 因为这样能让 `export default` 的操作对象变成一个表达式, 而不是一个命名的声明(解析其实也会将它们的匿名版作为表达式, 这样可能会造成不一致, 甚至引入新的声明形式), 可以用`()` 将export default 后面的部分写成一个表达式, 那么后面就可以加分号了.

```JavaScript
export default (function(){});
export default (class{}); 

```
	- exporting values directly : 通过表达式来产生值,形如: `export default expression`
	
```JavaScript
export default 'abc';
export default foo();
export default /^xyz$/;
export default 5*7;
export default {no: false, yes:true};
```







> 注明: 本文由笔者从[原文](http://exploringjs.com/es6/ch_modules.html)翻译而来, 加上一些个人理解, 引用请注明出处.