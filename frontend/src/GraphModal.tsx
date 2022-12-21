import { Modal } from "antd";
import { FC } from "react";
import { Graph } from "./Graph";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";

export const GraphModal: FC = () => {
    const { state, dispatch } = useAppContext();

    const isGraphShown = !!state.shownGraph;

    return <>
        {<Modal
            title={null}
            destroyOnClose={true}
            open={isGraphShown}
            footer={null}
            closable={true}
            onCancel={() => { // close button action
                dispatch({
                    type: ActionKind.CloseGraph
                });
            }}
            width={800}
        >
            {!!state.shownGraph && // needs to prevent type errors on article prop
                <Graph graph={state.shownGraph}></Graph>}
        </Modal>}
    </>
}
