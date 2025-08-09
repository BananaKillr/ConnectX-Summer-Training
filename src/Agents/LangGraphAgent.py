from langgraph.graph import START, StateGraph,END
from typing_extensions import List, TypedDict
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict,Annotated
from langchain_core.messages import AIMessage,HumanMessage
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
# from Config.config import get_settings
# 
    

class State(TypedDict):
    user_id: int
    messages : Annotated[list, add_messages]
    count: int = 0


class LangGraphAgent:
    def __init__(self):
        print("hello")
        # self.settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(google_api_key="AIzaSyCfdpg3fCA1zfIgC-YeXijDhq3H7xsPfyo",
                                          model="gemini-2.0-flash")  


        graph_builder = StateGraph(State)
        graph_builder.add_node("call_llm",self.call_llm)
        graph_builder.add_node("check_counter",self.check_counter_node)
        graph_builder.add_node("end_conversation",self.end_conversation)

        graph_builder.add_conditional_edges("check_counter", self.check_counter_condition, 
                                            { True: "call_llm", 
                                             False: "end_conversation"} )
        
        graph_builder.add_edge("end_conversation",END)

        graph_builder.add_edge("call_llm", "check_counter")
        graph_builder.set_entry_point("check_counter")

        self.graph = graph_builder.compile(interrupt_after=['call_llm'])
         
        image_data = self.graph.get_graph(xray=0).draw_mermaid_png()
        print('xxx')
        with open("langgraph.png", "wb") as f:
                 f.write(image_data)
    
    def call_llm(self,state:State,config):
        messages = [
                (
                    "system",
                    "You are a helpful personal assistant that answers all user questions.",
                ),
                ("human", f"{state['messages'][-1].content}"),
            ]
        llm_response = self.llm.invoke(messages)
        print(llm_response)
        count = state['count'] + 1
        print(count)
        return {'messages': llm_response,
                "count": count}
        
    def check_counter_node(self, state: State, config):
        print(f"Checking counter: {state['count']}")
        return state

    def check_counter_condition(self, state: State):
        return state["count"] < 3

    
    def end_conversation(self,state:State,config):
         return {"messages":AIMessage(content="You passed your conversation limit, Please retry after 6 hours!")}
    


if __name__ == "__main__":
    agent = LangGraphAgent()
    config = {"configurable": {"thread_id": "abc123"}}
    initial_state = {
            "user_id": 1,
            "messages": [HumanMessage(content="Hello, what is the capital of France?")],
            "count": 0
        }
    result = agent.graph.invoke(initial_state, config)
    print("Final result:", result['messages'][-1].content)


   