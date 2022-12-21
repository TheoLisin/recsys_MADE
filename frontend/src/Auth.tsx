import { useCallback, useEffect, useState } from 'react';
import { Button, Form, Input, Modal, message } from 'antd';

import { token } from './api/token';
import { fetchAuth, AuthParams } from './api/Auth';
import { useAppContext } from './state/AppContext';
import { ActionKind } from './state/types';
import { useController, useDLE } from '@rest-hooks/react';
import { ServerError } from './api/Error';


type FormFields = {
    username: string,
    password: string
};

type SubmitCallback = (formData: FormFields) => void;

type AuthFormProps = {
    onSubmit: SubmitCallback
    onSignUp: () => void
    isLoading: boolean
};

const AuthForm: React.FC<AuthFormProps> = ({ onSubmit, onSignUp, isLoading }) => {
    return (
        <Form
            name="basic"
            labelCol={{ span: 8 }}
            wrapperCol={{ span: 16 }}
            initialValues={{ remember: true }}
            onFinish={onSubmit}
            autoComplete="off"
        >
            <Form.Item
                label="Username"
                name="username"
                rules={[{ required: true, message: 'Please input your username!' }]}
            >
                <Input />
            </Form.Item>

            <Form.Item
                label="Password"
                name="password"
                rules={[{ required: true, message: 'Please input your password!' }]}
            >
                <Input.Password />
            </Form.Item>

            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                <Button type="primary" htmlType="submit" loading={isLoading} className="login-form-button">
                    Submit
                </Button>
                <br />
                Or <a onClick={onSignUp}> register now! </a>
            </Form.Item>
        </Form>
    );
};

export type AuthProps = {
    show: boolean
};

export const Auth: React.FC<AuthProps> = ({ show }: AuthProps) => {
    /* Render modal */
    return <>
        <Modal
            title="Login"
            open={show}
            footer={null}
            closable={false}
            destroyOnClose={true}
        >
            <Authentication />
        </Modal>
    </>;
}

const Authentication: React.FC = () => {
    const { isAuthFinished, isLoading, error, setCredentials } = useAuth();

    const [messageApi, contextHolder] = message.useMessage();

    const { dispatch } = useAppContext();

    const handleLogin = (formData: FormFields) => {
        setCredentials({
            username: formData.username,
            password: formData.password
        });
    }

    const signUp = () => {
        dispatch({ type: ActionKind.SignUp });
    }

    useEffect(() => {
        if (error) {
            messageApi.open({
                type: 'error',
                content: `Authentication error: ${error.detail}`,
            });
        }
    }, [error, messageApi])

    useEffect(() => {
        if (isAuthFinished) {
            dispatch({ type: ActionKind.Login });
        }
    }, [dispatch, isAuthFinished])

    return <>
        {contextHolder}
        <AuthForm
            onSubmit={handleLogin}
            onSignUp={signUp}
            isLoading={isLoading}
        />
    </>
}

/**
 * Try to login if credentials provided
 *  
 * @returns `isAuthFinished` false indicates the credentials is not set or error occurred
 * @returns `loading` auth in progress
 * @returns `error` contains error from server if auth failed
 * @returns `setCredentials` use this to provide credentials for auth
 */
function useAuth() {
    const [credentials, setCredentials] = useState<AuthParams | null>(null);
    const { data, loading, error } = useDLE(fetchAuth, credentials);
    const controller = useController()

    useEffect(() => {
        if (data) {
            token.set(data.access_token);
            controller.invalidate(fetchAuth, credentials);
        }
    },
    [data]);

    const errorMsg = error ? (error as unknown as ServerError) : undefined;
    const isAuthFinished = !!data;

    return {
        isAuthFinished,
        isLoading: loading,
        error: errorMsg,
        setCredentials
    };
}
