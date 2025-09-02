import streamlit as st
import sys
from pathlib import Path

current_dir = Path(__file__).parent.parent.parent
sys.path.append(str(current_dir))

from enhanced_integration.core.key_manager import enhanced_key_manager
from enhanced_integration.core.database_service import enhanced_db_service

st.set_page_config(page_title="JARVIS Enhanced", layout="wide")

def main():
    st.title("🚀 JARVIS Enhanced Dashboard")
    
    # System status
    try:
        enhanced_db_service.initialize()
        data = enhanced_db_service.get_dashboard_data()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Companies", data['total_companies'])
        with col2:
            st.metric("Contacts", data['total_contacts'])  
        with col3:
            st.metric("Verified", data['verified_contacts'])
            
        st.success("Enhanced System is running!")
        
    except Exception as e:
        st.error(f"System error: {e}")

if __name__ == "__main__":
    main()
