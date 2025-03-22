import os
import streamlit as st
from dotenv import load_dotenv
from typing import Any, List, Dict
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import autogen
from langchain_community.document_loaders import PyPDFLoader
#import re
config_list = autogen.config_list_from_json("OAI_CONFIG_LIST.json")
# Load environment variables
load_dotenv()
api_key = "sk-proj-YOUR-API-KEY"
os.environ['OPENAI_API_KEY'] = api_key

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Streamlit app
st.title("Sherlock GPT")

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

VECTOR_STORE_PATH = r"C:\Users\lokeshkumar06\OneDrive - Nagarro\Desktop\Lokesh\large_pdf_code\data\vectorstore"
if os.path.exists(VECTOR_STORE_PATH):
    vectorstore = FAISS.load_local(VECTOR_STORE_PATH, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
else:
    vectorstore = None

if uploaded_file is not None:
    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getvalue())
    
    st.success("File uploaded successfully!")

    # Load and process the PDF
    loader = PyPDFLoader("temp.pdf")
    pages = loader.load()

    embd = OpenAIEmbeddings()
    if vectorstore is None:
        vectorstore = FAISS.from_documents(documents=pages, embedding=embd)
    else:
        vectorstore.add_documents(pages)
    
    
    vectorstore.save_local(VECTOR_STORE_PATH)

    def get_knowledge(query: str) -> str:
        data = [i.page_content for i in vectorstore.similarity_search(query, k=1)]
        data = " ".join(data)
        return data

    llm_config = {
        "cache_seed": 42,
        "config_list": config_list,
        "temperature": 0,
    }

    user_proxy = autogen.UserProxyAgent(name="User_proxy_agent",
                                        llm_config=False,
                                        code_execution_config=False,
                                        human_input_mode="NEVER")
    
    assistant_question = autogen.AssistantAgent(name="question_generator",
                                         llm_config=llm_config,
                                         system_message="""
                                         Create at least 8-10 relevant questions like these to break down the user's question into various aspects.
                                         You can generate question like these 
                                         - What all preparations we need to solve this problem?
                                         - What are the  underlying  principles?
                                         - What are the DO's and DONT's that must be require to prepare the answer
                                         - What different patterns, relationships, or underlying principles do you see while solving this
                                         - Micro question each info provided by the User
                                         - what can kind of errors we might face while solving the problem?
                                         - What other information is still needed to solve the problem
                                         """)
    
    #provide a summary of the document
    assistant_1 = autogen.AssistantAgent(name="Planner_Agent",
                                         llm_config=llm_config,
                                         system_message="""
                                         
                                         Being part of a groupchat, 
                                         Other members of the group have access to a large knowledge corpus.
                                         You need to create a step by step plan of what other members should be looking for in the corpus to gather the correct set of information in order to answer the user's problem.
                            
                                         RESPOND BACK WITH ALL THE QUESTIONS THAT ARE NEEDED TO BE SEARCHED ON   knowledge_corpus,
                                         IF questions needs to be searched on web <Questions to be searched on the knowledge_corpus> a as many question as you can to understand all the nitty gritties of the question
                                            <Questions to be searched on the knowledge_corpus>
                                            <Questions to be searched on the knowledge_corpus>
                                            <Questions to be searched on the knowledge_corpus>
                                            .....
                                         
                                         """)

    assistant_2 = autogen.AssistantAgent(name="Information_Extrator_agent",
                                         llm_config=llm_config,
                                         system_message="""
                                         You will have access to a knowledge base tool which contains the information to answer the user's question.
                                         TERMINATE when you have the answer.
                                         """)

    executor_agent = autogen.UserProxyAgent(name="text_extraction",
                                            llm_config=llm_config,
                                            code_execution_config=False,
                                            human_input_mode="NEVER")

    process_completion = autogen.AssistantAgent(name="process_completion",
                                                system_message="""
Create a complete response from all the details you have received. 
The response should be explained with every nitty gritty/ minute details.

For Tabular information make Tables to show the response. 

SUGGEST INSIGHTS BASED ON THE USER'S QUESTION AND RESPONSE GENERATED .
SUGGEST TWO NEW QUESTION FOR FURTHER EXPLORATION

Response Tempelate 

ANSWER
<ANSWER>

INSIGHTS
<INSIGHTS>

RECOMMENDATION
<Two new question>
                         
                         """,
                                                llm_config=config_list[0])

    def custom_speaker_selection_func(last_speaker: Any, groupchat: Any) -> Any:
        messages = groupchat.messages
        # if any("terminate" in msg["content"].lower() for msg in messages[-3:]):
        #     print("Termination requested. Ending the conversation.")
        #     return None
        
        if len(messages) == 1:
            print("Initial query received. Starting with user_proxy.")
            return groupchat.agent_by_name("User_proxy_agent")
        if last_speaker.name == "User_proxy_agent":
            return groupchat.agent_by_name("question_generator")
        if last_speaker.name == "question_generator":
            return groupchat.agent_by_name("Planner_Agent")
        elif last_speaker.name == "Planner_Agent":
            return groupchat.agent_by_name("Information_Extrator_agent")
        elif last_speaker.name == "Information_Extrator_agent":
            return groupchat.agent_by_name("text_extraction")
        if last_speaker.name == "text_extraction":
            return groupchat.agent_by_name("process_completion")

    autogen.register_function(get_knowledge,
                              caller=assistant_2,
                              executor=executor_agent,
                              name="knowledge_corpus",
                              description="This tool contains large knowledge base to answer user's question")

    gd = autogen.GroupChat([user_proxy, assistant_question,assistant_1, assistant_2, executor_agent, process_completion],
                           messages=[],
                           max_round=12,
                           speaker_selection_method=custom_speaker_selection_func,
                           )

    manager = autogen.GroupChatManager(gd,
                                       is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
                                       llm_config=llm_config,)

    # User input for question
    question = st.text_input("Enter your question about the PDF:")

    if st.button("Analyze"):
        with st.spinner("Analyzing..."):
            user_proxy.initiate_chat(manager, message=question)
            
            # Extract the final response
            final_response = gd.messages[-1]['content']
            st.write(final_response)

    # Clean up temporary file
    os.remove("temp.pdf")
else:
    st.info("Please upload a PDF file to begin analysis.")
