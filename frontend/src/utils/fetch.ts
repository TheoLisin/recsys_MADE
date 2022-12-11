import { ServerError } from "../api/Error"

/**
 * Same as fetch, but returns response.json()
 * 
 * @param input same as `fetch`
 * @param init same as `fetch`
 * @returns returns response.json() if no error otherwise Promise of ServerError
 */
export function api_fetch(input: RequestInfo | URL, init?: RequestInit | undefined): Promise<any> {
    return fetch(input, init)
        .then(async res => {
            if (res.ok) {
                return res.json();
            }

            const error: ServerError = await res.json();
            return await Promise.reject(error);
        })
        .catch((error: ServerError | { message: string }) => {
            if (error instanceof Error) {
                return Promise.reject({ detail: error.message });
            }
            else {
                return Promise.reject(error);
            }
        })
}
