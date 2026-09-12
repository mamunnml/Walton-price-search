import streamlit as st
import pandas as pd

# ওয়েবসাইটের টাইটেল ও কনফিগারেশন
st.set_page_config(page_title="Walton Product Price Finder", page_icon="💻", layout="centered")

st.title("📱 ওয়ালটন প্রোডাক্ট প্রাইস ফাইন্ডার")
st.write("আপনার কাঙ্ক্ষিত ওয়ালটন মডেলটি লিখে দ্রুত প্রাইস খুঁজে বের করুন।")

# এক্সেল ফাইল লোড করার ফাংশন
@st.cache_data
def load_data():
    file_path = "WALTON price.xlsx"
    df = pd.read_excel(file_path, sheet_name="ALL")
    
    # প্রথম ৩টি কলাম সুনির্দিষ্ট করা
    df = df.iloc[:, :3] 
    df.columns = ['Category', 'Model', 'Price']
    
    # মডেলের নাম ও প্রাইস অনুযায়ী রিপিট/ডুপ্লিকেট ডাটা রিমুভ করা
    df = df.drop_duplicates(subset=['Model', 'Price'])
    
    return df

try:
    df = load_data()

    # সার্চ বার তৈরি
    search_query = st.text_input("🔍 মডেলের নাম লিখুন (যেমন: WFK, WFC, ইত্যাদি):", "")

    if search_query:
        # মডেলে সার্চ কোয়েরি আছে কিনা তা ফিল্টার করা (case-insensitive)
        results = df[df['Model'].astype(str).str.contains(search_query, case=False, na=False)]
        
        if not results.empty:
            st.success(f"🎉 মোট {len(results)}টি প্রোডাক্ট পাওয়া গেছে!")
            st.write("---")
            
            # প্রতিটি মডেল ও প্রাইস এক লাইনে বড় অক্ষরে দেখানো
            for index, row in results.iterrows():
                st.markdown(
                    f"<p style='font-size:20px; font-weight:bold; margin-bottom:12px;'>"
                    f"📦 {row['Model']} — <span style='color:#2ecc71;'>{row['Price']}</span>"
                    f"</p>", 
                    unsafe_allow_html=True
                )
        else:
            st.warning("⚠️ দুঃখিত, এই মডেলের কোনো প্রোডাক্ট পাওয়া যায়নি। অনুগ্রহ করে সঠিক বানান চেক করুন।")
            
except FileNotFoundError:
    st.error("❌ 'WALTON price.xlsx' ফাইলটি খুঁজে পাওয়া যায়নি। অনুগ্রহ করে গিটহাবে ফাইলটির নাম সঠিক আছে কিনা নিশ্চিত করুন।")
except Exception as e:
    st.error(f"❌ একটি সমস্যা হয়েছে: {e}")