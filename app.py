import streamlit as st
import pandas as pd

# ওয়েবসাইটের টাইটেল ও কনফিগারেশন
st.set_page_config(page_title="Walton Product Price Finder", page_icon="💻", layout="centered")

st.title("📱 ওয়ালটন প্রোডাক্ট প্রাইস ফাইন্ডার")
st.write("আপনার কাঙ্ক্ষিত ওয়ালটন মডেলটি লিখে দ্রুত প্রাইস খুঁজে বের করুন।")

# এক্সেল ফাইল লোড করার ফাংশন
@st.cache_data
def load_data():
    file_path = "Walton.xlsx"
    xls = pd.ExcelFile(file_path)
    all_data = []
    
    # সবগুলো শিটের ডাটা একসাথে কম্বাইন করা
    for sheet in xls.sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        
        # শুধুমাত্র প্রয়োজনীয় প্রথম ৩টি কলাম নেওয়া হচ্ছে
        if df.shape[1] >= 3:
            df = df.iloc[:, :3] 
            df.columns = ['Product Name', 'Model', 'Price']
            all_data.append(df)
        
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # মডেলের নাম ও প্রাইস অনুযায়ী ডুপ্লিকেট (রিপিট) ডাটা রিমুভ করা
    combined_df = combined_df.drop_duplicates(subset=['Model', 'Price'])
    
    return combined_df

try:
    df = load_data()

    # সার্চ বার তৈরি
    search_query = st.text_input("🔍 মডেলের নাম লিখুন (যেমন: WFC-3F5, WFE, ইত্যাদি):", "")

    if search_query:
        # মডেলে সার্চ কোয়েরি আছে কিনা তা ফিল্টার করা (case-insensitive)
        results = df[df['Model'].astype(str).str.contains(search_query, case=False, na=False)]
        
        if not results.empty:
            st.success(f"🎉 মোট {len(results)}টি প্রোডাক্ট পাওয়া গেছে!")
            
            st.write("---") # একটি ডিভাইডার লাইন
            
            # প্রতিটি মডেল ও প্রাইস এক লাইনে বড় অক্ষরে দেখানো
            for index, row in results.iterrows():
                # HTML ব্যবহার করে ফন্ট সাইজ বড় (20px) এবং এক লাইনে করা হয়েছে
                st.markdown(f"<p style='font-size:20px; font-weight:bold; margin-bottom:10px;'>📦 {row['Model']} — <span style='color:#2ecc71;'>{row['Price']}</span></p>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ দুঃখিত, এই মডেলের কোনো প্রোডাক্ট পাওয়া যায়নি। অনুগ্রহ করে সঠিক বানান চেক করুন।")
            
except FileNotFoundError:
    st.error("❌ 'Walton.xlsx' ফাইলটি খুঁজে পাওয়া যায়নি। অনুগ্রহ করে ফাইলটি একই ফোল্ডারে রাখুন।")
except Exception as e:
    st.error(f"❌ একটি সমস্যা হয়েছে: {e}")
