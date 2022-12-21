import { getLocalStorageValue, removeFromLocalStorageValue, setLocalStorageValue } from "../utils/useLocalStorage";

const TOKEN_KEY = 'auth_token'

const makeToken = () => {
    return ({
        set: (token: string | undefined) => {
            setLocalStorageValue(TOKEN_KEY, token)
        },

        get: () => {
            return getLocalStorageValue(TOKEN_KEY, undefined)
        },

        is_valid: () => {
            return getLocalStorageValue(TOKEN_KEY, undefined) !== undefined
        },

        reset: () => { removeFromLocalStorageValue(TOKEN_KEY) },
    })
};

export const token = makeToken();
