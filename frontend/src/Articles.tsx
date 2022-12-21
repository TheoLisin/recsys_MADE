import { useDLE } from "@rest-hooks/react";
import { Button, List, Pagination, Skeleton } from "antd";
import { FC, useCallback, useState } from "react";

import { ArticleAllResource, ArticleSchema, ArticleSearchResource } from "./api/Article";
import { FIRST_PAGE_INDEX, PAGE_SIZE } from "./api/consts";
import { ArticlesFilters } from "./ArticlesFilters";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";
import { Error } from "./Error";

type ArticlesListProps = {
    articles: Array<ArticleSchema>
    loading?: boolean
}

const ARTICLES_STUBS =
    Array<ArticleSchema>(PAGE_SIZE).fill(new ArticleSchema());

const ArticlesList: FC<ArticlesListProps> = ({ articles, loading }) => {
    const { dispatch } = useAppContext();

    const onOpenButtonClick = (article: ArticleSchema) => {
        dispatch({
            type: ActionKind.ShowArticle,
            payload: article
        })
    };

    const onListItemRender = (article: ArticleSchema) => (
        <List.Item actions={
            !loading ? [
                <Button onClick={() => onOpenButtonClick(article)}>
                    Open
                </Button>
            ] : undefined
        }>
            <Skeleton loading={loading} active paragraph={{rows: 1}}>
                <List.Item.Meta
                    title={article.title}
                    description={`${article.year}`}
                />
            </Skeleton>
        </List.Item>
    )

    return <List
        itemLayout="horizontal"
        dataSource={articles}
        renderItem={onListItemRender}
    />
}

export type Filters = {
    year?: number,
    author_name?: string,
    journal_name?: string,
    tag?: string
}

type ResourceType = typeof ArticleAllResource | typeof ArticleSearchResource;

export const Articles: FC = () => {
    const [page, setPage] = useState(FIRST_PAGE_INDEX);

    const [articlesResource, setArticlesResource] = useState<ResourceType>(ArticleAllResource)
    const [filters, setFilters] = useState<Filters>({})

    const { data, loading, error } = useDLE(articlesResource.getList, { page: page, ...filters });

    /** Change resource type and apply filters */
    const onFiltersApply = useCallback((new_filters: Filters) => {
        const isEmpty = Object.keys(new_filters).length === 0;
        if (!isEmpty) {
            setArticlesResource(ArticleSearchResource)
            setFilters(new_filters)
            setPage(FIRST_PAGE_INDEX);
        }
        else {
            setArticlesResource(ArticleAllResource)
            setFilters({})
            setPage(FIRST_PAGE_INDEX);
        }
    }, [])

    const onPageChange = (page: number) => {
        setPage(page);
    }

    const articles = useCallback(() => {
        if (error) {
            return <Error
                title={`Failed to read articles from page ${page}`}
                msg={error.message}
                status={error.status as number}
            />
        }
        else if (loading || !data) {
            return <ArticlesList articles={ARTICLES_STUBS} loading={loading} />
        }
        else {
            return <ArticlesList articles={data} />
        }
    }, [error, data, loading, page])

    return <>
        <ArticlesFilters onApply={onFiltersApply} />
        {articles()}
        {(data && data.length >= PAGE_SIZE) &&
            <Pagination defaultCurrent={page} total={100000} onChange={onPageChange} />}
    </>
}
 