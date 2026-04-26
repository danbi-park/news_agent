from crewai.flow.flow import Flow, listen, start, router, and_, or_

# 데이터 관리 라이브러리 (주로 데이터 검증을 쉽게 도와주는 라이브러리)
from pydantic import BaseModel


class MyFirstFlowState(BaseModel):
    hello: str = ""


class MyFirstFlow(Flow[MyFirstFlowState]):
    # state: MyFirstFlowState = MyFirstFlowState()

    @start()
    def start_flow(self):
        self.state.hello = "hello"
        print("hello start flow")
        # return 123

    @listen(start_flow)
    def first_step(self):
        # def first_step(self, num):
        # print(num) 123 이 출력됨
        self.state.hello = "word"
        print("hello first step")

    @listen(first_step)
    def second_step(self):
        print(f"hello step {self.state.hello}")

    @listen(
        and_(first_step, second_step)
    )  # first Step 이란 secondStep이 실행됐을때 실행되는 함수!!
    def and_dummy_func(self):
        print("and dummy func")

    @listen(
        or_(first_step, second_step)
    )  # 두번 실행됨!! fisrt_step, second_step 둘 다 있어서
    def or_dummy_func(self):
        print("or dummy func")

    # 라우터는 의사결정 단계, 조건식 분기같은 로직을 사용할 때 많이 쓰임
    @router(second_step)
    def router_to_end(self):
        print("router to end")
        check = True

        if check:
            return "check is True"  # 문자열을 리턴했는데 @listen("check is True")에서 감지할 수 있음
        else:
            return "check is False"

    @listen("check is True")
    def end_flow(self):
        print("end flow")


flow = MyFirstFlow()
flow.kickoff()
