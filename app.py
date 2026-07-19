# app.py - The Protected Enterprise Gateway Viewport
import streamlit as st
import requests

st.set_page_config(page_title="m-PAIRS Gateway", layout="wide")
st.title("🛡️ m-PAIRS | Enterprise Gateway")

# Access Control & Inputs
api_key = st.text_input("Access Token", type="password")
query_input = st.text_area(
    "Grievance / Audit Target Text", 
    placeholder="Type or paste your query/context parameters here...", 
    height=150
)

# NEW: Document Ingestion Field (Supports PDF, Word, and Plain Text)
uploaded_file = st.file_uploader(
    "Upload Supporting Evidence / Reference Files", 
    type=["pdf", "docx", "txt"]
)

if st.button("Execute m-PAIRS Engine", type="primary"):
    if not api_key:
        st.error("Access Denied: Please provide a valid Access Token.")
    elif not query_input.strip():
        st.error("Input Error: The text query field cannot be empty.")
    else:
        # Your proprietary prompt logic remains safely isolated behind this endpoint URL
        MPAIRS_SECURE_ENDPOINT = "https://engine.totalstrategies.workers.dev/v1/execute" 
        headers = {"Authorization": f"Bearer {api_key}"}
        
        # Base textual data payload
        data_payload = {"target_text": query_input}
        
        try:
            with st.spinner("Streaming data to secure m-PAIRS execution layer..."):
                if uploaded_file:
                    # Package the binary file data securely for multipart transmission
                    file_payload = { 
                        "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                    }
                    # Sending text parameters and files simultaneously
                    response = requests.post(
                        MPAIRS_SECURE_ENDPOINT, data=data_payload, files=file_payload, headers=headers, timeout=90
                    )
                else:
                    # Fallback to standard JSON payload if no document is attached
                    response = requests.post(
                        MPAIRS_SECURE_ENDPOINT, json=data_payload, headers=headers, timeout=60
                    )
                    
                # Check for server-side errors
                if response.status_code == 200:
                    st.success("✅ System Audit Complete")
                    st.markdown(response.json()["resolution"])
                else:
                    st.error(f"Backend Server Error ({response.status_code}): {response.text}")
                    
        except requests.exceptions.Timeout:
            st.error("Execution Timeout: The heavy document analysis exceeded the network buffer window.")
        except Exception as e:
            st.error(f"Gateway Connection Failure: {str(e)}")
window.)
except Exception as e:
st.error(f"Gateway Connection Failure: {str(e)}")
