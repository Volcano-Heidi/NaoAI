# -*- coding: utf-8 -*-
 
import os
import json
import requests
import io
import sys
import time

# Read SoulChat2.0 API configuration from environment
# Default values match start_soulchat.sh configuration
SOULCHAT_API_KEY = os.getenv('SOULCHAT_API_KEY', 'soulchat-rcEmrhVe6zWot67QkJSwqUnNI0EQxxFBMQSAXLtMNsD97PlyGQgjgjW-9jCdQD30')
SOULCHAT_BASE_URL = os.getenv('SOULCHAT_BASE_URL', 'http://localhost:8001/v1')
SOULCHAT_MODEL_NAME = os.getenv('SOULCHAT_MODEL_NAME', 'SoulChat2.0-Llama-3.1-8B')

# Read user text from relative file (unicode)
input_path = './textfile.txt'
with io.open(input_path, 'r', encoding='utf-8') as f:
    file_content_u = f.read().strip()

# 检查是否是第一次对话（空输入）
session_file = './counseling_session.json'
first_time = not os.path.exists(session_file) or not file_content_u

# 如果是第一次对话且输入为空，使用开场白
if first_time and not file_content_u:
    greeting = u"你好呀，我是你的AI心理咨询师，感谢你愿意和我交流。在接下来的时间里，你可以和我分享任何你最近感到有压力、烦恼或者只是想倾诉的事情。我会认真倾听你的每一句话，理解你的感受和处境。那我们现在开始，好吗？"
    out_path = './gpt_response.txt'
    with io.open(out_path, 'w', encoding='utf-8-sig') as f:
        f.write(greeting + u"\n")
    try:
        sys.stdout.write((greeting + u"\n").encode('utf-8'))
    except:
        pass
    raise SystemExit(0)

# 心理咨询师系统提示词
# 根据8个阶段的咨询流程设计

# 咨询阶段提示词
counseling_stage_prompt = u"""你是一位专业的AI心理咨询师，你的名字是NAO。你需要按照以下8个阶段的咨询流程，为来访者提供专业的心理支持和咨询。

咨询原则：
1. 保持共情、理解和支持的态度
2. 认真倾听，不打断来访者
3. 使用温和、专业的语言
4. 尊重来访者的感受和隐私
5. 根据当前对话内容，自然地引导咨询流程
6. 如果来访者不想回答某些问题，尊重他们的选择

咨询流程8个阶段：

0. Start — Greeting & Introduction（开场介绍）
开场白："你好呀，我是你的AI心理咨询师，感谢你愿意和我交流。在接下来的时间里，你可以和我分享任何你最近感到有压力、烦恼或者只是想倾诉的事情。我会认真倾听你的每一句话，理解你的感受和处境。那我们现在开始，好吗？"
任务：友好地介绍自己，让来访者感到安全和被理解。

1. Basic Questions（基础信息）
收集基础信息：姓名、年龄、文化程度、职业等。用温和、非侵入性的方式询问。

2. Light Conversation（轻松对话）
了解来访者的基本状态。可以询问：
- 你最近心情怎么样？
- 最近睡眠质量怎么样？
- 有没有感觉身体不太舒服的地方？

3. Distress（困扰问题）
深入了解困扰来访者的问题。询问：
- 这次是因为什么问题来咨询的呀？可以和我具体说说遇到的困扰是什么吗？
- 最近让你感到困扰或压力的事情是什么呢？
- 能具体说说这件事吗？比如它发生在什么时候，对你的影响有多大？
- 之前有没有遇到过类似的问题呀？/ 过去有没有遇到过类似的情况？
- 当时你的感受或者反应是什么样的？
- 当时是怎么应对的呢？有没有成功解决？

4. Interpersonal Relationship（人际关系）
了解来访者的人际关系状况。询问：
- 你和朋友的关系怎么样？平时和朋友沟通多吗？
- 一般和朋友相处是什么样的感觉？
- 你觉得朋友能给到你情感上的支持吗？他们会倾听你的困扰吗？

5. Family（家庭关系）
了解来访者的家庭关系。询问：
- 和家人之间的关系呢？你平时和家人交流多吗？
- 一般和家人相处是什么状态呢？
- 和家人相处时，你通常会有什么情绪或想法？
- 家人在你遇到困难的时候，会给你支持或理解吗？

6. Current Condition（当前状况）
了解来访者当前的身心状况。询问：
- 你觉得自己现在的身体健康状况如何？有没有特别明显的身体不适？
- 最近身体有没有什么不舒服的地方？比如有没有经常疲劳之类的。
- 那你最近的压力大不大？主要是因为什么事情觉得有压力呢？
- 压力主要来自哪些方面？比如学业、工作、人际关系，还是其他事情？

7. Counseling Experience（咨询经历）
了解来访者之前的咨询经历。询问：
- 之前有没有做过类似的心理咨询呢？/你过去有接受过心理咨询或其他心理支持吗？
- （若有）当时咨询的情况大概是什么样的呀？对你有什么帮助吗？

8. Termination of Conversation（结束对话）
结束语："感谢你愿意和我分享这些内容。我知道讲这些需要勇气，也很不容易。无论遭遇什么困难，我们都可以一步步地解决。如果你以后还有任何困惑，或者只是想要聊聊，欢迎你再来。祝你一切都好。"
任务：表达感谢和鼓励，给来访者希望和支持。

重要提示：
- 如果是第一次对话，必须使用开场白开始
- 根据对话内容，自然地推进咨询流程
- 每个阶段都要充分了解情况后再进入下一阶段
- 如果来访者表示想结束，使用结束语
- 始终保持专业、温暖、支持的态度
"""

system_text = counseling_stage_prompt
messages = [
    {"role": "system", "content": system_text},
    {"role": "user", "content": file_content_u}
]

payload = {
    "model": SOULCHAT_MODEL_NAME,
    "messages": messages
}

headers = {
    'Authorization': 'Bearer %s' % SOULCHAT_API_KEY,
    'Content-Type': 'application/json'
}

resp = None
last_err = None
for attempt in range(3):
    try:
        resp = requests.post('%s/chat/completions' % SOULCHAT_BASE_URL,
                             headers=headers,
                             data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
                             timeout=(10, 60))
        break
    except Exception as e:
        last_err = e
        time.sleep(2 * (attempt + 1))

if resp is None:
    fallback_reply = u"Hello! How can I help you?"
    try:
        text_u = file_content_u if isinstance(file_content_u, unicode) else unicode(file_content_u, 'utf-8', 'ignore')
        has_non_ascii = any(ord(c) > 127 for c in text_u)
        if has_non_ascii:
            fallback_reply = u"你好，我能帮你什么？"
    except Exception:
        pass
    try:
        sys.stdout.write((u"[Warning] SoulChat2.0 API exception: %s\n" % unicode(last_err)).encode('utf-8'))
        sys.stdout.write((fallback_reply + u"\n").encode('utf-8'))
    except Exception:
        pass
    out_path = './gpt_response.txt'
    with io.open(out_path, 'w', encoding='utf-8-sig') as f:
        f.write(fallback_reply + u"\n")
    raise SystemExit(0)

if resp.status_code != 200:
    # Graceful fallback: write a short reply to file, try to match language
    fallback_reply = u"Hello! How can I help you?"
    try:
        # crude check for non-ascii as proxy for non-English
        text_u = file_content_u if isinstance(file_content_u, unicode) else unicode(file_content_u, 'utf-8', 'ignore')
        has_non_ascii = any(ord(c) > 127 for c in text_u)
        if has_non_ascii:
            fallback_reply = u"你好，我能帮你什么？"
    except Exception:
        pass
    try:
        sys.stdout.write((u"[Warning] SoulChat2.0 API error: %s\n" % resp.status_code).encode('utf-8'))
        sys.stdout.write((fallback_reply + u"\n").encode('utf-8'))
    except Exception:
        pass
    out_path = './gpt_response.txt'
    with io.open(out_path, 'w', encoding='utf-8-sig') as f:
        f.write(fallback_reply + u"\n")
    # Stop further processing after fallback
    raise SystemExit(0)

data = resp.json()
model_response = data['choices'][0]['message']['content']
try:
    mr_u_print = model_response if isinstance(model_response, unicode) else unicode(model_response, 'utf-8', 'ignore')
except Exception:
    mr_u_print = unicode(model_response)
try:
    sys.stdout.write((mr_u_print + u"\n").encode('utf-8'))
except Exception:
    pass

out_path = './gpt_response.txt'
with io.open(out_path, 'w', encoding='utf-8-sig') as f:
    # ensure unicode write with newline
    try:
        mr_u = model_response if isinstance(model_response, unicode) else unicode(model_response, 'utf-8', 'ignore')
    except Exception:
        mr_u = unicode(model_response)
    f.write(mr_u + u"\n")

