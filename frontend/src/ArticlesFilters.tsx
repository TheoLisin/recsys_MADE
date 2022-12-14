import { Button, Col, Collapse, Form, Input, Row, Select } from "antd";
import { FC } from "react";

import { YEARS } from "./api/consts";
import { Filters } from "./Articles";


type SearchProps = {
    onApply: (filters: Filters) => void
}

const { Panel } = Collapse;

export const ArticlesFilters: FC<SearchProps> = ({ onApply }) => {
    const [form] = Form.useForm();

    const onFromSubmit = (values: any) => {
        // Remove undefined and empty fields
        Object.keys(values).forEach(key => {
            if (values[key] === undefined || values[key] === "") {
                delete values[key];
            }
        });

        onApply(values);
    }

    const onReset = () => {
        onApply({});
    }

    return <Collapse>
        <Panel header="Filters" key="1">
            <Form
                name="advanced_search"
                onFinish={onFromSubmit}
                form={form}
            >
                <Row gutter={32}>
                    <Col span={6}>
                        <Form.Item name={"year"} label={"Year"}>
                            <Select
                                defaultValue={""}
                                options={YEARS}
                            />
                        </Form.Item>
                    </Col>
                    <Col span={7}>
                        <Form.Item
                            name={"author_name"}
                            label={"Author name"}
                        >
                            <Input placeholder="Author name" />
                        </Form.Item>
                    </Col>
                    <Col span={7}>
                        <Form.Item
                            name={"journal_name"}
                            label={"Journal name"}
                        >
                            <Input placeholder="Journal name" />
                        </Form.Item>
                    </Col>
                    <Col span={4}>
                        <Form.Item name={"tag"} label={"Tag"}>
                            <Input placeholder="Tag" />
                        </Form.Item>
                    </Col>
                </Row>
                <Row>
                    <Col span={2} style={{ textAlign: 'right' }}>
                        <Button type="primary" htmlType="submit">
                            Apply
                        </Button>
                    </Col>
                    <Col span={2} style={{ textAlign: 'right' }}>
                        <Button type="ghost" htmlType="reset" onClick={onReset}>
                            Reset
                        </Button>
                    </Col>
                </Row>
            </Form>
        </Panel>
    </Collapse>
}
