
import random
import pandas as pd
from market_trends import generate_content_plan

trends = [{'topic': 'Test Topic', 'traffic': 'High'}]
try:
    plan = generate_content_plan(trends)
    print("Success!")
    print(plan)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
