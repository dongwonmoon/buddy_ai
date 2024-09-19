import os
import re
import json
from collections import OrderedDict

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
with open(os.path.join(root_dir, "data/kt_data/txt_data/KakaoTalkChats.txt"), mode='r', encoding='utf-8') as f:
    context = f.readlines()

branched_data = OrderedDict()
current_key = ""
current_value = []
prev_key = ""

user = '조한결'
me = '문도'

for text in context[3:]:
    if ('년' in text and '월' in text and '일' in text) and (user not in text and me not in text):
        current_key = text
        current_value = []
    elif ('년' in text and '월' in text and '일' in text) and (user in text or me in text):
        current_value.append(text)
        
    if prev_key != current_key:
        branched_data[current_key] = current_value
        
    prev_key = current_key

# date: {chat1:, chat2:, ...}
sep_by_date = OrderedDict()
for date in branched_data.keys():
    chatting_chunk = OrderedDict()
    at_that_date_chatting = branched_data[date]

    current_user = ""
    prev_user = ""
    chatting = []
    n = 0

    for chat in at_that_date_chatting:
        colon_sliced_chat = chat[:chat.find(":", chat.find(":")+1)]  # 두 번째 ":" 까지 자름

        # 채팅한 사람 찾기
        whoes_chat = re.search(f"{user}|{me}", colon_sliced_chat)
        if whoes_chat:
            current_user = whoes_chat.group()

        chat = chat[chat.find(current_user):].rstrip("\n")
        # 발화자가 바뀌면 대화 덩어리 저장
        if current_user != prev_user:
            if chatting:  # 비어 있지 않은 경우만 저장
                n += 1
                chatting_chunk[f"chatting_{n}"] = chatting
            chatting = [chat]  # 새로운 대화 시작
        else:
            chatting.append(chat)  # 같은 사람이 연속으로 대화하면 추가

        prev_user = current_user

    # 마지막 대화 덩어리 저장
    if chatting:
        n += 1
        chatting_chunk[f"chatting_{n}"] = chatting
    sep_by_date[date.rstrip("\n")] = chatting_chunk
    
with open(os.path.join(root_dir, "data/kt_data/json_data/Chatting.json"), 'w', encoding='utf-8') as json_file:
    json.dump(sep_by_date, json_file, ensure_ascii=False, indent="\t")