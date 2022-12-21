import { useDLE } from "@rest-hooks/react";
import { Modal } from "antd";
import { FC, useCallback, useEffect, useState } from "react";
import { AuthorWithArticlesResource } from "./api/Author";
import { Error } from "./Error";
import { Loading } from "./Loading";

import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";
import { User } from "./User";

type BaseProps = {
    showUser: boolean
    id: number,
    onClose: () => void
}

const UserModalBase: FC<BaseProps> = ({ showUser, id, onClose }: BaseProps) => {
    const { data, loading, error } = useDLE(
        AuthorWithArticlesResource.get, { id: id }
    );

    const user = useCallback(
        () => {
            if (error) {
                return <Error
                    title={"Failed to get author info"}
                    msg={error.message}
                    status={error.status as number}
                />
            }
            else if (loading || !data) {
                return <Loading />
            }
            else {
                return <User {...data} />
            }
        }, [data, error, loading]);

    return <>
        <Modal
            title={null}
            open={showUser}
            footer={null}
            closable={true}
            onCancel={onClose} // close button action
            width={800}
        >
            {user()}
        </Modal>
    </>
}

export const AuthorModal: FC = () => {
    const { state, dispatch } = useAppContext();
    const [authorId, setAuthorId] = useState<number | undefined>(undefined)

    const onClose = useCallback(() => {
        dispatch({ type: ActionKind.CloseAuthorInfo })
    }, [dispatch])

    useEffect(() => {
        setAuthorId(state.shownAuthor);
    }, [state])

    return <> {
        authorId !== undefined && <UserModalBase
            showUser={!!authorId}
            id={authorId}
            onClose={onClose}
        />}
    </>
}
