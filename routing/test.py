from rag_module.prompts import ROUTE_INTENT_PROMPT
from rag_module.generation import get_generation_service
from intent_rules import IntentRule
if __name__ == "__main__":
    rule = IntentRule()
    llm = get_generation_service()
    q = "bắt đầu trả lời câu hỏi tôi cung cấp liên quan đến môn lịch sử đảng nhé"
    out = rule.step0_intent(q)
    if out['handled'] == False:
        res = (llm.ask_clarify(question=q, prompt_template=ROUTE_INTENT_PROMPT))
        if res['need_more_information'] == True:
            print('Ok. Bạn gửi câu hỏi về Lịch sử Đảng (nêu rõ giai đoạn/năm hoặc chương nếu có). Nếu câu hỏi dài nhiều ý, mình sẽ tách và trả lời từng ý.”')
