import { Entity, RestEndpoint } from '@rest-hooks/rest';

import AuthdEndpoint from './AuthdEndpoint';
import { PREFIX } from './consts';

export class TopAuthorSchema extends Entity {
    id_author: number = 0
    name: string = ""
    n_citation: number = 0

    pk(parent?: any, key?: string | undefined): string {
        return `${this.id_author}`;
    }
}

export class TopAuthorListSchema extends Entity {
    readonly tag: string = ""
    readonly data: TopAuthorSchema[] = []

    static schema = {
        data: [TopAuthorSchema],
    };

    pk(parent?: any, key?: string | undefined): string {
        return `${this.tag}`;
    }
}

const AnalyticsTopResourceBase = new RestEndpoint({
    urlPrefix: PREFIX,
    path: '/analytics/top',
    schema: TopAuthorListSchema,
    Endpoint: AuthdEndpoint,
    method: 'GET',
});

export const AnalyticsTopResource = AnalyticsTopResourceBase.extend({
    searchParams: {} as { tag_part?: string },
});

export const GRAPH_API_URL: string = `${PREFIX}/analytics/graph`;