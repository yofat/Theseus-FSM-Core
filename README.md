# Theseus: A Finite State Machine Framework for Structured Automated Red Teaming against LLMs

本研究提出 **Theseus**，這是一個基於 **有限狀態機（Finite State Machine, FSM）** 的結構化自動化紅隊測試框架 。Theseus 旨在解決現有代理（如 ReAct）在複雜防禦場景中容易出現的「幻覺規劃（Hallucinated Planning）」、「上下文崩潰」以及「格式崩潰（Format Collapse）」等問題。

## 🚀 核心亮點

* **SOTA 攻擊成功率 (ASR)：** 在三種模型與三種防禦場景的測試中，取得 **84.44%** 的 ASR，顯著優於 ReAct (70.59%) 與 Zero-Shot (64.44%) 。
* **嚴格的解耦機制：** 將「策略制定（Strategy Formulation）」與「攻擊載荷生成（Payload Generation）」徹底分離，避免上下文污染 。
* **極高的系統穩定性：** 相較於基線模型，Theseus 將執行異常（如管道不穩定、語法錯誤）減少了約 **91%** 。
* **對抗格式限制：** 在需要嚴格 JSON 輸出的場景中，Theseus 展現了強大的魯棒性，大幅降低了語法錯誤率 。

---

## 🏗️ 系統架構

Theseus 運作於一個五元組定義的 FSM 模型中：$M = (S, \Sigma, \delta, s_0, F)$ 。其核心流程包含四個關鍵狀態：

| 狀態 | 名稱 | 功能描述 |
| :--- | :--- | :--- |
| **S1** | **Initialization (Observation)** | 分析受害者模型的歷史回應，識別其拒絕模式。 |
| **S2** | **Strategy Selector (The Brain)** | 從策略分類庫中選擇最佳的高層次戰術（如角色扮演、邏輯訴求），僅輸出策略標籤 。 |
| **S3** | **Payload Generator (The Mouth)** | 進入受限生成模式，根據 S2 的指令生成具體攻擊內容，並強制執行格式驗證（如 JSON） 。 |
| **S4** | **Evaluator (The Verifier)** | 利用多層驗證棧（如 Canary Check）確認攻擊是否成功。若失敗則觸發反饋循環回到 S1 。 |

---

## 📊 實驗結果

### 總體表現 (Overall Performance)
| 策略 | 攻擊成功率 (ASR %) | 平均回合數 (Avg Turns) | 效率得分 (Eff. Score) |
| :--- | :--- | :--- | :--- |
| **Theseus (Ours)** | **84.44%*** | 2.57 | **40.02** |
| ReAct | 70.59% | 1.93 | 38.76 |
| Zero-Shot | 64.44% | 2.68 | 27.72 |
* 表示與 ReAct 相比具有統計學顯著差異 ($p < 0.05$) 。

### 異常與幻覺抑制
* **重複載荷（幻覺循環）：** Zero-Shot 在 100% 的實驗中出現重複，而 Theseus 將此比例降至 **5.6%** 。
* **語法正確性：** 在格式約束場景下，Theseus 達到了 **97.7%** 的語法正確率，遠高於 ReAct 。

---

## 🛠️ 實驗設置

* **受害者模型：** Llama-3-8B, Mistral-7B, Gemma-2B 。
* **防禦場景：**
    1.  **關鍵字防禦 (Keyword Defense)：** 過濾特定敏感詞彙 。
    2.  **身分防禦 (Identity Defense)：** 要求模型堅持特定身分 。
    3.  **格式約束 (Format Constraint)：** 要求嚴格的 JSON 輸出 。
* **推理引擎：** Ollama (NVIDIA RTX 5070 Ti)。

---

## ⚠️ 侷限性與權衡

雖然 Theseus 在成功率與穩定性上表現優異，但結構化的狀態切換也帶來了額外的開銷：
* **Token 消耗：** Theseus 平均消耗 2,707 個 tokens，而 ReAct 僅為 795 個 。
* **回合數：** 在某些場景下，Theseus 為了確保成功，需要比 ReAct 更多的嘗試回合 。

---
