import os
import json
import ollama
import platform

class SimpleAIAgent:
    """极简版AI Agent，实现感知、规划、执行、反馈闭环"""
    
    def __init__(self):
        # 1. 记忆模块：存储任务相关信息（短期记忆）
        self.memory = {
            "user_goal": "",       # 用户目标
            "task_steps": [],      # 拆解后的任务步骤
            "execution_result": "",# 执行结果
            "feedback": ""         # 反馈/检查结果
        }

    def perceive(self, user_goal):
        """2. 感知模块：接收用户目标，转化为结构化信息"""
        print(f"【感知模块】接收到用户目标：{user_goal}")
        self.memory["user_goal"] = user_goal
        return True

    def plan(self):
        """3. 规划模块：使用本地Ollama模型进行任务理解和拆解"""
        print("\n【规划模块】开始拆解任务...")
        goal = self.memory["user_goal"]
        
        try:
            # 获取当前操作系统信息
            current_os = platform.system()
            
            # 动态获取当前用户的桌面路径
            default_desktop = ""
            if current_os == "Darwin":  # macOS
                # 使用expanduser获取当前用户的桌面路径
                default_desktop = os.path.expanduser('~/Desktop/')
                path_separator = "/"
            elif current_os == "Windows":
                # Windows系统使用当前用户的桌面路径
                default_desktop = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', '')
                path_separator = "\\"
            elif current_os == "Linux":
                # Linux系统使用当前用户的桌面路径
                default_desktop = os.path.expanduser('~/Desktop/')
                path_separator = "/"
            else:
                default_desktop = "./"
                path_separator = "/"
            
            print(f"💻 当前操作系统：{current_os}")
            print(f"🗂️ 当前用户桌面路径：{default_desktop}")
            
            # 使用本地Ollama模型进行任务理解和拆解
            prompt = f"""
            请详细分析以下用户目标，并生成执行计划：
            用户目标：{goal}
            当前操作系统：{current_os}
            当前用户桌面路径：{default_desktop}
            
            要求：
            1. 分析任务类型（如：文件操作、信息查询、数据处理等）
            2. 提取关键参数（如：文件名、内容、路径等）
            3. 拆解为具体的、可执行的步骤
            4. 使用JSON格式输出，包含以下字段：
               - task_type: 任务类型
               - params: 关键参数对象
               - steps: 步骤数组
            5. 每个步骤是一个字符串，格式为"步骤X：具体操作"
            6. 对于文件操作任务：
               - 如果用户提到"桌面"，请使用提供的当前用户桌面路径：{default_desktop}
               - 路径格式必须使用当前操作系统的格式：
                 * macOS/Linux使用正斜杠(/)作为路径分隔符
                 * Windows使用反斜杠(\)作为路径分隔符
            
            示例输出（文件创建任务 - macOS）：
            {{
                "task_type": "file_creation",
                "params": {{
                    "path": "{default_desktop}",
                    "filename": "agent_test.txt",
                    "content": "测试内容",
                    "action": "create_and_write"
                }},
                "steps": [
                    "步骤1：在桌面路径{default_desktop}创建一个名为agent_test.txt的文件",
                    "步骤2：向文件中写入内容'测试内容'",
                    "步骤3：检查文件是否创建成功并验证内容"
                ]
            }}
            
            示例输出（仅查询任务）：
            {{
                "task_type": "information_query",
                "params": {{
                    "query": "什么是AI Agent"
                }},
                "steps": [
                    "步骤1：查询'什么是AI Agent'的相关信息"
                ]
            }}
            """
            
            # 调用本地Ollama模型
            response = ollama.generate(
                model="qwen3:latest",  # 可以替换为您本地安装的模型名称
                prompt=prompt,
                format="json"
            )
            
            # 解析模型输出
            result = json.loads(response["response"])
            # print(f"解析模型后输出result={result}")
            # 存储任务信息
            self.memory["task_type"] = result.get("task_type", "unknown")
            self.memory["task_params"] = result.get("params", {})
            self.memory["task_steps"] = result.get("steps", [])
            
            # 输出模型分析结果
            print(f"🎯 任务类型：{self.memory['task_type']}")
            if self.memory['task_params']:
                print(f"📋 关键参数：{self.memory['task_params']}")
            
        except Exception as e:
            print(f"⚠️ 调用Ollama模型失败，使用默认逻辑：{str(e)}")
            # 回退到原始的硬编码逻辑
            target_content = "AI Agent测试内容"  # 默认内容
            
            write_index = goal.find("写入")
            if write_index != -1:
                quote_start = goal.find("'", write_index)
                if quote_start != -1:
                    quote_end = goal.find("'", quote_start + 1)
                    if quote_end != -1:
                        target_content = goal[quote_start + 1:quote_end]
            
            if "创建" in goal and "txt文件" in goal:
                if "写入" in goal and "检查" in goal:
                    self.memory["task_steps"] = [
                        "步骤1：创建一个名为agent_test.txt的文件",
                        f"步骤2：向文件中写入指定内容'{target_content}'",
                        "步骤3：检查文件是否存在，验证内容是否正确"
                    ]
                    self.memory["target_content"] = target_content
                else:
                    self.memory["task_steps"] = [
                        "步骤1：创建一个名为agent_test.txt的文件",
                        "步骤2：检查文件是否创建成功"
                    ]
            else:
                self.memory["task_steps"] = ["步骤1：无法识别的任务，无法拆解"]
        
        # 输出拆解后的步骤
        print("\n【规划模块】任务拆解结果：")
        print(f"解析模型后输出result=》{result}")
        if self.memory["task_steps"]:
            print("拆解后的任务步骤：")
            for step in self.memory["task_steps"]:
                print(f"  - {step}")
        else:
            print("⚠️ 无法拆解任务，使用默认逻辑") 
            self.memory["task_params"] = result.get("params", {})
        return self.memory["task_steps"]

    def execute(self):
        """4. 执行模块：根据任务类型动态执行拆解后的步骤"""
        print("\n【执行模块】开始执行任务...")
        task_type = self.memory.get("task_type", "unknown")
        params = self.memory.get("task_params", {})
        steps = self.memory["task_steps"]
        result = ""
        
        try:
            # 根据任务类型执行不同的逻辑
            if task_type == "file_creation":
                # 文件创建任务
                filename = params.get("filename", "agent_test.txt")
                content = params.get("content", "")
                action = params.get("action", "create")
                path = params.get("path", "")  # 获取指定路径
                
                # 根据操作系统设置默认桌面路径
                if not path:
                    current_os = platform.system()
                    if current_os == "Darwin":  # macOS
                        path = os.path.expanduser('~/Desktop/')
                    elif current_os == "Windows":
                        path = os.path.join(os.environ.get('USERPROFILE', ''), 'Desktop', '')
                    elif current_os == "Linux":
                        path = os.path.expanduser('~/Desktop/')
                    else:
                        path = "./"
                
                # 构建完整的文件路径
                full_path = filename
                if path:
                    full_path = os.path.join(path, filename)
                    # 确保路径存在
                    os.makedirs(os.path.dirname(full_path), exist_ok=True)
                
                print(f"📄 执行文件操作任务：{action}")
                print(f"   - 路径：{path if path else '当前目录'}")
                print(f"   - 文件名：{filename}")
                print(f"   - 完整路径：{full_path}")
                print(f"   - 内容：{content}")
                
                if action == "create" or action == "create_and_write":
                    with open(full_path, "w", encoding="utf-8") as f:
                        if content:
                            f.write(content)
                            result += f"已在路径{path if path else '当前目录'}创建文件{filename}并写入内容；"
                        else:
                            result += f"已在路径{path if path else '当前目录'}创建空文件{filename}；"
                elif action == "write":
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)
                        result += f"已向路径{path if path else '当前目录'}下的文件{filename}写入内容；"
                
            elif task_type == "information_query":
                # 信息查询任务
                query = params.get("query", "")
                print(f"🔍 执行信息查询：{query}")
                
                try:
                    # 调用本地Ollama模型进行信息查询（流式输出）
                    prompt = f"请详细回答以下问题：{query}"
                    
                    # 启用流式输出
                    response_stream = ollama.generate(
                        model="qwen3:latest",  # 使用本地qwen3模型
                        prompt=prompt,
                        stream=True  # 关键参数，开启流式输出
                    )
                    
                    # 初始化查询结果
                    query_result = ""
                    print(f"📚 查询结果：")
                    
                    # 遍历流式响应，逐块获取和输出结果
                    for chunk in response_stream:
                        chunk_content = chunk["response"].strip()
                        if chunk_content:
                            # 实时输出到控制台
                            print(chunk_content, end="", flush=True)
                            # 拼接完整结果
                            query_result += chunk_content
                    
                    print()  # 输出换行符
                    self.memory["query_result"] = query_result.strip()
                    result += f"已查询信息：{query}；"
                except Exception as e:
                    error_msg = f"查询失败：{str(e)}"
                    print(f"⚠️ {error_msg}")
                    self.memory["query_result"] = error_msg
                    result += error_msg
            
            else:
                # 默认执行逻辑，兼容旧版本
                if steps and len(steps) > 0:
                    # 检查是否是文件创建相关任务
                    if any("创建" in step and "文件" in step for step in steps):
                        filename = "agent_test.txt"
                        content = ""
                        
                        # 提取文件名
                        for step in steps:
                            if "名为" in step and "的文件" in step:
                                name_start = step.find("名为") + 2
                                name_end = step.find("的文件", name_start)
                                if name_start > 1 and name_end > name_start:
                                    filename = step[name_start:name_end]
                        
                        # 提取内容
                        for step in steps:
                            if "写入" in step and "'" in step:
                                content_start = step.find("'")
                                content_end = step.find("'", content_start + 1)
                                if content_start != -1 and content_end != -1:
                                    content = step[content_start + 1:content_end]
                        
                        # 执行文件操作
                        with open(filename, "w", encoding="utf-8") as f:
                            if content:
                                f.write(content)
                                result += f"已创建文件{filename}并写入内容；"
                            else:
                                result += f"已创建空文件{filename}；"
            
            self.memory["execution_result"] = result
            print(f"执行结果：{result}")
            return True
        
        except Exception as e:
            self.memory["execution_result"] = f"执行失败：{str(e)}"
            print(f"执行失败：{str(e)}")
            return False

    def feedback(self):
        """5. 反馈/评估模块：检查执行结果是否符合预期"""
        print("\n【反馈模块】开始检查执行结果...")
        
        task_type = self.memory.get("task_type", "unknown")
        params = self.memory.get("task_params", {})
        
        if task_type == "file_creation":
            # 文件创建任务的反馈
            filename = params.get("filename", "agent_test.txt")
            expected_content = params.get("content", "")
            
            # 检查文件是否存在
            file_exists = os.path.exists(filename)
            content_correct = False
            actual_content = ""
            
            if file_exists:
                # 检查文件内容是否正确
                with open(filename, "r", encoding="utf-8") as f:
                    actual_content = f.read()
                    if expected_content:
                        content_correct = (actual_content == expected_content)
                    else:
                        content_correct = True  # 空文件视为正确
            
            # 生成反馈
            if file_exists and content_correct:
                if expected_content:
                    self.memory["feedback"] = f"✅ 任务完成：文件{filename}创建成功，内容写入正确！"
                else:
                    self.memory["feedback"] = f"✅ 任务完成：文件{filename}创建成功！"
            elif file_exists and not content_correct:
                self.memory["feedback"] = f"⚠️ 部分完成：文件{filename}创建成功，但内容写入错误！\n   预期：{expected_content}\n   实际：{actual_content}"
            else:
                self.memory["feedback"] = f"❌ 任务失败：文件{filename}未创建成功！"
        
        elif task_type == "information_query":
            # 信息查询任务的反馈
            query_result = self.memory.get("query_result", "")
            if query_result:
                self.memory["feedback"] = f"✅ 任务完成：信息查询结果如下\n\n{query_result}"
            else:
                self.memory["feedback"] = "✅ 任务完成：信息查询已执行！"
        
        else:
            # 默认反馈逻辑
            self.memory["feedback"] = "✅ 任务执行完成！"
        
        print(f"检查结果：{self.memory['feedback']}")
        return self.memory["feedback"]

    def run(self, user_goal):
        """Agent主运行流程：感知→规划→执行→反馈"""
        print("===== AI Agent 开始工作 =====")
        # 完整闭环
        try:
            self.perceive(user_goal)    # 感知
            self.plan()                 # 规划
            self.execute()              # 执行
            final_feedback = self.feedback()  # 反馈
        except Exception as e:
            self.memory["feedback"] = f"运行过程中发生错误：{str(e)}"
            final_feedback = self.memory["feedback"] + ""
        
        print("\n===== AI Agent 工作结束 =====")
        print(f"最终结果：{final_feedback}")
        return final_feedback

# ------------------- 测试运行 -------------------
if __name__ == "__main__":
    # 实例化Agent
    agent = SimpleAIAgent()
    
    # 通过CLI获取用户目标
    print("请输入您的目标（例如：帮我创建一个txt文件，写入'测试内容'，并检查文件是否创建成功）：")
    user_goal = input().strip()
    
    # 如果用户没有输入，使用默认目标
    if not user_goal:
        user_goal = "帮我创建一个txt文件，写入'AI Agent测试内容'，并检查文件是否创建成功"
    
    # 运行Agent
    agent.run(user_goal)
