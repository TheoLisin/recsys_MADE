from pyvis.network import Network
from collections import defaultdict
from typing import Any, Dict, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.sql import select
from sqlalchemy import func, desc, and_

from api.crud.crud_base import resp_to_dict

from db.models import Article, Author, ArticleAuthor, ArticleTag, Tag, AuthorCoauthor


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

    return resp_to_dict(resp, ["id_author", "name", "n_citation"])


def coauthor_adj_lists(session: Session, id_author: int, depth: int = 2):
    coauths_adj = defaultdict(list)
    to_handle = [id_author]
    names = {}
    set_of_auths = set()
    cdepth = 0
    coauths_count = 1

    while cdepth < depth:
        cur_count = coauths_count
        coauths_count = 0

        while cur_count > 0:
            cur_auth_id = to_handle.pop(-1)
            coauth_list, new_names = _unpack_coauths(session, cur_auth_id, id_author)
            names.update(new_names)
            set_of_auths = set_of_auths.union(coauth_list)
            coauths_adj[cur_auth_id] = coauth_list
            cur_count -= 1
            coauths_count += len(coauth_list)
            to_handle.extend(coauth_list)
        cdepth += 1

    return coauths_adj, names


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


def _unpack_coauths(
    session: Session,
    id_auth: int,
    root_id: int,
) -> Tuple[List[int], Dict[int, str]]:
    coauths = (
        select(
            AuthorCoauthor.id_coauth,
            Author.name,
        )
        .join(Author, and_(Author.id == AuthorCoauthor.id_coauth))
        .where(AuthorCoauthor.id_author == id_auth)
    )
    coauths_w_names = session.execute(coauths).all()
    coauths_lst = [ca[0] for ca in coauths_w_names if ca[0] != root_id]
    names_dct = {ca[0]: ca[1] for ca in coauths_w_names}

    return coauths_lst, names_dct


def get_author_articles(session: Session, id_author: int):
    arts = (
        session.query(ArticleAuthor.id_article)
        .filter(ArticleAuthor.id_author == id_author)
        .all()
    )
    return [atpl[0] for atpl in arts]


def get_auth_recommendation(session: Session, id_author: int, max_rank: int = 10):
    auth_art_count = (
        select(
            ArticleAuthor.id_author.label("id_author"),
            func.count(ArticleAuthor.id_article).label("count"),
        )
        .group_by("id_author")
        .order_by(desc("count"))
        .cte("auth_art_count")
    )

    auth_tag = (
        select(
            ArticleAuthor.id_author.label("id_author"),
            ArticleTag.id_tag.label("id_tag"),
        )
        .join(ArticleAuthor, ArticleAuthor.id_article == ArticleTag.id_article)
        .distinct()
    ).cte("auth_tag")

    auth_tag_num = (
        select(
            auth_tag.c.id_tag.label("tag"),
            auth_tag.c.id_author.label("auth"),
            auth_art_count.c.count.label("count"),
        ).join(auth_art_count, auth_art_count.c.id_author == auth_tag.c.id_author)
    ).cte("auth_tag_num")

    cur_at = select(auth_tag.c.id_tag).where(auth_tag.c.id_author == id_author)
    auth_tag = session.execute(cur_at).all()
    tags = [at[0] for at in auth_tag]

    auth_tag_num_cat = select(
        auth_tag_num.c.tag.label("tag"),
        auth_tag_num.c.auth.label("auth"),
        auth_tag_num.c.count.label("count"),
    ).where(auth_tag_num.c.tag.in_(tags))

    auth_tag_num_cat_part = select(
        auth_tag_num_cat.c.tag,
        auth_tag_num_cat.c.auth,
        auth_tag_num_cat.c.count.label("count"),
        func.row_number()
        .over(partition_by=auth_tag_num_cat.c.tag, order_by=desc("count"))
        .label("rank"),
    ).cte("auth_tag_num_part")

    possible_coath = session.execute(
        select("*")
        .select_from(auth_tag_num_cat_part)
        .where(auth_tag_num_cat_part.c.rank <= max_rank)
    ).all()

    return {(pc[1], pc[2]) for pc in possible_coath}
