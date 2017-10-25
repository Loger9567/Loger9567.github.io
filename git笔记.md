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
+ 克隆仓库
	+ 克隆仓库的时候会同步远程仓库的数据和分支, 并且在本地仓库建立一个 master 分支, 当本地仓库没有变动的时候, master 和 remote/origin/master 都指向远程仓库的 master 分支, 当本地仓库修改了 master 分支, 那么本地的 master 分支往前走, 而本地的 remote/origin/master 分支保持, 不管远程仓库的 remote 分支有没有变动, 只要没有和远程通信, 那么本地的 remote/origin/master 分支位置就不变, 当使用 fetch 同步数据的时候才可能会发生变化. 也就是说`git fetch`会更新 remote/origin/master 索引.

```sh
$ git clone [url]
```

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


#### 9.操作分支

+ 先了解分支的结构
	+ 每次提交对应一个`commit` 对象, 也就是一个快照, 对应一个 `SHA-1`
	+ `commit` 对象包含每一个子目录的校验和信息对象 `tree`
	+ `tree` 对象保存记录实际文件信息的 `blob` 对象
	+ 分支指向 `commit` 对象的校验和 `SHA-1`
	+ `HEAD` 指向正在工作的本地分支

```sh
# 查看所有分支
$ git branch -a
```

+ 新建分支

```sh
$ git branch [branch_name]
```

+ 切换分支 (切换之前`一定要`先提交当前分支修改, 否则会在其他分支被看到和提交)

```sh
# 只切换
$ git checkout [branch_name]

# 新建并切换
$ git checkout -b [branch_name]
```

+ 合并分支
	+ 如果分支`A`可以顺着提交顺序可以走到另一个分支`B`,中间没有分岔,那么`git`合并的时候就直接把`A`的指针移动到`B`, 这个就是 `Fast Forward`
	+ 在分支`A`上 `merge` 分支`B`, 和在分支`B`上 `merge` 分支`A`是不一样的, 如果不是`Fast Forward`, 那会新生成一个`commit`对象, 而进行合并操作时所在的分支将会指向新的`commit`对象.
	+ 合并都是在本地操作的, 不涉及到远程仓库, 除非是要合并远程仓库的分支到本地.`git merge origin/some_branch`

```sh
$ git merge [branch_name]

#i.e. hotfix 是从 master 分支创建的紧急修复, 测试之后合并
$ git checkout master
$ git merge hotfix

```

+ 删除分支
	+ 当修复完成之后可以删除掉分支 hotfix
		+ 如果 hotfix 还没有被 merge, 那么会提交保存, 因为会丢失数据
		+ 可以强制杉树

```sh
$ git branch -d hotfix
```

+ 冲突解决
	+ 当 git 合并发生冲突, 合并结果还没有提交, 需要解决冲突后再提交
	+ git 会在有冲突的文件中加入标准的冲突解决标记, 通过它们来手工定位解决冲突
	+ 手工解决之后只需要将所有冲突的文件重新`add`, 然后`commit`就可以了

+ 管理分支

```sh
# 查看所有分支
$ git branch

# 查看所有分支和最后一次提交对象信息
$ git branch -v

# 查看哪些分支已经被(/没有被)并入当前分支(直接上游) 
$ git branch --merge
$ git branch --no-merged
```

+ 跟踪分支
	+ 从远程分支`checkout`的分支称为跟踪分支(tracking branch). 使用 `git pull`会直接拉取对应的远程分支合并到本地, 使用 `git push` 会自动推送到对应的远程分支.
	+ clone 的时候就会自动创建一个 master 的跟踪分支, 跟踪 origin/master 分支

```sh
$ git checkout --track origin/some_branck_to_be_tracked
# 或者
$ git checkout -b sf origin/some_branck_to_be_tracked
```

+ 分支的衍合(rebase)
	+ 与 merge 对应的另一种合并分支的方法
	+ rebase 将分支`A`中提交的改变,在分支	`B`中重放一遍.也就是将分支`A`的`变化补丁`在`B`中重新打一遍,然后产生一个新的提交, `A`再指向这个新的提交
	+ rebase 的原理是: 回到`A`和`B`的最近公共祖先, 找到要进行 rebase 的分支(假设为`A`) 的后续历次提交记录, 产生一系列补丁, 然后在`base`分支(一般是master, 这里假设为`B`)的最后一个提交对象上逐个`应用`这些补丁, 然后每一个补丁对应生成一个新的提交对象, 这些对象是`B`的直接下游, 然后`A`再指向新生成的最后的对象. 然后就可以用`Fast Forward`合并A和B了.
	+ 好处: 可以得到一个在远程分支上干净应用的补丁. 然后项目的维护这就可以根据这个补丁进行快速合并. 从而把解决分支冲突的责任转移给开发者.
	+ 稍微复杂的应用: rebase 可以放到其他分支进行, 不一定是根据分化之前的分支.
	+ `danger`: 一旦分支中的提交对象发布到公共仓库，就千万不要对该分支进行衍合操作
	
```sh
# 切换到 A 上准备打补丁
$ git checkout A 
# 然后打补丁, 并且基于 B 生成补丁(新的 commit 对象), 它不会改变 B
$ git rebase B 

# 稍复杂的应用
#    master分支出 server 分支, 然后 server 分支处 client 分支
#    接着master,server和client都各种前进, 现在要跳过 server 直接把 client rebase 到 master
#    --onto 指定 base 分支
$ git rebase --onto master server client

# 具体语法: 取出特性分支, 在主分支上重演
$ git rebase [主分支] [特性分支]
```


#### 参考资料
> [Pro Git（中文版）前3个章节](http://git.oschina.net/progit/index.html)




