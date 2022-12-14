import { FC, useCallback } from "react";
import { Button, Col, Empty, List, Row, Tooltip, Typography } from 'antd';
import { UserInfoSchema } from "./api/User";
import { ArticleSchema } from "./api/Article";
import { ActionKind } from "./state/types";
import { useAppContext } from "./state/AppContext";
import { AuthorSchema } from "./api/Author";

import { CodeSandboxOutlined } from '@ant-design/icons';

const { Paragraph, Text } = Typography;

type Props = {
    user?: UserInfoSchema,
    author?: AuthorSchema,
    articles?: ArticleSchema[]
}

export const User: FC<Props> = ({ user, author, articles }: Props) => {
    const { dispatch } = useAppContext();

    const onListItemRender = useCallback((article: ArticleSchema) => {
        const onOpenButtonClick = (article: ArticleSchema) => {
            dispatch({
                type: ActionKind.ShowArticle,
                payload: article
            })
        };

        return <List.Item actions={
            [
                <Button onClick={() => onOpenButtonClick(article)}>
                    Open
                </Button>
            ]
        }>
            <List.Item.Meta
                title={article.title}
                description={`${article.year}`}
            />
        </List.Item>
    }, [dispatch]);

    const renderArticles = useCallback(() => {
        if (articles) {
            return <List
                itemLayout="horizontal"
                dataSource={articles}
                renderItem={onListItemRender}
            />
        }
        else {
            return <Empty description={
                <span>
                    No articles yet
                </span>
            }></Empty>
        }
    }, [articles, onListItemRender])

    const graphShow = useCallback(() => {
        if (author) {
            dispatch({
                type: ActionKind.ShowGraph,
                payload: { id_author: author.id }
            })
        }
    }, [author, dispatch])

    const authorName = useCallback(() => {
        if (author && user) {
            return <>
                <Row gutter={8}>
                    <Col><Typography.Title level={3}>{author.name}</Typography.Title></Col>
                    <Col><Tooltip title="Show graph"><Button shape="circle" icon={<CodeSandboxOutlined />} onClick={ graphShow } /></Tooltip></Col>
                </Row>
                <Paragraph><Text type="secondary">{user.login}</Text></Paragraph>
            </>
        }
        else if (author) {
            return <Typography.Title level={3}>{author.name}</Typography.Title>
        }
        else if (user) {
            return <Typography.Title level={3}>{user.login}</Typography.Title>
        }
        else {
            return <Typography.Title level={3}>Unknown</Typography.Title>
        }
    }, [user, author, graphShow])

    return <Paragraph>
        {authorName()}
        {renderArticles()}
    </Paragraph>
}
