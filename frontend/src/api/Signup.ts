import { Endpoint } from '@rest-hooks/rest';

import { PREFIX } from './consts';
import { api_fetch } from '../utils/fetch';

export interface SignupResponse {
    login: string;
    pwdhash: string;
    id: number;
}

export interface Params {
    username: string;
    password: string;
}

const signupFetch = ({ username, password }: Params): Promise<SignupResponse> =>
    api_fetch(`${PREFIX}/signup`,
        {
            method: 'post',
            headers: new Headers({
                'content-type': 'application/json;charset=UTF-8',
            }),
            body: JSON.stringify({
                login: username,
                pwdhash: password,
            }),
        }
    )

export const fetchSignup = new Endpoint(signupFetch);
