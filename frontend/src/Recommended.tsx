import { Tabs } from "antd";
import { FC } from "react";

import { ArticlesRecommend } from "./ArticlesRecommended";
import { AuthorsRecommended } from "./AuthorsRecommended";

export const Recommended: FC = () => {
    return <Tabs
        defaultActiveKey="1"
        items={[
            {
                label: `Coauthors`,
                key: '1',
                children: <AuthorsRecommended />,
            },
            {
                label: `Articles`,
                key: '2',
                children: <ArticlesRecommend />,
            },
        ]}
    />
};
