# 手机 Obsidian 同步 GitHub trade 仓库攻略

适用仓库：`krauser1991/trade`

远端地址：

```text
https://github.com/krauser1991/trade.git
```

电脑端已完成：

- 本地目录：`/Users/krauser/Documents/Obsidian Vault/trade`
- Git 远端：`git@github.com:krauser1991/trade.git`
- 分支：`main`
- Obsidian Git 插件 `basePath` 已设置为 `trade`

手机端目标：把 GitHub 上的 `trade` 仓库拉到手机 Obsidian，并能在手机上继续 Pull / Commit / Push。

## 方案选择

推荐优先级：

1. Android：优先用 Obsidian Git 插件，体验相对直接。
2. iPhone / iPad：优先用 Working Copy + Obsidian 文件夹，稳定性通常更好。
3. 如果你只想读，不想在手机上写：直接用 GitHub App 或浏览器看仓库即可。

原因：

- Obsidian Git 插件在桌面端最稳。
- 手机端 Git、认证、后台运行受系统限制，iOS 尤其容易被权限和目录隔离卡住。
- Working Copy 是 iOS 上比较成熟的 Git 客户端，适合管理 Git 仓库。

## 准备 GitHub Token

手机端通常不要用账号密码登录 Git，建议用 GitHub Personal Access Token。

GitHub 创建 Token 路径：

```text
GitHub -> Settings -> Developer settings -> Personal access tokens
```

建议权限：

- 如果仓库是 private：选择能读写该仓库的 `Contents: Read and write`
- 如果使用 classic token：勾选 `repo`

保存后复制 token。它只会完整显示一次。

## Android 方案：Obsidian Git 插件

### 1. 安装 Obsidian

在 Android 手机上安装 Obsidian，打开后创建一个新的 vault，例如：

```text
trade
```

### 2. 安装 Obsidian Git 插件

在 Obsidian 手机端：

```text
Settings -> Community plugins -> Turn on community plugins
Settings -> Community plugins -> Browse -> 搜索 Git -> 安装并启用
```

插件名通常是：

```text
Git
```

作者一般显示为 Vinzent。

### 3. Clone 仓库

打开命令面板：

```text
Ctrl/Cmd + P 或手机端命令面板按钮
```

执行：

```text
Git: Clone an existing remote repo
```

远端地址填写：

```text
https://github.com/krauser1991/trade.git
```

如果要求用户名和密码：

- Username：你的 GitHub 用户名，例如 `krauser1991`
- Password：填 GitHub Token，不是 GitHub 登录密码

clone 目录建议填：

```text
.
```

表示直接克隆到当前 vault 根目录。

### 4. 插件基础设置

进入：

```text
Settings -> Community plugins -> Git -> Options
```

建议配置：

```text
Auto pull on startup: 开启
Pull before push: 开启
Disable push: 关闭
Commit message: mobile backup: {{date}}
Auto save interval: 0
Auto push interval: 0
```

先不要开自动提交和自动推送，避免误提交一堆临时文件。

### 5. 日常同步流程

每次手机打开 Obsidian 后：

1. 先执行 `Git: Pull`
2. 修改笔记
3. 执行 `Git: Commit all changes`
4. 执行 `Git: Push`

如果你在电脑和手机都会改同一份笔记，务必养成：

```text
先 Pull，再写；写完 Commit + Push
```

## iPhone / iPad 推荐方案：Working Copy

iOS 上更推荐这个组合：

```text
Working Copy 管 Git
Obsidian 管编辑
```

### 1. 安装 App

安装：

- Obsidian
- Working Copy

### 2. 在 Working Copy 克隆仓库

打开 Working Copy：

```text
Repositories -> + -> Clone repository
```

仓库地址：

```text
https://github.com/krauser1991/trade.git
```

认证方式：

- GitHub 登录授权，或
- 用户名 + GitHub Token

分支选择：

```text
main
```

### 3. 让 Obsidian 打开 Working Copy 的仓库

在 Obsidian 里选择：

```text
Open folder as vault
```

然后从文件选择器里找到 Working Copy 提供的 `trade` 仓库目录。

如果 Obsidian 无法直接选中 Working Copy 目录，可以使用 Working Copy 的分享/文件夹集成功能，把仓库暴露到 iOS Files，再让 Obsidian 打开。

### 4. iOS 日常同步流程

推荐流程：

1. 打开 Working Copy
2. Pull 最新内容
3. 打开 Obsidian 写笔记
4. 回到 Working Copy
5. 查看 Changes
6. Commit
7. Push

Commit message 可以写：

```text
docs(trade): 手机更新交易笔记
```

## 如果坚持 iOS 直接用 Obsidian Git 插件

可以试，但不作为首选。

步骤和 Android 类似：

1. Obsidian 安装 Git 插件
2. 使用 HTTPS 地址 clone：

```text
https://github.com/krauser1991/trade.git
```

3. 密码使用 GitHub Token
4. 每次同步手动执行 Pull / Commit / Push

如果遇到认证失败、插件无响应、无法 clone，直接切换到 Working Copy 方案。

## 常见问题

### Authentication failed

原因通常是把 GitHub 登录密码当成 Git 密码了。

解决：

- Username 填 GitHub 用户名
- Password 填 GitHub Token
- 确认 Token 有仓库读写权限

### Push 被拒绝

常见原因：

- 电脑端先 push 了新内容，手机还没 pull
- 手机和电脑改了同一份文件

解决：

1. 先 Pull
2. 如果有冲突，手动打开冲突文件处理
3. 再 Commit
4. 再 Push

### Obsidian Git 提示没有仓库

检查当前手机 vault 是否就是 clone 下来的 `trade` 仓库目录。

仓库根目录里应该能看到：

```text
.git
```

如果你把仓库 clone 到 vault 的子目录，插件可能需要设置 `basePath`。

### 手机和电脑内容不一致

按这个顺序处理：

1. 电脑端确认已 push
2. 手机端执行 Pull
3. 如果还是没有，检查手机打开的是不是同一个 vault 目录

### 不想同步 tmp 文件

当前仓库里已经包含 `tmp/pdfs` 等产物。如果后面觉得手机端同步太慢，可以在电脑端调整 `.gitignore`，再统一清理仓库。

不要在手机端随便删除 `tmp` 后直接 push，除非确认这些文件不再需要。

## 推荐工作流

电脑端做重活：

- 批量生成 PDF
- 大量整理资料
- 处理冲突
- 推送大文件

手机端做轻量记录：

- 临时想法
- 盘中观察
- 晚上复盘补充
- 小段交易纪律修订

手机端每次使用：

```text
Pull -> 写笔记 -> Commit -> Push
```

电脑端每次使用：

```text
Pull -> 写/整理 -> Commit -> Push
```

只要坚持先 Pull 后写，就能少掉大部分冲突。

## 当前仓库信息备忘

```text
GitHub: https://github.com/krauser1991/trade
HTTPS clone: https://github.com/krauser1991/trade.git
SSH clone: git@github.com:krauser1991/trade.git
Branch: main
```
