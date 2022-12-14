import { FC, useState } from "react";
import { Spin, Typography } from 'antd';
import { CodeSandboxOutlined } from '@ant-design/icons';

import { GRAPH_API_URL } from "./api/Analytics";


const { Paragraph } = Typography;

export interface GraphInfo {
    id_author: number
}

type Props = {
    graph: GraphInfo
}

const iframeStyle = {
    width: '1px',
    minWidth: '100%',
    minHeight: 500,
    overflow: "hidden",
    border: 0
};

export const Graph: FC<Props> = ({ graph }: Props) => {
    const [isLoading, setGraphLoading] = useState(true);
    return <Paragraph>
        <Typography.Title level={3}> Coauthors graph </Typography.Title>

        {isLoading &&
            <Spin tip="Loading..." style={{marginTop: 30}}  indicator={<CodeSandboxOutlined size={28} spin />}>
                <div style={{ width: "100%" }}></div>
            </Spin>}

        <iframe
            title={`graph_${graph.id_author}`}
            style={iframeStyle} src={`${GRAPH_API_URL}/${graph.id_author}`}
            onLoad={() => { setGraphLoading(false) }}
        >
        </iframe>
    </Paragraph >
}



