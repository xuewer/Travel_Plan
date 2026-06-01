#定义整个系统的状态机数据流（State）以及大模型的结构化输出（Pydantic)

from typing import List, Annotated
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages

class ScenicSpot(BaseModel):
    """单个景点、餐厅或体验的精细化编排"""
    name: str = Field(description="景点、餐厅或酒店的名称")
    duration_hours: str = Field(description="建议停留、游玩或就餐的时长，例如: 2.5小时")
    cost_per_person: int = Field(description="预计人均花费（元），纯数字")
    time_slot: str = Field(description="建议游玩时间段，例如: 上午、中午、下午、晚上")
    notes: str = Field(description="实时小提示，如交通方式、避坑指南、或特色菜推荐")

class DailyItinerary(BaseModel):
    """单日的行程路线"""
    day_number: int = Field(description="第几天，例如：1")
    spots: List[ScenicSpot] = Field(description="这一天按时间顺序排列的景点与活动列表")

class FullTravelPlan(BaseModel):
    """最终交付给用户的完整多天自适应路线方案"""
    total_days: int = Field(description="总天数")
    destination: str = Field(description="目的地城市")
    daily_plans: List[DailyItinerary] = Field(description="每日精细化行程单列表")
    summary_tips: str = Field(description="通行的整体建议，如穿衣、天气、大交通提醒")

class PlannerState(TypedDict):
    """LangGraph 全局状态机模型，负责在节点间流转和合并数据"""
    messages: Annotated[List[AnyMessage], add_messages]
    city: str
    interests: List[str]
    itinerary_structured: FullTravelPlan