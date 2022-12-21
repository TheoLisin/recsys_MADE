import { Alert } from 'antd';
import React from 'react';


export type ErrorProps = {
    msg: string,
    status?: number,
    title?: string
}

export const Error: React.FC<ErrorProps> = (props) => {
    const description = (() => {
        if (props.status) {
            if (props.status === 500) {
                return <>
                    <b>Apparently, server offline... But we are working on it!</b>
                    <br />Error {props.status}: {props.msg}.
                </>
            }
            else {
                return <>Error {props.status}: {props.msg}</>
            }
        }
        else {
            return <>Error: {props.msg}</>
        }
    })();

    return <Alert
        message={props.title ? props.title : undefined}
        description={description}
        type="error"
        showIcon
    />
}
