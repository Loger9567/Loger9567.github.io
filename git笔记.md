# git学习笔记

#### 1. 配置文件修改--设置和查看用户信息等操作

+ git 的配置分为系统, 用户和项目3级, 分别对应的文件是: `/etc/gitconfig`, `~/.gitconfig` 和项目中的 `.git/config`; 使用 `--global` 更改的是用户级别的配置, 对该用户的所有项目生效.

```sh
# 设置
$ git config --global user.name "Uncaught ReferenceError"
$ git config --global user.email loger9567@gmail.com

# 查看
$ git config --list
$ git config user.name
```

#### 2. 查看提交记录

```sh
# 查看最后一次提交
$ git last

# 查看所有
$ git log

# 查看最近2次提交
$ git log -2

# 查看提交简要信息(增改行数统计)
$ git log --stat

# 在同一行显示一个提交
$ git log --pretty=oneline

# 显示图形 --graph
$ git log --pretty=format:"%h %s" --graph

#使用 format
$ git log --pretty=format: "%h - %an, %ar : %s"
选项 说明
    %H 提交对象（commit）的完整哈希字串
    %h 提交对象的简短哈希字串
    %T 树对象（tree）的完整哈希字串
    %t 树对象的简短哈希字串
    %P 父对象（parent）的完整哈希字串
    %p 父对象的简短哈希字串
    %an 作者（author）的名字
    %ae 作者的电子邮件地址
    %ad 作者修订日期（可以用 -date= 选项定制格式）
    %ar 作者修订日期，按多久以前的方式显示
    %cn 提交者(committer)的名字
    %ce 提交者的电子邮件地址
    %cd 提交日期
    %cr 提交日期，按多久以前的方式显示
    %s 提交说明
```

#### 3.修改最后一次提交

+ 使用当前暂存区的快照进行提交, 如果没有新的改动的话, 相当于可以更新 comment. 使用参数 `--amend`

```sh
$ git commit -m "mistake commit"
$ git add right_file.txt
$ git commit --amend
```


#### 4.取消已暂存的文件

```sh
$ git reset HEAD <file>
$ git unstage <file>
```


#### 5.从暂存区恢复文件

+ 从暂存区检出

```sh
$ git checkout -- <file>
```

#### 6. 查看分支信息

```sh
# 查看所有分支
$ git branch -a
```


#### 7. 远程仓库操作
+ 查看远程仓库

```sh
# 使用 git clone 之后会自动添加 origin 为远程仓库
$ git remote

# 加 -v 或者 --verbose显示对应克隆地址
$ git remote -v
```

+ 添加远程仓库

```sh
# 可以使用 shortname 指代对应仓库地址
$ git remote add [shortname] [url]
```

+ 从远程仓库获取数据
	+ `fetch`: 从远程仓库获取本地没有的数据, 只获取数据, 但是不合并
	+ `pull`: 用于设置了跟踪某个远程分支, 会自动合并到当前分支
		+ 如果没有设置跟踪分支, 使用 `pull` 会提示你先设置 `tracking information for branch`, 一般情况下默认跟踪同名分支
	
```sh
# 1. 使用 fetch
# origin 是 git clone 之后默认创建的remote-name
# 完成后可以
#    从本地访问远程仓库的所有分支
#    将其中的某个分支合并到本地 
#    检出某个分支.
$ git fetch [remote-name]
# 2. 使用 pull
# 设置 tracking information for branch
$ git branch --set-upstream-to=origin/<branch> master
$ git pull
```

+ 推送代码到远程仓库
	+ origin 指定远程仓库, 可能是其他名字, 比如有多个仓库的情况


```sh
# <refspec>的格式为[src_branch]:[dst_branch]
#    :[dst_branch]如果和 src_branch 同名则可以省略, 如果远程不存在同名分支, 则会自动新建.
#    如果[src_branch]为空,则会删除远程分支
$ git push origin <refspec>

# 删除远程上的 mybranch 分支
$ git push origin :mybranch

# 推送当前分支
$ git push origin HEAD:master
```

+ 删除或者重命名远程仓库

```sh
# 重命名
$ git remote rename old_name new_name

# 删除
$ git remote rm [remote_name]
```


#### 8. 打tag

+ 查看tag

```sh
# 查看所有 tag
$ git tag

# 查看指定版本的tag(通配符)
$ git tag -l 'v1.4.2.*'
```

+ 新建tag
	+ `lightweight`: 指向特定提交对象的引用
	+ `annotated`: 存储在仓库中的独立对象, 有自身的校验和信息, 包含标签的名字, 电子邮件和日期及标签说明,运行 GPG 签署或者验证, 推荐.

```sh
# 1. 创建lightweight 标签
$ git tag tag_name
# 查看刚才创建的 tag, 只有响应的提交对象摘要信息
$ git show tag_name

# 2. 创建 annotated 标签 , -a 是 --annotated 缩写
$ git tag -a tag_name -m 'comment info'
# 查看刚才创建的 tag, 就会有更多信息
```

+ 使用GPG签署标签

```sh
# -s 表示 --signed
$ git tag -s tag_name -m "comment info"
```

+ 验证tag

```sh
# 使用 GPG 公钥来验证, -v 表示 --verify
$ git tag -v tag_name
```

+ 推送标签
	+ git push 不会将标签传递到远程服务器, 需要显示命令才能分享
	
```sh
# 提交一个tag
$ git push origin [tagname]

# 提交本地所有新增 tag
$ git push origin --tags
```


