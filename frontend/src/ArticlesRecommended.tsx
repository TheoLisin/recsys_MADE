import { useDLE } from "@rest-hooks/react";
import { Button, Empty, List, Pagination, Skeleton, Tag, Typography } from "antd";
import { FC, useCallback, useState } from "react";

import { ArticleRecommendResource, ArticleRecommendSchema } from "./api/Article";
import { FIRST_PAGE_INDEX, PAGE_SIZE } from "./api/consts";
import { Error } from "./Error";
import { Loading } from "./Loading";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";

const { Title, Paragraph } = Typography;

type ArticlesProps = {
    articles: Array<ArticleRecommendSchema>
    loading?: boolean
}

const ArticlesList: FC<ArticlesProps> = ({ articles, loading }) => {
    const { dispatch } = useAppContext();

    const onOpenButtonClick = (article: ArticleRecommendSchema) => {
        dispatch({
            type: ActionKind.ShowArticle,
            payload: article
        })
    };

    const onListItemRender = (article: ArticleRecommendSchema) => (
        <List.Item actions={
            !loading ? [
                <Button onClick={() => onOpenButtonClick(article)}>
                    Open
                </Button>
            ] : undefined
        }>
            <Skeleton loading={loading} active paragraph={{ rows: 1 }}>
                <List.Item.Meta
                    title={article.title}
                    description={
                        <Paragraph ellipsis={true}>
                            Tags: {article.tags.map((text) => <Tag>{text}</Tag>)}
                        </Paragraph>
                    }
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

export const ArticlesRecommend: FC = () => {
    const [page, setPage] = useState(FIRST_PAGE_INDEX);
    const { data, loading, error } = useDLE(ArticleRecommendResource.getList, { page: page });

    const onPageChange = (page: number) => {
        setPage(page);
    }

    const articles = useCallback(() => {
        if (error && error.status !== 422) {
            return <Error
                title={"Failed to read articles"}
                msg={error.message}
                status={error.status as number}
            />
        }
        else if (error && error.status === 422) {
            return <Empty />
        }
        else if (loading) {
            return <Loading />;
        }
        else if (data) {
            return <>
                <Title level={4}>Recommended articles</Title>
                <ArticlesList articles={data} />
            </>
        }
        else {
            return <Empty />
        }
    }, [error, data, loading])

    return <>
        {articles()}
        {(data && data.length >= PAGE_SIZE) &&
            <Pagination defaultCurrent={page} total={100000} onChange={onPageChange} />}
    </>
}
