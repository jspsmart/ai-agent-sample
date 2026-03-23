# Simple AI Agent

一个极简版的AI Agent实现，演示了AI Agent的核心工作流程：感知→规划→执行→反馈。帮您快速理解AI Agent的基本原理。

## 功能特点

- **感知模块**：接收用户目标，转化为结构化信息
- **规划模块**：自主拆解任务步骤（模拟大模型的推理能力）
- **执行模块**：执行拆解后的步骤（模拟工具调用）
- **反馈模块**：检查执行结果是否符合预期

## 安装方法

### 1. 克隆项目

```bash
git clone <项目地址>
cd ai-agent-sample
```

### 2. 创建虚拟环境

```bash
# 在Linux/Mac上
python3 -m venv venv

# 在Windows上
python -m venv venv
```

### 3. 激活虚拟环境

```bash
# 在Linux/Mac上
source venv/bin/activate

# 在Windows上
venv\Scripts\activate
```

### 4. 安装依赖

本项目仅使用Python标准库，无需安装额外依赖：

```bash
pip install -r requirements.txt
```

## 使用示例

### 基本使用

直接运行`app.py`文件即可：

```bash
python3 app.py
```

### 修改用户目标

在`app.py`文件的第122行，可以修改用户目标来测试不同场景：

```python
# 示例1：创建文件并写入内容
user_goal = "帮我创建一个txt文件，写入'AI Agent is my good friend.'，并检查文件是否创建成功"

# 示例2：仅创建文件
user_goal = "帮我创建一个txt文件"
```

## 项目结构

```
ai-agent-sample/
├── app.py          # 主程序文件
├── requirements.txt # 依赖文件
├── README.md       # 说明文档
└── venv/           # Python虚拟环境（需自行创建）
```

## 模块说明

### 1. SimpleAIAgent类

AI Agent的核心类，包含以下方法：

- **`__init__()`**：初始化Agent，创建记忆模块
- **`perceive(user_goal)`**：感知用户目标，存储到记忆中
- **`plan()`**：根据用户目标拆解任务步骤
- **`execute()`**：执行拆解后的任务步骤
- **`feedback()`**：检查执行结果，生成反馈
- **`run(user_goal)`**：Agent主运行流程，整合所有模块

### 2. 任务处理流程

1. **接收用户目标**：用户输入要完成的任务
2. **任务拆解**：根据预设逻辑拆解任务为具体步骤
3. **任务执行**：执行拆解后的步骤（创建文件、写入内容等）
4. **结果反馈**：检查执行结果是否符合预期

## 支持的任务类型

### 1. 创建TXT文件并写入内容

用户目标：`"帮我创建一个txt文件，写入'AI Agent测试内容'，并检查文件是否创建成功"`

执行步骤：
- 步骤1：创建一个名为agent_test.txt的文件
- 步骤2：向文件中写入指定内容'AI Agent测试内容'
- 步骤3：检查文件是否存在，验证内容是否正确

### 2. 仅创建TXT文件

用户目标：`"帮我创建一个txt文件"`

执行步骤：
- 步骤1：创建一个名为agent_test.txt的文件
- 步骤2：检查文件是否创建成功

## 注意事项

1. 本项目仅为演示AI Agent的基本工作原理，实际场景中任务拆解和执行逻辑应由大模型和工具调用系统实现
2. 目前仅支持创建TXT文件相关的任务
3. 执行结果会在控制台输出，同时创建/修改当前目录下的`agent_test.txt`文件
4. 项目使用Python 3.6+，建议使用最新版本的Python

## 扩展建议

- 集成大模型API，实现更智能的任务拆解
- 增加更多工具调用功能（如文件操作、网络请求等）
- 实现长期记忆功能，存储历史任务和结果
- 添加配置文件，便于自定义Agent行为

## 许可证

本项目采用MIT许可证，可自由使用和修改。# ai-agent-sample
