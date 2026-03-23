import os

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
        """3. 规划模块：自主拆解任务步骤（模拟大模型的推理能力）"""
        print("\n【规划模块】开始拆解任务...")
        goal = self.memory["user_goal"]
        
        # 模拟Agent的自主拆解逻辑（实际场景中由大模型实现）
        # 从用户目标中提取要写入的内容（模拟大模型的信息提取能力）
        target_content = "AI Agent测试内容"  # 默认内容
        
        # 查找写入关键词和单引号
        write_index = goal.find("写入")
        if write_index != -1:
            # 查找写入后面的第一个单引号
            quote_start = goal.find("'", write_index)
            if quote_start != -1:
                # 查找下一个单引号，支持中文和英文标点
                quote_end = goal.find("'", quote_start + 1)
                if quote_end != -1:
                    target_content = goal[quote_start + 1:quote_end]
        
        if "创建" in goal and "txt文件" in goal:
            # 检查是否需要写入内容
            if "写入" in goal and "检查" in goal:
                # 拆解出具体步骤
                self.memory["task_steps"] = [
                    "步骤1：创建一个名为agent_test.txt的文件",
                    f"步骤2：向文件中写入指定内容'{target_content}'",
                    "步骤3：检查文件是否存在，验证内容是否正确"
                ]
                # 保存目标内容到记忆中，供执行和反馈模块使用
                self.memory["target_content"] = target_content
            else:
                self.memory["task_steps"] = [
                    "步骤1：创建一个名为agent_test.txt的文件",
                    "步骤2：检查文件是否创建成功"
                ]
        else:
            self.memory["task_steps"] = ["步骤1：无法识别的任务，无法拆解"]
        
        # 输出拆解后的步骤
        print("拆解后的任务步骤：")
        for step in self.memory["task_steps"]:
            print(f"  - {step}")
        return self.memory["task_steps"]

    def execute(self):
        """4. 执行模块：执行拆解后的步骤（模拟工具调用）"""
        print("\n【执行模块】开始执行任务...")
        steps = self.memory["task_steps"]
        result = ""
        
        try:
            # 执行步骤1：创建文件
            if "创建一个名为agent_test.txt的文件" in steps[0]:
                with open("agent_test.txt", "w", encoding="utf-8") as f:
                    # 执行步骤2：写入内容（如果有该步骤）
                    if len(steps) >= 2 and "写入" in steps[1]:
                        content = self.memory.get("target_content", "AI Agent测试内容")
                        f.write(content)
                        result += f"已创建文件并写入内容：{content}；"
                    else:
                        result += "已创建空文件；"
            
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
        
        # 检查文件是否存在
        file_exists = os.path.exists("agent_test.txt")
        content_correct = False
        
        if file_exists:
            # 检查文件内容是否正确
                with open("agent_test.txt", "r", encoding="utf-8") as f:
                    content = f.read()
                    target_content = self.memory.get("target_content", "AI Agent测试内容")
                    if content == target_content:
                        content_correct = True
        
        # 生成反馈
        if file_exists and content_correct:
            self.memory["feedback"] = "✅ 任务完成：文件创建成功，内容写入正确！"
        elif file_exists and not content_correct:
            self.memory["feedback"] = "⚠️ 部分完成：文件创建成功，但内容写入错误！"
        else:
            self.memory["feedback"] = "❌ 任务失败：文件未创建成功！"
        
        print(f"检查结果：{self.memory['feedback']}")
        return self.memory["feedback"]

    def run(self, user_goal):
        """Agent主运行流程：感知→规划→执行→反馈"""
        print("===== AI Agent 开始工作 =====")
        # 完整闭环
        self.perceive(user_goal)    # 感知
        self.plan()                 # 规划
        self.execute()              # 执行
        final_feedback = self.feedback()  # 反馈
        
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
