import sys
import os

# Add root directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Run dashboard application
exec(open("dashboard/app.py").read())
