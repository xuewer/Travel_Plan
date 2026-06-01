#系统的总控制室。利用 LangGraph 构建有向无环图，完成状态机的拓扑组装，并提供最终的本地运行演示。

from langgraph.graph import StateGraph, START, END
from src.schemas import PlannerState
from src.nodes import input_city_node, input_interests_node
from src.agents import create_itinerary_agent


def build_workflow() -> StateGraph:
    """组装拓扑状态图"""
    # 1. 传入全局状态模型初始化图
    workflow = StateGraph(PlannerState)

    # 2. 注册所有节点（包括交互节点与大模型 Agent 节点）
    workflow.add_node("input_city", input_city_node)
    workflow.add_node("input_interests", input_interests_node)
    workflow.add_node("create_itinerary", create_itinerary_agent)

    # 3. 构建确定性的状态流转边界（顺序流转）
    workflow.add_edge(START, "input_city")
    workflow.add_edge("input_city", "input_interests")
    workflow.add_edge("input_interests", "create_itinerary")
    workflow.add_edge("create_itinerary", END)

    return workflow


if __name__ == "__main__":
    # 编译图，生成可执行的智能体系统
    app = build_workflow().compile()

    # 初始化空的全局状态启动
    initial_state = {
        "messages": [],
        "city": "",
        "interests": [],
        "itinerary_structured": None
    }

    # 触发运行状态机
    final_output = app.invoke(initial_state)

    # --- 验收成果 ---
    plan = final_output.get("itinerary_structured")
    if plan:
        print("\n" + "=" * 50)
        print(f"🎉 您的专属定制【{plan.destination}】{plan.total_days}日游精细化方案已生成！")
        print("=" * 50)

        for day in plan.daily_plans:
            print(f"\n📅 【第 {day.day_number} 天行程单】")
            print("-" * 30)
            for idx, spot in enumerate(day.spots, 1):
                print(f" 📍 景点{idx}: {spot.name}")
                print(f"    ⏳ 建议时段: {spot.time_slot} | 建议停留: {spot.duration_hours}")
                print(f"    💰 预计花费: 人均 {spot.cost_per_person} 元")
                print(f"    💡 避坑指南: {spot.notes}\n")

        print("=" * 50)
        print(f"💡 【大出行综合贴士】\n{plan.summary_tips}")
        print("=" * 50)
    else:
        print("❌ 行程编排失败，请检查您的 API Key 与网络连接。")