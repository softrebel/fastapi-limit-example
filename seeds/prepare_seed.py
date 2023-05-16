import os,sys
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
path=Path(os.path.realpath(__file__))
parent_path = path.parent.parent.absolute()
# sys.path.insert(0,'../')
os.environ["PYTHONPATH"] = "../"
sys.path.extend([str(parent_path)])
