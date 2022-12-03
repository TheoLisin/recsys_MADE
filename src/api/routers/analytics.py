from api import schemas
from api.crud.crud_authors import author_top_tag, create_graph

from db.db_params import get_session

from typing import List
from fastapi import APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter(prefix="/analytics")


@router.get("/top", tags=["Authors"], response_model=List[schemas.PAuthorTop])
def top_authors(tag: str, top: int = 100):
    with get_session() as session:
        resp = author_top_tag(session, tag, top)
    return resp


@router.get("/graph")
def redirect():
    return RedirectResponse(url="/analytics/graph/1")


@router.get("/graph/{id_auth}", tags=["Authors"], response_class=HTMLResponse)
def graph_coauth(id_auth: int):
    with get_session() as session:
        net = create_graph(session, id_auth)
    return net.html
