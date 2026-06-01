#存放需要调用大模型（LLM）进行智能推理的节点。

import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from src.schemas import PlannerState, FullTravelPlan

# 强行刷新当前目录的环境变量，防止缓存干扰
load_dotenv(override=True)

# 关键环隔离：防止在启用了本地全局科学上网时导致阿里云报错 ProxyError
os.environ["NO_PROXY"] = "aliyuncs.com,127.0.0.1,localhost"

llm = ChatTongyi(
    model="qwen-plus"
)

# 构建带有显式契约的结构化大模型实例
structured_llm = llm.with_structured_output(FullTravelPlan)

# 编写精细化的 Expert Agent 提示词
itinerary_prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "你是一位深耕【{city}】本地长达10年的金牌资深导游、金牌行程规划师。\n"
        "请根据用户的兴趣偏好：【{interests}】，自适应地为其编排一套精细化、高可行性的单日或多日游玩路线。\n"
        "【严格要求】：必须严格按照给定的 FullTravelPlan 结构返回 JSON，确保时间和人均花费切合实际，拒绝大而化之的空话。"
    )),
    ("user", "我已经提供了我的出游城市和兴趣，请立即为我生成精细化的行程单。")
])


def create_itinerary_agent(state: PlannerState) -> dict:
    """大模型核心编排节点：根据收集到的状态，生产高精度的结构化旅行方案"""
    print(f"\n[AI 智能体] 正在基于您的兴趣 {state['interests']} 深度编排 {state['city']} 的行程...")

    # 格式化提示词并调用结构化大模型
    formatted_prompt = itinerary_prompt.format_messages(
        city=state['city'],
        interests=", ".join(state['interests'])
    )

    response: FullTravelPlan = structured_llm.invoke(formatted_prompt)

    # 仅增量返回大模型生成的结构化对象，不带任何黄线
    return {
        "itinerary_structured": response
    }