import subprocess
import threading
import time
import requests
from pathlib import Path
import streamlit as st
import json
import base64

class PreviewServer:
    def __init__(self):
        self.process = None
        self.local_url = None

    def start_preview(self, output_dir):
        """Start the local preview server"""
        self.process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=output_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.local_url = "http://localhost:3001"
        return self.local_url

    def stop_preview(self):
        """Stop the local preview server"""
        if self.process:
            self.process.terminate()
            self.process = None

    def get_status(self):
        """Get the status of the local preview server"""
        is_running = self.process is not None
        return {
            "is_running": is_running,
            "local_url": self.local_url if is_running else None
        }

def show_preview_interface():
    """Streamlit interface for local preview functionality"""
    if "preview_server" not in st.session_state:
        st.session_state.preview_server = PreviewServer()
    
    preview_server = st.session_state.preview_server
    status = preview_server.get_status()
    
    st.header("🌐 Local Website Preview")
    
    if not status["is_running"]:
        if st.button("🚀 Start Local Preview", type="primary"):
            output_dir = Path("generated_website")
            if output_dir.exists():
                local_url = preview_server.start_preview(output_dir)
                if local_url:
                    st.success(f"Preview is running locally! 🎉")
                    st.markdown(f"**Local URL:** {local_url}")
                    st.info("💡 Click the URL above to open the preview in a new tab")
                    
                    # Auto-refresh to update status
                    st.rerun()
            else:
                st.error("No generated website found. Please generate a website first.")
    else:
        # Server is running
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.success("✅ Preview server is running")
            st.markdown(f"**Local URL:** {status['local_url']}")
            st.info("💡 Click the URL above to open the preview in your browser")
        
        with col2:
            if st.button("🛑 Stop Preview", type="secondary"):
                preview_server.stop_preview()
                st.rerun()
            
            if st.button("🔄 Refresh Status", type="secondary"):
                st.rerun()
    
    # Show requirements
    with st.expander("📋 Requirements"):
        st.markdown("""
        For local preview to work, you need:
        1. **Node.js** installed on your system
        2. The generated website will run on `http://localhost:3001`
        3. Make sure port 3001 is available
        """)
    
    # Show helpful tips
    with st.expander("💡 Tips"):
        st.markdown("""
        - The preview server runs the actual Next.js development build
        - Hot reload is enabled - changes to files will update automatically
        - Use browser developer tools to inspect the generated website
        - Stop the preview when done to free up system resources
        """)