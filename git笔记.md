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

### 2. 