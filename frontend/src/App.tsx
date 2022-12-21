import React, { FC } from 'react';
import 'antd/dist/reset.css';
import { CacheProvider, LogoutManager } from '@rest-hooks/react';

import './App.css';
import Page from "./Page";
import reducer from './state/reducer';
import { ActionKind, StateType } from './state/types';
import { token } from './api/token';
import { getLocalStorageValue } from './utils/useLocalStorage';
import AppContext from './state/AppContext';


const initialState: StateType = {
    shownArticle: undefined,
    authState: token.is_valid() ? "LOGGED_IN" : "LOGGED_OUT",
    showUser: false,
    page: getLocalStorageValue('page', "ARTICLES"),
    shownAuthor: undefined,
    shownGraph: undefined
}

const logout_manager = new LogoutManager();

const managers = [
    logout_manager,
    ...CacheProvider.defaultProps.managers,
];

const App: FC = () => {
    const [state, dispatch] = React.useReducer(reducer, initialState);
    const appContextProviderState = { state, dispatch };

    /** Logout on any 401 response */
    logout_manager.handleLogout = (controller) => {
        controller.resetEntireStore();
        dispatch({ type: ActionKind.Logout });
    }

    return <CacheProvider managers={managers}>
        <React.StrictMode>
            <AppContext.Provider value={appContextProviderState}>
                <Page />
            </AppContext.Provider>
        </React.StrictMode>
    </CacheProvider>
};

export default App;
