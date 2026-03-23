#!/bin/bash
# 功能：一键初始化 Git 仓库并推送到 GitHub
# 适用：macOS 系统，需提前安装 Git 并配置 GitHub 账号（已登录）

# 颜色输出函数（增强可读性）
green_echo() {
    echo -e "\033[32m$1\033[0m"
}
red_echo() {
    echo -e "\033[31m$1\033[0m"
}
 
# 步骤1：检查当前目录是否已存在 Git 仓库
if [ -d ".git" ]; then
    red_echo "❌ 当前目录已存在 .git 文件夹，已是 Git 仓库，退出执行！"
    exit 1
fi

# 步骤2：创建 README.md 并写入内容
green_echo "✅ 开始创建 README.md 文件..."
echo "# ai-agent-sample" >> README.md
if [ ! -f "README.md" ]; then
    red_echo "❌ 创建 README.md 失败！"
    exit 1
fi

# 步骤3：初始化 Git 仓库
green_echo "✅ 初始化 Git 仓库..."
git init
if [ $? -ne 0 ]; then
    red_echo "❌ git init 执行失败！请检查 Git 是否安装。"
    exit 1
fi

# 步骤4：添加文件并提交
green_echo "✅ 添加文件并提交第一个版本..."
git add README.md
git commit -m "first commit"
if [ $? -ne 0 ]; then
    red_echo "❌ git commit 失败！请检查 Git 配置（用户名/邮箱）。"
    exit 1
fi

# 步骤5：切换分支为 main
green_echo "✅ 切换分支为 main..."
git branch -M main
if [ $? -ne 0 ]; then
    red_echo "❌ 切换分支失败！"
    exit 1
fi

# 步骤6：添加远程仓库并推送
green_echo "✅ 添加远程仓库并推送代码..."
git remote add origin https://github.com/jspsmart/ai-agent-sample.git
git push -u origin main

# 最终结果判断
if [ $? -eq 0 ]; then
    green_echo "🎉 全部操作完成！代码已成功推送到 GitHub：https://github.com/jspsmart/ai-agent-sample.git"
else
    red_echo "❌ git push 失败！请检查：
    1. GitHub 仓库 https://github.com/jspsmart/ai-agent-sample.git 是否存在；
    2. 本地 Git 是否已配置 GitHub 账号（用户名/密码/SSH 密钥）；
    3. 网络是否正常访问 GitHub。"
    exit 1
fi
