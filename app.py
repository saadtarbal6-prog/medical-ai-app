import streamlit as st
from groq import Groq

st.set_page_config(page_title="المساعد الطبي الذكي", page_icon="🩺")

st.title("🩺 المساعد الطبي الذكي")
st.write("مرحباً بك! أنا مساعد ذكاء اصطناعي للتحقق من الأعراض والتوعية الصحية.")

st.warning(
    "⚠️ **تنبيه هام:** هذا التطبيق للاسترشاد والتوعية فقط، ولا يغني عن استشارة الطبيب المختص. "
    "إذا كنت تعاني من حالة طارئة، يرجى الاتصال برقم الطوارئ فوراً."
)

api_key = st.sidebar.text_input("أدخل مفتاح Groq API Key:", type="password")

if not api_key:
    st.info("💡 يرجى إدخال مفتاح API في الشريط الجانبي لبدء المحادثة.")
    st.stop()

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """
أنت مساعد طبي ذكي وتوعوي ومؤدب.
قواعدك الصارمة:
1. قدم نصائح توعوية وإرشادات عامة فقط.
2. لا تعطي تشخيصاً نهائياً ومؤكداً للمريض.
3. لا تصف أدوية أو جرعات محددة.
4. اطلب دائماً من المستخدم زيارة الطبيب للتشخيص الدقيق.
5. إذا ذكر المستخدم أعراضاً طارئة، انصحه فوراً بالتوجه للطوارئ.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

if user_input := st.chat_input("اكتب أعراضك أو سؤالك الطبي هنا..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("جاري تحليل السؤال..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.3
            )
            bot_reply = response.choices[0].message.content
            st.write(bot_reply)

    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
