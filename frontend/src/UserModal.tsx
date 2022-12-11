import { useDLE } from "@rest-hooks/react";
import { Modal } from "antd";
import { FC, useCallback, useEffect, useState } from "react";

import { UserResource } from "./api/User";
import { Loading } from "./Loading";
import { useAppContext } from "./state/AppContext";
import { ActionKind } from "./state/types";
import { User } from "./User";

type BaseProps = {
    showUser: boolean
    onClose: () => void
}

const UserModalBase: FC<BaseProps> = ({ showUser, onClose }: BaseProps) => {
    const { data, loading, error } = useDLE(UserResource.get);

    const user = useCallback(
        () => {
            if (error) {
                return <div>
                    <>Failed to get user info. Error {error.status}</>
                </div>;
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

export const UserModal: FC = () => {
    const [showed, setShowed] = useState(false);
    const { state, dispatch } = useAppContext();

    const onClose = useCallback(() => {
        dispatch({ type: ActionKind.CloseUserInfo })
    }, [dispatch])

    useEffect(() => {
        setShowed(state.showUser);
    }, [state])

    return <UserModalBase
        showUser={showed}
        onClose={onClose}
    />
}
