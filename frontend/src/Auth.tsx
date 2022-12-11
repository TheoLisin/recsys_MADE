import { useCallback, useEffect, useState } from 'react';
import { Button, Form, Input, Modal, message } from 'antd';

import { token } from './api/token';
import { fetchAuth, AuthData } from './api/Auth';
import { useLocalStorage } from './utils/useLocalStorage';
import { useAppContext } from './state/AppContext';
import { ActionKind } from './state/types';
import { useController } from '@rest-hooks/react';


type FormType = {
    username: string,
    password: string
};

type SubmitCallback = (formData: FormType) => Promise<AuthData>;

type Props = {
    onSubmit: SubmitCallback
};

const AuthForm: React.FC<Props> = (props: Props) => {
    const [messageApi, contextHolder] = message.useMessage();
    const [authToken, setToken] = useLocalStorage<string | undefined>("auth_token", undefined);
    const { dispatch, state } = useAppContext();
    const { resetEntireStore } = useController();

    const [isModalOpen, setModalOpen] = useState(false);
    const [isLoading, setLoading] = useState(false);

    const onFinish = (values: any) => {
        setLoading(true);

        props.onSubmit(values).then(({ access_token }) => {
            setToken(access_token);
            dispatch({ type: ActionKind.Login });

            setModalOpen(false);
        }).catch(
            (error) => {
                messageApi.open({
                    type: 'error',
                    content: `Authentication error: ${error.detail}`,
                });
            }
        ).finally(
            () => setLoading(false)
        );
    };

    const signUp = () => {
        dispatch({ type: ActionKind.SignUp });
        setModalOpen(false);
    }

    /** Reset token on logout */
    useEffect(() => {
        if (state.authState === "LOGGED_OUT") {
            setToken(undefined);
            dispatch({type: ActionKind.WaitForLogin})
        }
    }, [state, setToken, dispatch])

    /** On any authToken change do set/reset of auth context */
    useEffect(() => {
        if (authToken) {
            token.set(authToken)
            dispatch({ type: ActionKind.Login })
        }
        else {
            resetEntireStore();
            token.reset()
            setModalOpen(true);
        }
    }, [authToken, dispatch, resetEntireStore])

    return (
        <>
            {contextHolder}

            <Modal
                title="Login"
                open={isModalOpen}
                footer={null}
                closable={false}
            >
                <Form
                    name="basic"
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
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
                        Or <a onClick={signUp}>
                            register now!
                        </a>
                    </Form.Item>
                </Form>
            </Modal>
        </>
    );
};

export const Auth: React.FC = () => {
    const handleLogin = useCallback(
        async (formData: FormType) => {
            return fetchAuth.fetch({
                password: formData.password,
                username: formData.username
            });
        },
        [],
    );

    return <AuthForm onSubmit={handleLogin} />;
}
