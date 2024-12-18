import os
import sys

def add_project_root_to_sys_path():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
    if project_root not in sys.path:
        sys.path.append(project_root)