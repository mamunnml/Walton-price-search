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
        df['Category'] = sheet  # শিটের নাম ক্যাটাগরি হিসেবে যোগ করা
        all_data.append(df)
        
    combined_df = pd.concat(all_data, ignore_index=True)
    # কলামের নামগুলো সুন্দর করা
    combined_df.columns = ['Product Name', 'Model', 'Price', 'Category']
    return combined_df

try:
    df = load_data()

    # সার্চ বার তৈরি
    search_query = st.text_input("🔍 মডেলের নাম লিখুন (যেমন: WFC-3F5, WFE, ইত্যাদি):", "")

    if search_query:
        # মডেলে সার্চ কোয়েরি আছে কিনা তা ফিল্টার করা (case-insensitive)
        results = df[df['Model'].str.contains(search_query, case=False, na=False)]
        
        if not results.empty:
            st.success(f"🎉 মোট {len(results)}টি প্রোডাক্ট পাওয়া গেছে!")
            
            # রেজাল্ট সুন্দরভাবে কার্ড আকারে বা টেবিল আকারে দেখানো
            for index, row in results.iterrows():
                with st.expander(f"📦 {row['Model']} — {row['Price']}", expanded=True):
                    st.write(f"**প্রোডাক্টের ধরন:** {row['Product Name']}")
                    st.write(f"**ক্যাটাগরি:** {row['Category']}")
                    st.write(f"**মূল্য:** :green[{row['Price']}]")
        else:
            st.warning("⚠️ দুঃখিত, এই মডেলের কোনো প্রোডাক্ট পাওয়া যায়নি। অনুগ্রহ করে সঠিক বানান চেক করুন।")
            
except FileNotFoundError:
    st.error("❌ 'Walton.xlsx' ফাইলটি খুঁজে পাওয়া যায়নি। অনুগ্রহ করে ফাইলটি একই ফোল্ডারে রাখুন।")
