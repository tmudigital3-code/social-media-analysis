"""
Test script to verify that all imports work correctly
"""
import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("Testing imports...")

# Test main dashboard import
try:
    import professional_dashboard
    print("✅ professional_dashboard imported successfully")
except Exception as e:
    print(f"❌ Error importing professional_dashboard: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test that render_ai_next_move is available
try:
    from professional_dashboard import render_ai_next_move
    print("✅ render_ai_next_move function is available")
except Exception as e:
    print(f"❌ Error accessing render_ai_next_move: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test that the function can be called
try:
    # Just check that it exists and is callable
    if callable(render_ai_next_move):
        print("✅ render_ai_next_move is callable")
    else:
        print("❌ render_ai_next_move is not callable")
        sys.exit(1)
except Exception as e:
    print(f"❌ Error checking if render_ai_next_move is callable: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n🎉 All import tests passed!")