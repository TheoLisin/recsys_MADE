import { useDLE } from "@rest-hooks/react";
import { Button, Empty, List, Skeleton, Tooltip, Typography } from "antd";
import { FC, useCallback } from "react";
import { CodeSandboxOutlined } from '@ant-design/icons';

import { AuthorRecommendSchema, AuthorsRecommendResource } from "./api/Author";
import { Loading } from "./Loading";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";

const { Title } = Typography;

type AuthorsProps = {
    authors: Array<AuthorRecommendSchema>
    loading?: boolean
}

const AuthorsList: FC<AuthorsProps> = ({ authors, loading }) => {
    const { dispatch } = useAppContext();

    const onOpenButtonClick = (author: AuthorRecommendSchema) => {
        dispatch({
            type: ActionKind.ShowAuthorInfo,
            payload: author.id_author
        })
    };

    const graphShow = useCallback((id_author: number) => {
        dispatch({
            type: ActionKind.ShowGraph,
            payload: { id_author }
        })
    }, [dispatch])

    const onListItemRender = (author: AuthorRecommendSchema) => (
        <List.Item actions={
            !loading ? [
                <Button onClick={() => onOpenButtonClick(author)}>
                    Open
                </Button>,
                <Tooltip title="Show graph">
                    <Button shape="circle" icon={<CodeSandboxOutlined />} onClick={() => graphShow(author.id_author)} />
                </Tooltip>
            ] : undefined
        }>
            <Skeleton loading={loading} active paragraph={{ rows: 1 }}>
                <List.Item.Meta
                    title={author.name}
                    description={`Count of articles: ${author.n_articles}`}
                />
            </Skeleton>
        </List.Item>
    )

    return <List
        itemLayout="horizontal"
        dataSource={authors}
        renderItem={onListItemRender}
    />
}

export const AuthorsRecommended: FC = () => {
    const { data, loading, error } = useDLE(AuthorsRecommendResource.getList);

    const authors = useCallback(() => {
        if (error && error.status !== 422) {
            return <div>
                <>Failed read top authors. Error {error.status}</>
            </div>;
        }
        else if (error && error.status === 422) {
            return <Empty />
        }
        else if (loading || !data) {
            return <Loading />;
        }
        else {
            return <>
                <Title level={4}>Recommended coauthors</Title>
                <AuthorsList authors={data} />
            </>
        }
    }, [error, data, loading])

    return <>
        {authors()}
    </>
}
