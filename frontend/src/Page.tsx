import { Layout } from "antd";
import React, { useEffect } from "react";

import { ArticleModal } from "./ActicleModal";
import { Articles } from "./Articles";
import { Auth } from "./Auth"
import { Menu } from "./Menu";
import { useAppContext } from "./state/AppContext"
import { SignUp } from "./Signup";
import { UserModal } from "./UserModal";
import { TopAuthors } from "./TopAuthors";
import { AuthorModal } from "./AuthorModal";
import { Recommended } from "./Recommended";
import { GraphModal } from "./GraphModal";
import { token } from "./api/token";
import { useController } from "@rest-hooks/react";

const { Content, Sider } = Layout;

const Page: React.FC = () => {
    const { state } = useAppContext()
    const { resetEntireStore } = useController();


    useEffect(() => {
        if (state.authState === "LOGGED_OUT") {
            token.reset()
            resetEntireStore();
        }
    }, [state.authState, resetEntireStore]);


    return <>
        <Auth show={state.authState === "LOGGED_OUT"} />
        <SignUp show={state.authState === "SIGN_UP"} />

        <ArticleModal />
        <AuthorModal />

        {state.authState === "LOGGED_IN" &&
            <>
                <UserModal />
                <GraphModal />
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
            </>
        }
    </>
}

export default Page;
