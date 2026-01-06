from .intent_rules import IntentRule
from rag_module.generation import get_generation_service
from rag_module.prompts import INTENT_PROMPT, ROUTER_AND_SPLIT_PROMPT
from .parser_res_json import parse_intent_response, parse_route_and_split
from rag_module.llm import GeminiLLM

chapter_titles = [
'CHƯƠNG 1: ĐẢNG CỘNG SẢN VIỆT NAM RA ĐỜI VÀ LÃNH ĐẠO ĐẤU TRANH GIÀNH CHÍNH QUYỀN (1930-1945)',
'CHƯƠNG 2: ĐẢNG LÃNH ĐẠO HAI CUỘC KHÁNG CHIẾN CHỐNG NGOẠI XÂM, HOÀN THÀNH GIẢI PHÓNG DÂN TỘC, THỐNG NHẤT ĐẤT NƯỚC (1945 - 1975)',
'CHƯƠNG 3: ĐẢNG LÃNH ĐẠO CẢ NƯỚC QUÁ ĐỘ LÊN CHỦ NGHĨA XÃ HỘI VÀ TIẾN HÀNH CÔNG CUỘC ĐỔI MỚI (TỪ NĂM 1975 ĐẾN NAY)',
]
def route_and_split(question: str, chapter_titles: list[str]):
    llm = GeminiLLM()
    chapters_text = "\n".join(f"{i+1}. {title}" for i, title in enumerate(chapter_titles))
    prompt = ROUTER_AND_SPLIT_PROMPT.format(
        chapters = chapters_text,
        question=question
    )
    response = llm.generate(prompt)
    chapter_number, sub_questions = parse_route_and_split(response)
    return chapter_number, sub_questions
def intent_route(q: str):
    rule = IntentRule()
    rule_need_more = rule.need_more_info_cheap
    llm = get_generation_service()
    out = rule.step0_intent(q)
    # handle=True
    if out['handled']: 
        # Rule from class IntentRule
        if out['intent'] in ('chitchat',):
            return {
                "handled": True,
                "intent": out["intent"], 
                "answer": llm.answer(q)
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
            chapter_number, sub_questions = route_and_split(q, chapter_titles)
            # In Debug 
            print(f"{'-'*100}\n"
                f"[DEBUG] Routed chapter: {chapter_number}\n"
                f"[DEBUG] Sub-questions: {len(sub_questions)}\n"
                f"{'-'*100}")
            for i, sq in enumerate(sub_questions, start=1):
                print(f"  [{i}] {sq}")
            print("-"*100)
            return {
                **out, 
                "chapter_number": chapter_number, 
                "sub_questions": sub_questions
            }
        return out
    
    # handled=False: gọi LLM intent prompt để ra intent chuẩn
    print(out, " -> Gọi LLM Xử Lý")
    raw = llm.ask_clarify(question=q, prompt_template=INTENT_PROMPT)
    (user_input, intent, need_more_information, 
    needs_normalization, normalized_query, sub_questions) = parse_intent_response(raw)
    if intent in ('chitchat', 'general_qa'):
        return {
            "handled": True,
            "intent": intent,
            "answer": llm.answer(user_input)
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

q = 'Nguyễn Ái Quốc đã chuẩn bị các điều kiện thành lập Đảng như thế nào trong những năm 1911-1930?'
test = intent_route(q)
print(test)
        
