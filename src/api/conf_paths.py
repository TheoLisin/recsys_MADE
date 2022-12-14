from pathlib import Path

SRC_PATH = Path().cwd() / "src"
API_PATH = SRC_PATH / "api"
ML_PATH = SRC_PATH / "ml"
DB_PATH = SRC_PATH / "db"

MODELS_PATH = ML_PATH / "models"
MODELS_PATH.mkdir(exist_ok=True)

GRAPH_TEMPLATE = SRC_PATH / "templates" / "graph_template.html"
