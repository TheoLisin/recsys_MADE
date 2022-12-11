import React, { Dispatch } from 'react';
import { StateType, Action } from './types'

interface IContextProps {
    state: StateType;
    dispatch: Dispatch<Action>
}

const AppContext = React.createContext({} as IContextProps);

export function useAppContext() {
    return React.useContext(AppContext);
}

export default AppContext;
