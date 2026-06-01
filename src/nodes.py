#存放负责处理人类交互、外接系统输入或确定性逻辑的边缘节点（人类协同节点）。

from langchain_core.messages import HumanMessage
from src.schemas import PlannerState


def input_city_node(state: PlannerState) -> dict:
    """交互节点：收集用户想去的城市"""
    print("\n🌍 [系统提示] 开启您的自适应多智能体路线编排之旅...")
    user_input = input("👉 请问您近期计划去哪座城市进行一日/多日游？\n您的输入: ").strip()

    # 返回增量字典，触发 LangGraph 全局自动合并
    return {
        "city": user_input,
        "messages": [HumanMessage(content=f"计划目的地：{user_input}")]
    }


def input_interests_node(state: PlannerState) -> dict:
    """交互节点：收集用户的个性化兴趣标签"""
    print(f"\n📌 [系统提示] 当前目的地已锁定：【{state['city']}】")
    user_input = input(
        "👉 请问您的出游偏好是什么？（例如: 历史古迹, 本地地道美食, 拍照打卡, 亲子避娃。多个请用逗号隔开）\n您的输入: ").strip()

    interests_list = [item.strip() for item in user_input.split(",") if item.strip()]

    return {
        "interests": interests_list,
        "messages": [HumanMessage(content=f"个性化偏好标签：{user_input}")]
    }