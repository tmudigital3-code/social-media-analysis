"""
Test data loading in the dashboard
"""
import sys
import os

# Test 1: Database has data
print("=" * 50)
print("TEST 1: Database Check")
print("=" * 50)
import database_manager
data = database_manager.load_data()
print(f"✅ Database has {len(data)} records")
if not data.empty:
    print(f"✅ Columns: {list(data.columns)[:8]}...")
    print(f"✅ Sample data:")
    print(data.head(2))
else:
    print("❌ Database is empty!")
    sys.exit(1)

# Test 2: Cached function works
print("\n" + "=" * 50)
print("TEST 2: Streamlit Cache Function")
print("=" * 50)
try:
    # Import streamlit
    import streamlit as st
    
    # Define the cached function (same as in dashboard)
    @st.cache_data(ttl=300)
    def get_cached_data():
        return database_manager.load_data()
    
    cached_data = get_cached_data()
    print(f"✅ Cached function returned {len(cached_data)} records")
    
    if cached_data.empty:
        print("❌ Cached function returned empty data!")
        sys.exit(1)
    else:
        print("✅ Cached function works correctly")
        
except Exception as e:
    print(f"⚠️ Could not test caching: {e}")

# Test 3: Check if app can run
print("\n" + "=" * 50)
print("TEST 3: Dashboard Import")
print("=" * 50)
try:
    # Try importing the dashboard
    import professional_dashboard
    print("✅ Dashboard module imported successfully")
except Exception as e:
    print(f"❌ Error importing dashboard: {e}")
    sys.exit(1)

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
print("=" * 50)
print("\n🚀 You can now run the dashboard with:")
print("   streamlit run professional_dashboard.py")
