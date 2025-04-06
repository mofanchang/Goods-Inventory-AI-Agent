# Agent
你說得沒錯，這個專案確實更偏向於一個 AI Agent 的應用，而不僅僅是單純的庫存管理系統。它結合了自然語言處理、向量檢索和規則推理，讓使用者能以對話方式與系統互動，具有 AI 代理的特性。以下是根據這個觀點調整後的更簡潔 README：

---

## 飲料進銷存 AI Agent

一個基於 Python 的 AI 代理，專為飲料進銷存管理設計，支援自然語言查詢與智能建議。

### 功能
- **數據管理**：輸入飲料進銷存資料，儲存至 Supabase。
- **智能對話**：回答如「可樂需要進貨嗎？」的問題，根據庫存規則提供建議。

### AI 特性
- **語言模型**：TinyLLaMA-1.1B 生成回應。
- **向量檢索**：MiniLM-L6-v2 嵌入 + Chroma 資料庫。
- **流程**：LangGraph 串聯檢索與分析。

### 使用
1. 安裝：`pip install -r requirements.txt`。
2. 配置 Supabase URL 與 Key。
3. 啟動 Gradio 介面，輸入資料或提問。

### 範例
- 輸入：可樂，進貨 100，銷貨 60，過期 2025-06-12。
- 問：「可樂需要進貨嗎？」  
  答：「庫存 40 瓶，低於 50，建議進貨。」

### 依賴
- pandas, gradio, langchain-community, transformers, torch, requests, chromadb

