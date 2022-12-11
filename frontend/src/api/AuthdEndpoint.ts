import { token } from "./token";
import { RestEndpoint, RestGenerics } from '@rest-hooks/rest';

import { PREFIX } from "./consts";

export default class AuthdEndpoint<O extends RestGenerics = any> extends RestEndpoint<O> {
    urlPrefix = PREFIX;

    getHeaders(headers: HeadersInit): HeadersInit {
        return {
            ...headers,
            'Authorization': `bearer ${token.get()}` || "",
        };
    }
}
