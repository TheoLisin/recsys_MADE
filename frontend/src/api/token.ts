const makeToken = () => {
    let _value: string | undefined = undefined;

    return ({
        set: (token: string | undefined) => { _value = token },
        get: () => _value,
        is_valid: () => _value !== undefined,
        reset: () => { _value = undefined; },
    })
};

export const token = makeToken();
