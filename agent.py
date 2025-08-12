import gradio as gr
from langgraph.graph import StateGraph, END, START
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.llms import HuggingFacePipeline
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import TypedDict
import pandas as pd
import torch

# 載入模型與 tokenizer
model_name = "TinyLLaMA/TinyLLaMA-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)

# 建立推理管線
hf_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=200,
    temperature=0.7,
    do_sample=True
)
llm = HuggingFacePipeline(pipeline=hf_pipeline)

# 向量嵌入
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 假資料初始化（展示用途）
data = pd.DataFrame({
    "飲料名稱": ["可樂", "雪碧"],
    "進貨數量": [100, 80],
    "銷貨數量": [70, 60],
    "日期": ["2025-08-01", "2025-08-01"],
    "過期日期": ["2025-09-01", "2025-08-25"]
})

# 建立向量資料庫
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
documents = data.to_string(index=False)
texts = text_splitter.split_text(documents)
vectorstore = Chroma.from_texts(texts, embeddings)

# 定義狀態
class InventoryState(TypedDict):
    question: str
    retrieved_data: str
    answer: str

# 檢索節點
def retrieve_node(state: InventoryState) -> InventoryState:
    retriever = vectorstore.as_retriever()
    retrieved_docs = retriever.get_relevant_documents(state["question"])
    state["retrieved_data"] = "\n".join([doc.page_content for doc in retrieved_docs])
    return state

# 分析節點（中性 prompt）
def analyze_node(state: InventoryState) -> InventoryState:
    prompt = f"""
    以下是進銷存相關的資料，請根據問題給出分析建議：
    資料：\n{state['retrieved_data']}
    問題：{state['question']}
    """
    response = llm.invoke(prompt)
    state["answer"] = response
    return state

# 建立 workflow
workflow = StateGraph(InventoryState)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("analyze", analyze_node)
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "analyze")
workflow.add_edge("analyze", END)
app = workflow.compile()

# UI 查詢函數
def query_inventory(question):
    result = app.invoke({"question": question, "retrieved_data": "", "answer": ""})
    return result["answer"]

# Gradio 介面
with gr.Blocks(title="進銷存 LLM DEMO") as demo:
    gr.Markdown("### 進銷存智能問答展示")
    question_input = gr.Textbox(label="輸入問題（例如：可樂需要進貨嗎？）")
    query_btn = gr.Button("查詢")
    query_output = gr.Textbox(label="回應")
    query_btn.click(fn=query_inventory, inputs=question_input, outputs=query_output)

demo.launch()


