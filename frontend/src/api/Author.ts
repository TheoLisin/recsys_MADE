import { createResource, Entity } from '@rest-hooks/rest';
import { ArticleSchema } from './Article';

import AuthdEndpoint from './AuthdEndpoint';

export class AuthorSchema extends Entity {
    id_user: number = 0
    old_id: string = ""
    avatar: string = ""
    sid: string = ""
    name: string = ""
    organisations: string = ""
    orcid: string = ""
    position: string = ""
    email: string = ""
    bio: string = ""
    homepage: string = ""
    id: number = 0

    pk(parent?: any, key?: string | undefined): string {
        return `${this.id}`;
    }
}

export class AuthorWithArticlesSchema extends Entity {
    readonly id_author: number = 0
    readonly author: AuthorSchema = AuthorSchema.fromJS({});
    readonly articles: ArticleSchema[] | undefined = [];

    static schema = {
        author: AuthorSchema,
        articles: [ArticleSchema]
    };

    pk(parent?: any, key?: string | undefined): string {
        return `${this.id_author}`;
    }
}

export class AuthorRecommendSchema extends Entity {
    id_author: number = 0
    name: string = ""
    n_articles: number = 0

    pk(parent?: any, key?: string | undefined): string {
        return `${this.id_author}`;
    }
}

export const AuthorWithArticlesResource = createResource({
    path: '/authors/:id',
    schema: AuthorWithArticlesSchema,
    Endpoint: AuthdEndpoint,
});

export const AuthorsRecommendResource = createResource({
    path: '/authors/recommend/:stub',  // use this only with getList
    schema: AuthorRecommendSchema,
    Endpoint: AuthdEndpoint,
});

