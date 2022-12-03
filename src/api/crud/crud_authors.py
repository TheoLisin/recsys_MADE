from pyvis.network import Network
from collections import defaultdict
from typing import Any, Dict, Iterable, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy import func, desc

from db.models import Article, Author, ArticleAuthor, ArticleTag, Tag, AuthorCoauthor
from api.crud.crud_base import resp_to_dict


def author_top_tag(session: Session, tag: str, top: int = 100) -> List[Dict[str, Any]]:

    art_tag = (
        select(ArticleTag.id_article)
        .where(
            ArticleTag.id_tag.in_(
                select(Tag.id.label("tag_id")).where(Tag.tag.ilike(f"{tag}"))
            )
        )
        .cte("art_tag")
    )
    cit_art = (
        select(Article.n_citation.label("n_citation"), Article.id)
        .join(art_tag)
        .cte("cit_art")
    )
    auth_art = (
        select(ArticleAuthor.id_author.label("id_author"), cit_art.c.n_citation)
        .join(cit_art)
        .cte("auth_art")
    )
    auth_cit = (
        select(auth_art.c.id_author, func.sum(auth_art.c.n_citation).label("total"))
        .group_by(auth_art.c.id_author)
        .order_by(desc("total"))
        .cte("auth_cit")
    )

    auth_cit_name = (
        select(Author.id, Author.name, auth_cit.c.total)
        .where(auth_cit.c.total > 0)
        .join(Author)
        .cte("auth_cit_name")
    )

    if top < 0:
        resp = session.query(auth_cit_name).all()
    else:
        resp = session.query(auth_cit_name).limit(top).all()

    return resp_to_dict(resp, ["id_auth", "name", "n_citation"])


def coauthor_adj_lists(session: Session, id_author: int, depth: int = 2):
    coauths_adj = defaultdict(list)
    to_handle = [id_author]
    set_of_auths = set()
    cdepth = 0
    coauths_count = 1
    while cdepth < depth:
        cur_count = coauths_count
        coauths_count = 0
        while cur_count > 0:
            cur_auth_id = to_handle.pop(-1)
            coauth_list = _unpack_coauths(session, cur_auth_id, id_author)
            set_of_auths = set_of_auths.union(coauth_list)
            coauths_adj[cur_auth_id] = coauth_list
            cur_count -= 1
            coauths_count += len(coauth_list)
            to_handle.extend(coauth_list)
        cdepth += 1
    names = _get_names(session, [id_author], None)
    names = _get_names(session, set_of_auths, names)
    return coauths_adj, names


def _unpack_coauths(session: Session, id_auth: int, root_id: int) -> List[int]:
    coaths = session.execute(
        select(AuthorCoauthor.id_coauth).where(AuthorCoauthor.id_author == id_auth)
    )
    return [co[0] for co in coaths if co[0] != root_id]


def _get_names(
    session: Session,
    ids: Iterable[int],
    init_dct: Optional[Dict[int, str]] = None,
) -> Dict[int, str]:
    if init_dct is None:
        init_dct = {}

    for id_a in ids:
        if id_a in init_dct:
            continue
        name = session.execute(select(Author.name).where(Author.id == id_a)).first()
        init_dct[id_a] = name[0]

    return init_dct


def create_graph(session: Session, id_author: int, depth: int = 2) -> Network:
    coauthors, names = coauthor_adj_lists(session, id_author, depth)
    net = Network()

    for id_a in names:
        if id_a == id_author:
            net.add_node(id_a, label=names[id_a], color="#ff8cdb")
        else:
            net.add_node(id_a, label=names[id_a], size=10)

    for ath in coauthors.keys():
        for ca in coauthors[ath]:
            net.add_edge(ath, ca)

    net.generate_html()
    return net
