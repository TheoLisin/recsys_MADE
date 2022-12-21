import { useCallback, useState } from 'react';
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


const RegistrationForm: React.FC<Props> = ({ onSubmit }: Props) => {
    const [messageApi, contextHolder] = message.useMessage();
    const { dispatch } = useAppContext();
    const [form] = Form.useForm();

    const [isLoading, setLoading] = useState(false);

    const onFinish = (form_data: FormType) => {
        setLoading(true);

        onSubmit(form_data).then(({ login }) => {
            messageApi.open({
                type: 'success',
                content: `${login} registered!`,
            });

            dispatch({ type: ActionKind.Logout });

            form.resetFields();
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

    return (
        <>
            {contextHolder}

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
        </>
    );
};

export type SignUpParam = {
    show: boolean
}

export const SignUp: React.FC<SignUpParam> = ({ show }: SignUpParam) => {
    const { dispatch } = useAppContext();

    const handleSignup = useCallback(
        async (formData: FormType) => {
            return fetchSignup.fetch({
                password: formData.password,
                username: formData.username
            });
        },
        [],
    );

    const onModalClose = () => {
        dispatch({ type: ActionKind.Logout });
    };

    return <>
        <Modal
            title="Register"
            open={show}
            footer={null}
            closable={true}
            onCancel={onModalClose}
        >
            <RegistrationForm onSubmit={handleSignup} />
        </Modal>
    </>;
}
