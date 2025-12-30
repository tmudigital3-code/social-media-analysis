"""
Reset and restart the Streamlit app
This clears all caches and session state
"""
import os
import shutil
import subprocess
import sys

print("🔄 Resetting Streamlit application...")

# 1. Clear Streamlit cache
cache_dir = os.path.join(os.path.expanduser("~"), ".streamlit", "cache")
if os.path.exists(cache_dir):
    try:
        shutil.rmtree(cache_dir)
        print("✅ Cache cleared")
    except Exception as e:
        print(f"⚠️ Could not clear cache: {e}")

# 2. Verify database
import database_manager
data = database_manager.load_data()
print(f"📊 Database has {len(data)} records")

# 3. Start the app
print("\n🚀 Starting Streamlit app...")
print("=" * 50)

# Use subprocess to run streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", "professional_dashboard.py"])
