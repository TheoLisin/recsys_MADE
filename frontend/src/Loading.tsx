import { FC } from "react";
import { LoadingOutlined } from '@ant-design/icons';
import { Alert, Spin } from "antd";

const LOADING_ICON = <LoadingOutlined style={{ fontSize: 24 }} spin />;

export const Loading: FC = () => {
    return <Spin indicator={LOADING_ICON}>
        <Alert
            message="Data loading..."
            type="info"
        />
    </Spin>;
}
