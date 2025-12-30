"""
Clear Streamlit cache and verify data loading
"""
import os
import shutil

# Clear Streamlit cache directory
cache_dir = os.path.join(os.path.expanduser("~"), ".streamlit", "cache")
if os.path.exists(cache_dir):
    try:
        shutil.rmtree(cache_dir)
        print("✅ Streamlit cache cleared successfully!")
    except Exception as e:
        print(f"⚠️ Error clearing cache: {e}")
else:
    print("ℹ️ No cache directory found")

# Verify database has data
import database_manager
data = database_manager.load_data()
print(f"\n📊 Database Status:")
print(f"   Total records: {len(data)}")
if not data.empty:
    print(f"   Columns: {list(data.columns)[:5]}...")
    print(f"   Date range: {data['timestamp'].min()} to {data['timestamp'].max()}" if 'timestamp' in data.columns else "   No timestamp column")
    print("\n✅ Data is ready! You can now run the dashboard.")
else:
    print("\n⚠️ Database is empty. Please upload data.")

print("\n🚀 To start the dashboard, run:")
print("   streamlit run professional_dashboard.py")
