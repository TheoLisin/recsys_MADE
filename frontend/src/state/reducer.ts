import { ArticleSchema } from "../api/Article";
import { GraphInfo } from "../Graph";
import { Action, ActionKind, Page, StateType } from "./types";

export const reducer = (state: StateType, action: Action): StateType => {
    const { type, payload } = action;
    switch (type) {
        case ActionKind.ShowArticle:
            return {
                ...state,
                shownArticle: payload as ArticleSchema
            }
        case ActionKind.CloseArticle:
            return {
                ...state,
                shownArticle: undefined
            }
        case ActionKind.Login:
            return {
                ...state,
                authState: "LOGGED_IN"
            }

        case ActionKind.Logout:
            return {
                ...state,
                authState: "LOGGED_OUT"
            }

        case ActionKind.WaitForLogin:
            return {
                ...state,
                authState: "BEFORE_LOGIN"
            }

        case ActionKind.SignUp:
            return {
                ...state,
                authState: "SIGN_UP"
            }

        case ActionKind.ShowUserInfo:
            return {
                ...state,
                showUser: true
            }

        case ActionKind.CloseUserInfo:
            return {
                ...state,
                showUser: false
            }

        case ActionKind.SetPage:
            return {
                ...state,
                page: payload as Page
            }

        case ActionKind.ShowAuthorInfo:
            return {
                ...state,
                shownAuthor: payload as number
            }

        case ActionKind.CloseAuthorInfo:
            return {
                ...state,
                shownAuthor: undefined
            }
        case ActionKind.ShowGraph:
            return {
                ...state,
                shownGraph: payload as GraphInfo
            }
        case ActionKind.CloseGraph:
            return {
                ...state,
                shownGraph: undefined
            }

        default:
            return state;
    }
};

export default reducer;
