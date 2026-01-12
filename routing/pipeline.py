from .intent_rules import IntentRule
from rag_module.prompts import ROUTE_CHAPTER_NUMBER_and_SPLIT_QUES_PROMPT
from .parser_res_json import parse_intent_response, parse_route_and_split

def route_and_split(question: str, chapter_titles: list[str], llm):
    chapters_text = "\n".join(f"{i+1}. {title}" for i, title in enumerate(chapter_titles))
    prompt = ROUTE_CHAPTER_NUMBER_and_SPLIT_QUES_PROMPT.replace(
        "chapters", chapters_text).replace("{question}", question)
    response = llm.generate(prompt)
    chapter_number, questions = parse_route_and_split(response)
    print(f"{'-'*100}\n"
          f"[DEBUG] Routed chapter: {chapter_number}\n"
          f"[DEBUG] Sub-questions: {len(questions)}\n"
          f"{'-'*100}")
    for i, sq in enumerate(questions, start=1):
        print(f"  [{i}] {sq}")
    print("-"*100)
    return chapter_number, questions
def intent_route(q: str, llm):
    rule = IntentRule()
    rule_need_more = rule.need_more_info_cheap
    out = rule.step0_intent(q)
    # handled=True
    if out['handled']: 
        # Rule from class IntentRule
        if out['intent'] in ('chitchat',):
            return {
                "handled": True,
                "intent": out["intent"], 
                "answer": llm.generate(q)
            }
        if out["intent"] in ("study", "summary",) and rule_need_more(q):
            # need_more_info -> False -> handle = False
            return {
                'ask': f"{q}",
                'handled': False,
                'intent': out['intent'],
                'need_more_information': True,
                "message": "Vui lòng cung cấp thêm thông tin liên quan đến câu hỏi!",
            }
        if out["intent"] in ("study", "summary") and not rule_need_more(q):
            return {
                "handled": True,
                "intent": out["intent"],
                "need_more_information": False,
            }
        return out
    # handled=False: gọi LLM intent prompt để ra intent chuẩn
    print(out, " -> Gọi LLM Xử Lý")
    raw = llm.ask_clarify(question=q) # sử dụng intentprompt nếu chitchat general question -> return answer luôn
    (user_input, intent, need_more_information, 
    needs_normalization, normalized_query, sub_questions, answer) = parse_intent_response(raw)
    if intent in ('chitchat', 'general_qa'):
        return {
            "handled": True,
            "intent": intent,
            "answer": answer,
        }
    if need_more_information:
        return {
            'ask': user_input,
            'handled': False, # set tay
            'intent': intent,
            'need_more_information': need_more_information,
            "message": "Vui lòng cung cấp thêm thông tin liên quan đến câu hỏi!",
        }
    return {
        "ask": user_input,
        "handled": True,
        "intent": intent,
        "need_more_information": False,
        "needs_normalization": needs_normalization,
        "normalized_query": normalized_query,
        "sub_questions": sub_questions,
    }


        
