import { useDLE } from "@rest-hooks/react";
import { Button, Col, Empty, Form, Input, List, Row, Skeleton, Tooltip, Typography } from "antd";
import { FC, useCallback, useState } from "react";
import { CodeSandboxOutlined } from '@ant-design/icons';


import { AnalyticsTopResource, TopAuthorSchema } from "./api/Analytics";
import { Loading } from "./Loading";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";
import { Error } from "./Error";

type SearchProps = {
    onApply: (filters: Filters) => void
}

const { Title } = Typography;

export const TagsFilter: FC<SearchProps> = ({ onApply }) => {
    const onFromSubmit = (values: any) => {
        // Remove undefined and empty fields
        Object.keys(values).forEach(key => {
            if (values[key] === undefined || values[key] === "") {
                delete values[key];
            }
        });

        onApply(values);
    }

    return <Form name="top_search" onFinish={onFromSubmit}>
        <Row gutter={12}>
            <Col span={8}>
                <Form.Item name={"tag_part"}>
                    <Input placeholder="Enter tag" />
                </Form.Item>
            </Col>
            <Col span={1}>
                <Button type="primary" htmlType="submit">
                    Show
                </Button>
            </Col>
        </Row>
    </Form>
}

type TopAuthorsProps = {
    authors: Array<TopAuthorSchema>
    loading?: boolean
}

const TopAuthorsList: FC<TopAuthorsProps> = ({ authors, loading }) => {
    const { dispatch } = useAppContext();

    const onOpenButtonClick = (author: TopAuthorSchema) => {
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

    const onListItemRender = (author: TopAuthorSchema) => (
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
                    description={`Total number of citations: ${author.n_citation}`}
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

export type Filters = {
    tag_part?: string
}

export const TopAuthors: FC = () => {
    const [filters, setFilters] = useState<Filters | null>(null)

    const { data, loading, error } = useDLE(AnalyticsTopResource, filters ? { ...filters } : null );

    /** Apply filters */
    const onFiltersApply = useCallback((new_filters: Filters) => {
        const isEmpty = Object.keys(new_filters).length === 0;
        if (!isEmpty) {
            setFilters(new_filters)
        }
        else {
            setFilters(null)
        }
    }, [])

    const authors = useCallback(() => {
        if (error && error.status !== 422) {
            return <Error
                title="Failed to read top authors"
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
                <Title level={4}>Top for tag: "{data.tag}"</Title>
                <TopAuthorsList authors={data.data} />
            </>
        }
        else {
            return <Empty description="Enter the tag to find top users"></Empty>
        }
    }, [error, data, loading])

    return <>
        <TagsFilter onApply={onFiltersApply} />
        {authors()}
    </>
}
