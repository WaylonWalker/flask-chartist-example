
import os
import sys
from matplotlib import rcParams

rcParams['font.family'] = 'Tunga'

try:
    root_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
except NameError:
    root_dir = os.path.abspath(os.path.dirname(_dh[0]))
reports_dir = os.path.join(root_dir, 'reports')
data_dir = os.path.join(root_dir, 'data')
raw_data_dir = os.path.join(root_dir, 'data', 'raw')
processed_data_dir = os.path.join(root_dir, 'data', 'processed')
src_dir = os.path.join(root_dir, 'src')
analysis_dir = os.path.dirname(root_dir)
static_dir = os.path.join(src_dir, 'static')

sys.path.append(analysis_dir)
sys.path.append(root_dir)
sys.path.append(src_dir)
