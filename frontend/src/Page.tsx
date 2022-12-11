import { Layout } from "antd";
import React from "react";
import { FC } from "react";

import { ArticleModal } from "./ActicleModal";
import { Articles } from "./Articles";
import { Auth } from "./Auth"
import { Menu } from "./Menu";
import AppContext from "./state/AppContext"
import reducer from "./state/reducer";
import { StateType } from "./state/types"
import { SignUp } from "./Signup";
import { UserModal } from "./UserModal";
import { TopAuthors } from "./TopAuthors";
import { AuthorModal } from "./AuthorModal";
import { Recommended } from "./Recommended";

const { Content, Sider } = Layout;

const initialState: StateType = {
    shownArticle: undefined,
    authState: "BEFORE_LOGIN",
    showUser: false,
    page: "ARTICLES",
    shownAuthor: undefined
}

const Page: FC = () => {
    const [state, dispatch] = React.useReducer(reducer, initialState);
    const providerState = {
        state,
        dispatch,
    };

    return <>
        <AppContext.Provider value={providerState}>
            <Auth />
            <SignUp />
            <ArticleModal />

            <AuthorModal />
            {state.authState === "LOGGED_IN" && <UserModal />}

            {state.authState === "LOGGED_IN" &&
                <Layout>
                    <Sider width={200}>
                        <Menu />
                    </Sider>
                    <Layout style={{ padding: '0 24px 24px' }}>
                        <Content
                            style={{
                                padding: 24,
                                margin: 0,
                                minHeight: 280,
                            }}
                        >
                            {state.page === "ARTICLES" && <Articles />}
                            {state.page === "TOP" && <TopAuthors />}
                            {state.page === "RECOMMENDED" && <Recommended />}
                        </Content>
                    </Layout>
                </Layout>
            }
        </AppContext.Provider>
    </>
}

export default Page;
