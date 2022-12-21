import { Modal } from "antd";
import { FC, useEffect, useState } from "react";
import { Article, ArticleInfo } from "./Article";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";

export const ArticleModal: FC = () => {
    const { state, dispatch } = useAppContext();
    const [article, setArticle] = useState<ArticleInfo | undefined>(undefined)

    /** React on change of `shown_article` */
    useEffect(() => {
        setArticle(state.shownArticle);
    }, [state])

    return <>
        {<Modal
            title={null}
            open={!!article}
            footer={null}
            closable={true}
            onCancel={() => { // close button action
                dispatch({
                    type: ActionKind.CloseArticle
                });
            }}
            zIndex={1001}
        >
            {!!article && // needs to prevent type errors on article prop
                <Article article={article} fullInfo={true}></Article>}
        </Modal>}
    </>
}
