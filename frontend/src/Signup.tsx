import { useCallback, useEffect, useState } from 'react';
import { Button, Form, Input, Modal, message } from 'antd';

import { useAppContext } from './state/AppContext';
import { ActionKind } from './state/types';
import { fetchSignup, SignupResponse } from './api/Signup';
import { Rule } from 'antd/es/form';
import { ServerError } from './api/Error';


type FormType = {
    username: string,
    password: string
};

type SubmitCallback = (formData: FormType) => Promise<SignupResponse>;

type Props = {
    onSubmit: SubmitCallback
};

/**
 * Check if input field equal to content of password field
 * @see antd Rule and Form.Item
 */
const samePasswordRule: Rule =
    ({ getFieldValue }) => ({
        validator(_, value) {
            if (!value || getFieldValue('password') === value) {
                return Promise.resolve();
            }
            return Promise.reject(
                new Error('The two passwords that you entered do not match!')
            );
        },
    });

/**
 * Open registration form in modal
 * 
 * Modal will be opened of `state.authState` has "SIGN_UP" value.
 * It closes on the successful registration or by the close button.
 * Always dispatch Logout action on close.
 * 
 * @param props takes onSumbit handler
 */
const RegistrationForm: React.FC<Props> = ({ onSubmit }: Props) => {
    const [messageApi, contextHolder] = message.useMessage();
    const { dispatch, state } = useAppContext();
    const [form] = Form.useForm();

    const [isModalOpen, setModalOpen] = useState(false);
    const [isLoading, setLoading] = useState(false);

    const onModalClose = () => {
        form.resetFields();
        setModalOpen(false);
        dispatch({ type: ActionKind.Logout });
    }

    const onFinish = (form_data: FormType) => {
        setLoading(true);

        onSubmit(form_data).then(({ login }) => {
            messageApi.open({
                type: 'success',
                content: `${login} registered!`,
            });

            onModalClose();
        }).catch(
            (error: ServerError) => {
                messageApi.open({
                    type: 'error',
                    content: `Registration error: ${error.detail}`,
                });
            }
        ).finally(
            () => setLoading(false)
        );
    };

    /** Show modal on logout */
    useEffect(() => {
        if (state.authState === "SIGN_UP") {
            setModalOpen(true);
        }
    }, [state])

    return (
        <>
            {contextHolder}

            <Modal
                title="Register"
                open={isModalOpen}
                footer={null}
                closable={true}
                onCancel={onModalClose}
            >
                <Form
                    name="basic"
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    initialValues={{ remember: true }}
                    onFinish={onFinish}
                    autoComplete="off"
                    form={form}
                >
                    <Form.Item
                        label="Username"
                        name="username"
                        rules={[{
                            required: true,
                            message: 'Please input your username!'
                        }]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        label="Password"
                        rules={[{
                            required: true,
                            message: 'Please input your password!',
                        }]}
                        hasFeedback
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item
                        name="confirm"
                        label="Confirm Password"
                        dependencies={['password']}
                        hasFeedback
                        rules={[
                            {
                                required: true,
                                message: 'Please confirm your password!',
                            },
                            samePasswordRule,
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                        <Button type="primary" htmlType="submit" loading={isLoading}>
                            Register
                        </Button>
                    </Form.Item>
                </Form>
            </Modal>
        </>
    );
};

export const SignUp: React.FC = () => {
    const handleSignup = useCallback(
        async (formData: FormType) => {
            return fetchSignup.fetch({
                password: formData.password,
                username: formData.username
            });
        },
        [],
    );

    return <RegistrationForm onSubmit={handleSignup} />;
}
