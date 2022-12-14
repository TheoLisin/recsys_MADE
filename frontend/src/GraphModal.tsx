import { Modal } from "antd";
import { FC, useEffect, useState } from "react";
import { Graph, GraphInfo } from "./Graph";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";

export const GraphModal: FC = () => {
    const { state, dispatch } = useAppContext();
    const [graph, setGraph] = useState<GraphInfo | undefined>(undefined)

    /** React on change of `shown_article` */
    useEffect(() => {
        setGraph(state.shownGraph);
    }, [state])

    return <>
        {<Modal
            title={null}
            destroyOnClose={true}
            open={!!graph}
            footer={null}
            closable={true}
            onCancel={() => { // close button action
                dispatch({
                    type: ActionKind.CloseGraph
                });
            }}
            width={800}
        >
            {!!graph && // needs to prevent type errors on article prop
                <Graph graph={graph}></Graph>}
        </Modal>}
    </>
}
