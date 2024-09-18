import os

txt_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data/kt_data/txt_data/KakaoTalkChats.txt")
with open(txt_path, mode='r', encoding='utf-8') as f:
    context = f.readlines()

branched_data = {}
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

# user = '조한결'
# me = '문도'

# # ':' 전 '조한결' or '문도' 판단
# for key in branched_data.keys:
#     chat = branched_data[key]
    

# print(branched_data)