import { FC } from "react";
import { Typography } from 'antd';

const { Paragraph, Text } = Typography;

export interface ArticleInfo {
    title: string,
    year: string,
    abstract: string
}

type Props = {
    article: ArticleInfo,
    fullInfo?: boolean
}

export const Article: FC<Props> = ({ article, fullInfo }: Props) => {
    return <Paragraph>
        <Typography.Title level={3}>{article.title}</Typography.Title>
        <Paragraph><Text type="secondary">{article.year}</Text></Paragraph>
        {fullInfo && <Paragraph>{article.abstract}</Paragraph>}
    </Paragraph>
}
