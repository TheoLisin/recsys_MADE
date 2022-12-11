import { Endpoint } from '@rest-hooks/rest';

import { PREFIX } from './consts';
import { api_fetch } from '../utils/fetch';

export interface AuthData {
    access_token: string;
    token_type: string;
}

export interface Params {
    username: string;
    password: string;
}

const authFetch = ({ username, password }: Params): Promise<AuthData> =>
    api_fetch(`${PREFIX}/api/auth/login`,
        {
            method: 'post',
            headers: new Headers({
                'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }),
            body: `password=${password}&username=${username}`
        }
    )

export const fetchAuth = new Endpoint(authFetch);
