import { createResource, Entity } from '@rest-hooks/rest';

import AuthdEndpoint from './AuthdEndpoint';

export class ArticleSchema extends Entity {
    id: number = 0
    old_id: string = ""
    title: string = ""
    year: string = ""
    n_citatin: number = 0
    page_stat: number = 0
    page_end: number = 0
    volume: string = ""
    lang: string = ""
    issue: string = ""
    issn: string = ""
    isbn: string = ""
    doi: string = ""
    url_pdf: string = ""
    abstract: string = ""

    pk(parent?: any, key?: string | undefined) {
        return `${this.id}`;
    }
}

export class ArticleRecommendSchema extends Entity {
    id: number = 0
    title: string = ""
    year: string = ""
    abstract: string = ""
    tags: string[] = []

    pk(parent?: any, key?: string | undefined) {
        return `${this.id}`;
    }
}


export const ArticleResource = createResource({
    path: '/articles/:id',
    schema: ArticleSchema,
    Endpoint: AuthdEndpoint,
});

export const ArticleSearchResource = createResource({
    path: '/articles/search/:stub',
    schema: ArticleSchema,
    Endpoint: AuthdEndpoint,
});

export const ArticleRecommendResource = createResource({
    path: '/articles/recommend/:stub',
    schema: ArticleRecommendSchema,
    Endpoint: AuthdEndpoint,
});
