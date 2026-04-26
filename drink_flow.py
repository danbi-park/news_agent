from crewai.flow.flow import Flow, listen, start, router, and_, or_
from pydantic import BaseModel


class DrinkState(BaseModel):
    user_input: str = ""
    intent: str = ""
    result: str = ""


class DrinkFlow(Flow):
    state: DrinkState = DrinkState()

    @start()
    def receive(self):
        pass

    @listen(receive)
    def classify(self):
        text = self.state.user_input

        if "물" in text:
            self.state.intent = "water"
        elif "추천" in text:
            self.state.intent = "recommend"
        else:
            self.state.intent = "unknown"

    @router(classify)
    def route(self):
        return self.state.intent

    @listen("water")
    def give_water(self):
        return "물 드릴게용"

    @listen("recommend")
    def recommend(self):
        return "AI 가 추천하는 음료는 콜라 입니다!"

    @listen("unknown")
    def unknown(self):
        return "잘 모르겠어요"


if __name__ == "__main__":
    flow = DrinkFlow()
    flow.state.user_input = "과자 주세용"

    result = flow.kickoff()
    print(result)
