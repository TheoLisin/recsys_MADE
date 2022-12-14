import { createResource, Entity } from '@rest-hooks/rest';
import { ArticleSchema } from './Article';

import AuthdEndpoint from './AuthdEndpoint';
import { AuthorSchema } from './Author';

export class UserInfoSchema extends Entity {
    login: string = ""
    pwdhash: string = ""
    id: number = 0

    pk(parent?: any, key?: string | undefined): string {
        return `${this.id}`;
    }
}

export class UserSchema extends Entity {
    readonly user: UserInfoSchema = UserInfoSchema.fromJS({});
    readonly author: AuthorSchema | undefined = AuthorSchema.fromJS({});
    readonly articles: ArticleSchema[] | undefined = [];

    static schema = {
        user: UserInfoSchema,
        author: AuthorSchema,
        articles: [ArticleSchema]
    };

    pk(parent?: any, key?: string | undefined): string {
        return `${this.user.login}`;
    }
}

export const UserResource = createResource({
    path: '/me',
    schema: UserSchema,
    Endpoint: AuthdEndpoint,
});
