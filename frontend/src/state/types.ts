import { ArticleInfo } from "../Article";
import { GraphInfo } from "../Graph";

export type Page = "TOP" | "ARTICLES" | "RECOMMENDED";

export type StateType = {
    shownArticle: ArticleInfo | undefined,
    shownGraph: GraphInfo | undefined,
    authState: "SIGN_UP" | "BEFORE_LOGIN" | "LOGGED_IN" | "LOGGED_OUT",
    showUser: boolean,
    shownAuthor: number | undefined,
    page: Page
};

export enum ActionKind {
    ShowArticle,
    CloseArticle,
    ShowUserInfo,
    CloseUserInfo,
    ShowAuthorInfo,
    CloseAuthorInfo,
    ShowGraph,
    CloseGraph,
    Login,
    Logout,
    WaitForLogin,
    SignUp,
    SetPage
};

export type Action = {
    type: ActionKind;
    payload?: ArticleInfo | Page | number | GraphInfo;
};
