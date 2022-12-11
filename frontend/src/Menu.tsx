import { FC } from "react";
import { Menu as AntMenu, Divider } from "antd";
import { 
    FileTextOutlined, LogoutOutlined, UserOutlined, StarOutlined, ContactsOutlined 
} from '@ant-design/icons';

import { useAppContext } from "./state/AppContext";
import { ActionKind, Page } from "./state/types";

const menuStyle = { height: '100%', borderRight: 0, paddingTop: 10 };

export const Menu: FC = () => {
    const { dispatch, state } = useAppContext();

    const logout = () => {
        dispatch({ type: ActionKind.Logout });
    };

    const showUser = () => {
        dispatch({ type: ActionKind.ShowUserInfo });
    };

    const showPage = (page: Page) => {
        dispatch({ type: ActionKind.SetPage, payload: page });
    };

    return <AntMenu
        mode="inline"
        defaultSelectedKeys={[state.page.toLowerCase()]}
        style={menuStyle}
    >
        <AntMenu.Item key="articles" icon={<FileTextOutlined />} onClick={() => showPage("ARTICLES")}>
            <span>Articles</span>
        </AntMenu.Item>

        <AntMenu.Item key="top" icon={<StarOutlined />} onClick={() => showPage("TOP")}>
            <span>Top</span>
        </AntMenu.Item>

        <AntMenu.Item key="recommended" icon={<ContactsOutlined />} onClick={() => showPage("RECOMMENDED")}>
            <span>Recommended</span>
        </AntMenu.Item>

        <Divider dashed />

        <AntMenu.Item key="user" icon={<UserOutlined />} onClick={() => showUser()}>
            <span>User</span>
        </AntMenu.Item>

        <AntMenu.Item key="logout" icon={<LogoutOutlined />} onClick={() => logout()}>
            <span>Logout</span>
        </AntMenu.Item>
    </AntMenu>
}
