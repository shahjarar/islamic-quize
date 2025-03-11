import streamlit as st
import pandas as pd
import random
import time
import os
import streamlit as st

# 🟢 Custom CSS for Background Image
page_bg_img = '''
<style>
body {
    background-image: url("islamic-background.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
</style>
'''

# ✅ Apply CSS
st.markdown(page_bg_img, unsafe_allow_html=True)

# ✅ Add Other UI Elements
st.title("Islamic Quiz Game")
st.write("Welcome to the Islamic Quiz App!")
st.write("This app will test your knowledge about Islam.")

# 🟢 --- Initialize Session State Variables ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'submitted' not in st.session_state:
    st.session_state.submitted = False
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = None
if 'next_question_clicked' not in st.session_state:
    st.session_state.next_question_clicked = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = time.time()
if 'shuffled_questions' not in st.session_state:
    st.session_state.shuffled_questions = []

# 🟢 --- Questions Data ---
questions = [
    {"question": "Islam me pehla Nabi kaun the?", "options": ["Adam (A.S)", "Ibrahim (A.S)", "Muhammad (S.A.W)"], "answer": "Adam (A.S)"},
    {"question": "Quran me kitni suraten hain?", "options": ["114", "120", "100"], "answer": "114"},
    {"question": "Hajj ek musalman par kab farz hota hai?", "options": ["Har saal", "Zindagi me ek baar", "Kabhi nahi"], "answer": "Zindagi me ek baar"},
    {"question": "Islam ka pehla kalma kya hai?", "options": ["Kalma Tayyaba", "Kalma Shahadat", "Kalma Tauheed"], "answer": "Kalma Tayyaba"},
    {"question": "Islam ki buniyad kitni cheezon par hai?", "options": ["3", "4", "5", "6"], "answer": "5"},
  {
    "question": "Quran Majeed kis zuban mein nazil hua?",
    "options": ["Farsi", "Arabi", "Urdu", "Hebrew"],
    "answer": "Arabi"
  },
  {
    "question": "Islam ka pehla kalma kya hai?",
    "options": [
      "La ilaha illallah Muhammadur Rasulullah",
      "Subhanallah",
      "Bismillah",
      "Allahu Akbar"
    ],
    "answer": "La ilaha illallah Muhammadur Rasulullah"
  },
  {
    "question": "Hazrat Muhammad ﷺ ki walida ka naam kya tha?",
    "options": ["Hazrat Amina", "Hazrat Fatima", "Hazrat Khadija", "Hazrat Maryam"],
    "answer": "Hazrat Amina"
  },
  {
    "question": "Hazrat Jibrael (AS) pehli wahi lekar kab aaye?",
    "options": ["20 saal", "25 saal", "40 saal", "50 saal"],
    "answer": "40 saal"
  },
  {
    "question": "Quran Majeed mein kitni suratein hain?",
    "options": ["100", "114", "110", "120"],
    "answer": "114"
  },
  {
    "question": "Sabse pehli wahi kaun si surat mein nazil hui?",
    "options": ["Surah Al-Fatiha", "Surah Al-Baqarah", "Surah Al-Alaq", "Surah Yaseen"],
    "answer": "Surah Al-Alaq"
  },
  {
    "question": "Islam ka doosra khalifa kaun tha?",
    "options": ["Hazrat Abu Bakr (RA)", "Hazrat Umer (RA)", "Hazrat Usman (RA)", "Hazrat Ali (RA)"],
    "answer": "Hazrat Umer (RA)"
  },
  {
    "question": "Roza rakhna kis Islamic mahine mein farz hai?",
    "options": ["Muharram", "Rajab", "Ramadan", "Zul-Hijjah"],
    "answer": "Ramadan"
  },
  {
    "question": "Hajj ka ek rukn jo sab se bara hai wo kya hai?",
    "options": ["Tawaf", "Sa’i", "Waqoof-e-Arafat", "Rami"],
    "answer": "Waqoof-e-Arafat"
  },
  {
    "question": "Namaz mein kitne faraiz hain?",
    "options": ["5", "6", "7", "8"],
    "answer": "7"
  },
  {
    "question": "Hazrat Muhammad ﷺ ka hijrat ka safar kis shehar se kis shehar tak tha?",
    "options": ["Makka se Madina", "Madina se Makka", "Makka se Taif", "Taif se Madina"],
    "answer": "Makka se Madina"
  },
  {
    "question": "Zakat ki farz hone ki nisab kya hai?",
    "options": ["7 tolay sona", "10 tolay sona", "5 tolay sona", "12 tolay sona"],
    "answer": "7 tolay sona"
  },
  {
    "question": "Quran ki sab se lambi surat kaunsi hai?",
    "options": ["Surah Al-Fatiha", "Surah Al-Baqarah", "Surah Al-Kahf", "Surah Al-Ikhlas"],
    "answer": "Surah Al-Baqarah"
  },
  {
    "question": "Kaun sa farz ibadat hai jo sirf ameer logon par farz hota hai?",
    "options": ["Namaz", "Roza", "Hajj", "Zakat"],
    "answer": "Hajj"
  },
  {
    "question": "Jumma ki namaz kitni rak’aat hoti hai?",
    "options": ["2", "4", "6", "8"],
    "answer": "2"
  },
  {
    "question": "Islam ka pehla ghar konsa hai?",
    "options": ["Masjid-e-Nabwi", "Bait-ul-Maqdis", "Masjid-e-Haram", "Masjid-e-Quba"],
    "answer": "Masjid-e-Haram"
  },
  {
    "question": "Quran kis par nazil hua?",
    "options": ["Hazrat Isa (AS)", "Hazrat Musa (AS)", "Hazrat Muhammad ﷺ", "Hazrat Ibrahim (AS)"],
    "answer": "Hazrat Muhammad ﷺ"
  },
  {
    "question": "Hazrat Muhammad ﷺ ne kitni hijri mein wafat pai?",
    "options": ["8 Hijri", "10 Hijri", "11 Hijri", "12 Hijri"],
    "answer": "11 Hijri"
  },
  {
    "question": "Hazrat Musa (AS) ko Allah se hum kalam hone ka sharaf kaha mila?",
    "options": ["Koh-e-Toor", "Koh-e-Seena", "Masjid-e-Haram", "Bait-ul-Maqdis"],
    "answer": "Koh-e-Toor"
  },
  {
    "question": "Salahuddin Ayyubi ne kaunsa shehar fatah kiya?",
    "options": ["Makka", "Madina", "Quds (Jerusalem)", "Baghdad"],
    "answer": "Quds (Jerusalem)"
  },
  {
    "question": "Duniya ka sab se pehla qibla kaunsa tha?",
    "options": ["Masjid-e-Nabwi", "Masjid-e-Haram", "Masjid-e-Aqsa", "Masjid-e-Quba"],
    "answer": "Masjid-e-Aqsa"
  },
  {
    "question": "Jannat ke kitne darwaze hain?",
    "options": ["4", "6", "8", "10"],
    "answer": "8"
  },
  {
    "question": "Islam ki sab se pehli jang kaunsi thi?",
    "options": ["Jang-e-Badr", "Jang-e-Uhud", "Jang-e-Khandaq", "Jang-e-Tabook"],
    "answer": "Jang-e-Badr"
  },
  {
    "question": "Jis farishte ka kaam rooh kabz karna hai wo kaun hai?",
    "options": ["Hazrat Jibrael (AS)", "Hazrat Mikaeel (AS)", "Hazrat Israfeel (AS)", "Hazrat Izraeel (AS)"],
    "answer": "Hazrat Izraeel (AS)"
  },
  {
    "question": "Quran Majeed ka pehla kalma kya hai?",
    "options": ["Bismillah", "Alif", "Iqra", "Rabbuka"],
    "answer": "Iqra"
  },
  {
    "question": "Sood (riba) Islam mein kaisa hai?",
    "options": ["Jaiz", "Farz", "Halaal", "Haraam"],
    "answer": "Haraam"
  },
  {
    "question": "Islam mein aurat ka maqam kaisa hai?",
    "options": ["Kamzor", "Nafarman", "Izzat aur sharaf wali", "Ghulam"],
    "answer": "Izzat aur sharaf wali"
  },
  {
    "question": "Hazrat Muhammad ﷺ ne farmaya, behtareen insaan wo hai jo...",
    "options": [
      "Apni taqat dikhaye",
      "Ilm hasil kare",
      "Apni maa baap ki izzat kare",
      "Dusron ke liye behtareen ho"
    ],
    "answer": "Dusron ke liye behtareen ho"
  }

]

# 🟢 --- Shuffle Questions on Quiz Start ---
def shuffle_questions():
    st.session_state.shuffled_questions = random.sample(questions, len(questions))

# 🟢 --- Save Score to CSV ---
def save_score():
    new_data = {"Name": st.session_state.user_name, "Score": st.session_state.score}
    
    try:
        df = pd.read_csv("leaderboard.csv")

        # ✅ Agar user pehle exist karta hai, to highest score update karein
        if new_data["Name"] in df["Name"].values:
            df.loc[df["Name"] == new_data["Name"], "Score"] = max(df.loc[df["Name"] == new_data["Name"], "Score"].max(), new_data["Score"])
        else:
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    
    except FileNotFoundError:
        df = pd.DataFrame([new_data])  # Pehli dafa file create ho rahi hai
    
    df.to_csv("leaderboard.csv", index=False)

# 🟢 --- Load Leaderboard ---
def load_leaderboard():
    try:
        df = pd.read_csv("leaderboard.csv")
        return df.sort_values(by="Score", ascending=False)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Score"])


# 🟢 --- Front Page ---
def front_page():
 
    st.title("🕌 Islamic Quiz Game")
    
    st.session_state.user_name = st.text_input("📝 Apna naam likhein:")

    if st.session_state.user_name:
        if st.button("🚀 Quiz Start Karein"):
            shuffle_questions()
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.submitted = False
            st.session_state.selected_option = None
            st.session_state.next_question_clicked = False
            st.session_state.start_time = time.time()
            st.rerun()

# 🟢 --- Quiz Page ---
def quiz_page():

    st.sidebar.title("📊 Player Progress")
    st.sidebar.write(f"👤 **Player:** {st.session_state.user_name}")
    st.sidebar.write(f"✅ **Score:** {st.session_state.score}")
    st.sidebar.write(f"📌 **Question:** {st.session_state.current_question + 1} / {len(st.session_state.shuffled_questions)}")
    st.sidebar.button("🏆 View Leaderboard", on_click=lambda: st.session_state.update({"current_question": len(st.session_state.shuffled_questions)}))

    question_data = st.session_state.shuffled_questions[st.session_state.current_question]
    st.write(f"### ❓ {question_data['question']}")

    # Timer Logic
    time_left = 10 - (time.time() - st.session_state.start_time)
    if time_left > 0:
        st.write(f"⏳ **Time Left:** {int(time_left)} seconds")
    else:
        st.warning("⏰ Time is up! Answer nahi diya.")

    selected_option = st.radio("Options:", question_data['options'], index=None, key=st.session_state.current_question)
    st.session_state.selected_option = selected_option

    if st.session_state.selected_option and time_left > 0:
        if st.button("✅ Submit"):
            st.session_state.submitted = True
            if st.session_state.selected_option == question_data['answer']:
                st.success("🎉 MashaAllah! Sahi jawab.")
                st.session_state.score += 1
            else:
                st.error(f"❌ Ghalat jawab. Sahi jawab: {question_data['answer']}")

    if st.session_state.submitted or time_left <= 0:
        if st.button("➡ Next Question"):
            st.session_state.current_question += 1
            st.session_state.submitted = False
            st.session_state.selected_option = None
            st.session_state.next_question_clicked = False
            st.session_state.start_time = time.time()
            if st.session_state.current_question >= len(st.session_state.shuffled_questions):
                save_score()
                st.session_state.current_question = len(st.session_state.shuffled_questions)
            st.rerun()

# 🟢 --- Leaderboard Page ---
def leaderboard_page():
    
    st.title("🏆 Leaderboard")
    df = load_leaderboard()

    if df.empty:
        st.write("⚠️ Abhi tak koi score record nahi hua!")
    else:
        st.table(df)

    if st.button("🔄 Restart Quiz"):
        shuffle_questions()
        st.session_state.current_question = 0
        st.session_state.score = 0
        st.session_state.submitted = False
        st.session_state.selected_option = None
        st.session_state.next_question_clicked = False
        st.session_state.start_time = time.time()
        st.rerun()
# 🟢 --- Load Leaderboard ---
def load_leaderboard():
    try:
        df = pd.read_csv("leaderboard.csv")
        
        # ✅ Ensure "Score" column exists
        if "Score" not in df.columns:
            st.warning("⚠️ Leaderboard file corrupt hai. Naya leaderboard create ho raha hai.")
            df = pd.DataFrame(columns=["Name", "Score"])
            df.to_csv("leaderboard.csv", index=False)
        
        return df.sort_values(by="Score", ascending=False)
    
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Score"])

# 🟢 --- Main App Logic ---
def main():
    if not st.session_state.user_name:
        front_page()
    elif st.session_state.current_question < len(st.session_state.shuffled_questions):
        quiz_page()
    else:
        leaderboard_page()

if __name__ == "__main__":
 main()