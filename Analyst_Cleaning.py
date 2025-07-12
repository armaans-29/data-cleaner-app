import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder

st.title("📊 Data Analyst – Smart Data Cleaner")

uploaded_file = st.file_uploader("📤 Upload CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file:
    try:
        # Read file
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
            file_type = "csv"
        else:
            df = pd.read_excel(uploaded_file)
            file_type = "xlsx"

        st.subheader("📄 Original Data")
        st.dataframe(df.head())

        # Cleaning
        df.drop_duplicates(inplace=True)
        df.fillna(df.mean(numeric_only=True), inplace=True)
        df.fillna("Unknown", inplace=True)

        for col in df.select_dtypes(include='object'):
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))

        st.subheader("✅ Cleaned Data (No Scaling)")
        st.dataframe(df.head())

        # Download cleaned file
        if file_type == "csv":
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Cleaned CSV", csv, "cleaned_data.csv", "text/csv")
        else:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
                writer.save()
                processed_data = output.getvalue()
            st.download_button("📥 Download Cleaned Excel", processed_data, "cleaned_data.xlsx")

    except Exception as e:
        st.error(f"❌ Error: {e}")


#  To Run in terminal --> "C:\Users\arsit\AppData\Local\Programs\Python\Python38\python.exe" -m streamlit run Analyst_Cleaning.py