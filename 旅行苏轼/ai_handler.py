import requests
import config

def select_best_corpus(player_input, corpus_dict, limit=2):
    """
    权重抓取引擎：根据关键词匹配度选择最相关的语料
    """
    scored_fragments = []
    
    # 遍历 JSON 中定义的分类（如 policy, landscape）
    for category, fragments in corpus_dict.items():
        for item in fragments:
            score = 0
            # 匹配关键词并累加权重
            for kw in item.get("keywords", []):
                if kw in player_input:
                    score += item.get("weight", 5) 
            
            if score > 0:
                scored_fragments.append((score, item["content"]))
    
    # 按得分从高到低排序
    scored_fragments.sort(key=lambda x: x[0], reverse=True)
    
    # 返回得分最高的前 limit 条内容
    return [f[1] for f in scored_fragments[:limit]]

def ask_ai(persona_data, messages_history, poetry_mode = False):
    """
    persona_data: 传入从 JSON 加载的字典 (包含 system_prompt 和 corpus)
    messages_history: 传入聊天记录列表
    """
    # 1. 安全获取最后一条玩家输入
    player_input = messages_history[-1]["content"] if messages_history else ""
    
    # 2. 运行抓取引擎（只抓取最相关的语料，节省 Token 并精准定位）
    dynamic_corpus = select_best_corpus(player_input, persona_data.get("corpus", {}))
    
    # 3. 动态构建完整的 System Prompt
    corpus_text = ""
    if dynamic_corpus:
        corpus_text = "\n【你脑海中浮现的相关旧作片段，请不要超出该时段的记忆库内容，请在回复时参考其文采或逻辑】：\n" + "\n".join(dynamic_corpus)
    
    # 注意：这里要把基础设定和动态抓取的语料拼起来
    full_system_prompt = persona_data.get("system_prompt", "") + corpus_text
    #3.1和诗模式
    if poetry_mode:
        full_system_prompt += "玩家现在给你寄来了一首格律正确的诗，请你依据意境、构思和用典进行评价，视情况再回赠一句你自己的诗词。"
    
    # 4. 构建请求数据包
    headers = {
        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    # 构造发给 API 的消息列表
    # 第一条永远是刚生成的“灵魂设定 + 动态语料”
    api_messages = [{"role": "system", "content": full_system_prompt}]
    # 接着拼接之前的聊天记录
    api_messages.extend(messages_history)

    payload = {
        "model": "deepseek-chat",
        "messages": api_messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(config.API_URL, json=payload, headers=headers, timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result.get("choices")[0].get("message").get("content")
        else:
            # 增加更详细的错误排查
            error_msg = response.text
            return f"(梦境不稳，神识中断: {response.status_code} - {error_msg})"
    except Exception as e:
        return f"(天地间一阵混沌，似乎无法感应星空: {str(e)})"
    