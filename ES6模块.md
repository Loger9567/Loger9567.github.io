ES6 模块
---

### 1. Overview
##### JavaScript很早就有模块的概念了, 但是在之前是通过第三方库(CommonJS,AMD)实现的, ES6将模块内置的JavaScript 语言中.
##### 在 ES6中模块和文件一一对应, 有2种方式可以从模块到处变量和函数, 并且这两种方式可以混用, 不过推荐分开使用

#### 1.1 一个模块中多个 export
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

#### 1.2 一个模块单个 export
##### 可以只有一个默认的 export
##### 注意没有分号, 可以是匿名的
```JavaScript
export default funciton(){} //导出函数,注意没有分号
export default class{}  //导出类, 注意没有分号
```

#### 1.3 浏览器中: 使用 script 标签和使用模块对比
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


### 2. JavaScript中的模块

##### 一个模块就是一段代码, 在加载的时候执行
##### 这段代码中可以有变量和函数声明, 这些声明默认作用域属于这个模块, 可以使用 export给其他模块导入
##### 一个模块可以从其他模块中导入内容, 可以通过如下方式(都是字符串)导入, 默认是 js 文件
	+ 相对路径 ('../model/user')
	+ 绝对路径 ('/lib/js/utils')
	+ 已经配置的模块名 ('utils')
##### 多次导入同一个模块, 以第一次导入的为准

#### 2.1 ECMAScript5中的模块
##### ECMAScript5 中最重要的2中不互相兼容的模块标准:
	+ CommonJS
	+ AMD (Asynchronous Module Definition)

##### CommonJS
	+ Node.js 中主要采用了这个标准, 只有很少部分 feature 没有使用
	+ 主要特点: 
		+ 语法简介; 
		+ 适合服务器和同步加载

##### AMD
	+ 最流行的实现是 RequireJS
	+ 主要特点: 
		+ 略复杂的语法, 使得 AMD 不需要使用 eval(); 
		+ 适用于浏览器和异步加载

#### 2.2 ECMAScript6中的模块
##### ECMAScript6的目标是创建 CommonJS 和 AMD 用户都能接受的方式:
	+ 像 CommonJS 一样简洁的语法, 单个exports优先并且能解决循环依赖
	+ 像 AMD 一样直接支持异步加载和配置模块加载
##### 将模块内置到语言中让ES6拥有比 CommonJS 和 AMD 更强大的能力
	+ 比 CommonJS 语法更简洁
	+ 结构可以被静态分析(用作静态检查和优化等)
	+ 循环依赖检查比 CommonJS 更加强大
##### ES6模块标准分为2个部分
	+ 声明语法部分(用来 import 和 export)
	+ 程序化加载API(用来配置模块如何加载以及条件化加载)

### 3. ES6模块基础
##### 有2种export 方式
	+ named export : several per module
	+ default export : one per module
#### 3.1 Named Module
##### 在一个模块中通过在前面加上 export 前缀导出多个变量,函数或者类, export 通过它们的名字来区分这些需要导出的 item, 所以称为 named export 

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

#### 3.2 Default exports
##### 一个 ES6 模块可以选择一个 default export, default exports 特别容易 import

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
##### 有2种 default export style
	+ labeling declaration : 如上面myFunc 和 MyClass 中 function 和 Class 的名字可以去掉也可以加上, 但是建议匿名, 因为这样能让 `export default` 的操作对象变成一个表达式, 而不是一个命名的声明(解析其实也会将它们的匿名版作为表达式, 这样可能会造成不一致, 甚至引入新的声明形式), 可以用`()` 将export default 后面的部分写成一个表达式, 那么后面就可以加分号了.
	+ exporting values directly : 通过表达式来产生值,形如: `export default expression`

```JavaScript
//labeling declaration
export default (function(){});
export default (class{}); 

//exporting values directly
export default 'abc';
export default foo();
export default /^xyz$/;
export default 5*7;
export default {no: false, yes:true};
```
`export default expression` 相当于:
```JavaScript
const __default__ = expression;
export {__default__ as default };   //这个 export 语句在后文介绍
```

显然, 第二种方式, 当变量如下声明的时候就不知道哪一个是 default export 了:
```JavaScript
export default const foo = 1,bar=2, baz=3;  //not legal js
```

#### 3.3 import 和 export 必须时候 top level 的
+ 后面会讲到 ES6 模块的结构是 static 的,不能条件地 import 或者 export一些东西, 这样做有很多好处, 同时这也是句法强制的.

```JavaScript
if(Math.random()){
	import 'foo';  //SyntaxError
}
//不能将 import 和 export 嵌套在一个 block 里面
{
	import 'foo'; //syntax error
}
```

#### 3.4 import 会 hoisted
类似 js 的变量提升, 模块的 import 将会被移动到当前作用域的开始, 所以在哪里声明都没关系.

```JavaScript
foo();  //it works!
import {foo} from 'myModule'; 
```

#### 3.5 import 是 export 的 read-only view
###### ES6模块 import 进入后, 在被 import 的模块中声明的变量依然有效. 类似于引用一个视图
```JavaScript
//lib.js
export let counter = 3;
export function incCounter(){
	counter ++;
}
//main.js
import {counter, incCounter} from './lib';
/*the imported value `counter` is live*/
console.log(counter);   //3
incCounter();
console.log(counter); //4

```

###### 这样做有以下好处:
+ enable循环依赖, 甚至未检验的 import (后面讲解)
+ 已检验和未检验的 import 工作方式相同(它们都是 indirection的)
+ 可以将代码拆分为多个模块, 并且它将继续工作(如果你不试图去改变 import 的值)

#### 3.6 对循环依赖的支持
+ 如果模块 A 和模块 B满足: A 直接或者间接 import B, 并且 B imoprt A, 那么 A 和 B 就循环依赖了, 这种情况是应该被避免的, 它将导致 A 和 B 被紧紧捆绑.
+ CommonJS中的循环依赖

```JavaScript
//a.js
var b = require('b');
function foo(){
	b.bar();
}
exports.foo = foo;

//b.js
var a = require('a');   //(i)
function bar(){
	if(Math.random()){
		a.foo();   //(ii)
	}
}
exports.bar = bar;
//如果模块 a 先被导入, 在(i)行, 模块 b 中的 a 将在 export 之前获得模块 a 导入的对象. 因此, b 不能在 top level 获得 a.foo, 但是这个属性在 a 执行完成的时候是存在的. 如果 bar() 是在a 执行完成之后调用的, 那么(ii)行能正常工作.
//通常记住:带有循环依赖, 你在模块中将不能获取import的东西, ES6中也是一样
```

+ CommonJS 方法的限制:
	+ Node.js 方式的single value export 不能工作, 因此你需要export single value 而不是 object如: `module.exports = function(){...}` , 如果模块 a 这样导出, 模块 b 的变量 a 在赋值的时候将不会更新而是指向原值
	+ 你将不能直接使用 named export , 因为模块 b 不能像` var foo = require('a').foo` 这样导入 foo, foo 将变成 undefined. 也就是说无法用 foo 引用 a.foo
	+ 总之: 这些限制意味着导入者和导出者都必须注意循环依赖, 并且提供显式支持.

+ ES6中的循环依赖
	+ ES6模块自动支持循环依赖, 也就是说它没有上面 CommonJS 的2点限制, 所以, 你可以像下面一样实现相互依赖的2个模块.

```JavaScript
//a.js
import {bar} from 'b'; //(i)
export funciton foo(){
	bar();   //(ii)
}
//b.js
imoprt {foo} from 'a'; //(iii)
export function bar(){
	if(Math.random()){
		foo(); //(iv)
	}
}
//这段代码能正常工作, 因为之前讲到过 import 是 export 的一个 view, 也就是说即使未检验的 import(就像(ii) 和 (iv) 行中的 bar 和 foo)间接指向了原始数据. 因此从表面上看循环依赖, 无论你在哪里named export (通过未检验的的 import 或者通过模块)都会间接涉及到循环依赖, 并且它总是能工作.
```

### 4. import 和 export 的细节

#### 4.1 import的方式








> 注明: 本文由笔者从[原文](http://exploringjs.com/es6/ch_modules.html)翻译而来, 加上一些个人理解, 引用请注明出处.