"""
Debug script to test AI functions with various data scenarios
"""
import pandas as pd
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions
try:
    from advanced_techniques import render_ai_next_move
    print("✅ Successfully imported AI functions")
except Exception as e:
    print(f"❌ Error importing AI functions: {e}")
    sys.exit(1)

# Test Case 1: Normal data
print("\n=== Test Case 1: Normal data ===")
try:
    sample_data = pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=10, freq='D'),
        'likes': [100, 120, 90, 110, 130, 80, 140, 95, 125, 115],
        'comments': [10, 12, 9, 11, 13, 8, 14, 9, 12, 11],
        'shares': [5, 6, 4, 5, 7, 3, 8, 4, 6, 5],
        'impressions': [1000, 1200, 900, 1100, 1300, 800, 1400, 950, 1250, 1150],
        'reach': [800, 900, 700, 850, 1000, 650, 1100, 750, 950, 900],
        'follower_count': [10000, 10100, 10050, 10150, 10200, 10100, 10300, 10250, 10350, 10400],
        'media_type': ['Image', 'Video', 'Image', 'Carousel', 'Video', 'Image', 'Video', 'Carousel', 'Image', 'Video']
    })
    
    print("Testing render_ai_next_move with normal data...")
    # Since we're not in Streamlit context, we can't actually render
    # But we can check if the function processes the data without errors
    render_ai_next_move(sample_data)
    print("✅ render_ai_next_move executed successfully with normal data")
except Exception as e:
    print(f"❌ Error with normal data: {e}")
    import traceback
    traceback.print_exc()

# Test Case 2: Empty data
print("\n=== Test Case 2: Empty data ===")
try:
    empty_data = pd.DataFrame()
    print("Testing render_ai_next_move with empty data...")
    render_ai_next_move(empty_data)
    print("✅ render_ai_next_move handled empty data gracefully")
except Exception as e:
    print(f"❌ Error with empty data: {e}")
    import traceback
    traceback.print_exc()

# Test Case 3: Data with missing columns
print("\n=== Test Case 3: Data with missing columns ===")
try:
    partial_data = pd.DataFrame({
        'timestamp': pd.date_range('2023-01-01', periods=5, freq='D'),
        'likes': [100, 120, 90, 110, 130]
    })
    print("Testing render_ai_next_move with partial data...")
    render_ai_next_move(partial_data)
    print("✅ render_ai_next_move handled partial data gracefully")
except Exception as e:
    print(f"❌ Error with partial data: {e}")
    import traceback
    traceback.print_exc()

# Test Case 4: None data
print("\n=== Test Case 4: None data ===")
try:
    print("Testing render_ai_next_move with None data...")
    render_ai_next_move(None)
    print("✅ render_ai_next_move handled None data gracefully")
except Exception as e:
    print(f"❌ Error with None data: {e}")
    import traceback
    traceback.print_exc()

print("\n🎉 Debug test completed!")