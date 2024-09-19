import json
import os

root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
with open(os.path.join(root_dir, "data/kt_data/json_data/Chatting.json"), mode='r', encoding='utf-8') as f:
    data = json.load(f)

user = "조한결"
me = "문도"

# 결과를 저장할 리스트
corpus_pairs = []

# 데이터 전처리 함수
def process_chats(chat_dict):
    query = ""
    response = ""
    
    for chatting in chat_dict.values():
        for conversation in chatting:
            speaker, message = conversation.split(" : ", 1)
            
            if message in ['사진', '동영상', '이모티콘']:
                continue
            # "문도"의 발화는 query로 설정
            if speaker == me:
                if query and response:  # 기존 쌍이 있으면 저장
                    corpus_pairs.append((query.strip(), response.strip("<SEP>")))
                    response = ""  # response 초기화
                query = message  # 새 query 설정
            
            # "조한결"의 발화는 response로 설정
            elif speaker == user:
                if query:  # query가 있을 때만 response를 생성
                    if response:
                        response += f" <SEP> {message}"
                    else:
                        response = message
    
    # 마지막으로 쌓인 쌍 저장
    if query and response:
        corpus_pairs.append((query.strip(), response.strip("<SEP>")))

# 날짜별로 대화 처리
for date, chat_dict in data.items():
    process_chats(chat_dict)

data = dict()
for i, pair in enumerate(corpus_pairs):
    data[i] = {'query': pair[0], 'response': pair[1]}
    
with open(os.path.join(root_dir, 'data/kt_data/json_data/corpus_pair.json'), 'w', encoding='utf-8') as new_file:
    json.dump(data, new_file, ensure_ascii=False, indent="\t")