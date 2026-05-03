from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel
from crewai import CrewOutput
from typing import Optional


class FundManagerState(BaseModel):

    # 사용자 inputs
    investment_goal: str = ""  # 사용자의 투자 목표
    risk_preference: str = ""  # 사용자의 투가 성향(보수, 공격)
    budget: float = 0.0  # 사용자의 예산

    # 라우터의 의사 결정
    strategy_type: str = ""

    # 분석 결과들
    tech_trends: Optional[CrewOutput] = None
    growth_scores: Optional[CrewOutput] = None
    stability_scores: Optional[CrewOutput] = None
    divide_scores: Optional[CrewOutput] = None

    portfolio: Optional[CrewOutput] = None  # 최종


class FundManagerFlow(Flow[FundManagerState]):

    # start에서는 state에 대한 조건, 검증을 먼저 한다.
    @start()
    def init_fund_analysis(self):
        # 유효성 검사
        if not self.state.investment_goal:
            raise ValueError("투자 목표를 입력해주세요")
        if not self.state.risk_preference:
            raise ValueError("투자 성향을 입력해주세요")
        if not self.state.budget:
            raise ValueError("예산을 입력해주세요")

    # 투자 성향을 분기
    @listen(init_fund_analysis)
    def analyze_investment_strategy(self):
        pass
        # self.state.strategy_type = ""

    @router(analyze_investment_strategy)
    def strategy_router(self):
        if self.state.strategy_type == "growth":
            return "growth_analysis"  # 성장주, 기술주
        elif self.state.strategy_type == "value":
            return "value_analysis"  # 안정주

    @listen("growth_analysis")
    def analyze_tech_trends(self):
        pass

    @listen(analyze_tech_trends)
    def evaluate_growth_potential(self):
        # self.state.
        pass

    @listen("value_analysis")
    def screen_stable_companies(self):
        pass

    @listen(screen_stable_companies)
    def evaluate_value_potential(self):
        pass

    @listen(or_(evaluate_growth_potential, evaluate_value_potential))
    def synthesize_portfolio(self):
        pass

    @listen(synthesize_portfolio)
    def finalize_investment_recommendation(self):
        pass
        return self.state.portfolio


flow = FundManagerFlow()
# flow 를 시각적으로 보여줌, html 파일이 생김!!! crewai_flow.html
flow.plot()


flow.kickoff(
    inputs={
        "investment_goal": "AI 같은 첨단 기술주에 투자하고 싶습니다",
        "risk_preference": "공격적",
        "budget": 20000.0,
    }
)

# flow.kickoff(
#     inputs={
#         "investment_goal": "은퇴 자금을 위해 안정적인 배당을 원합니다. ",
#         "risk_preference": "보수적",
#         "budget": 50000.0,
#     }
# )
