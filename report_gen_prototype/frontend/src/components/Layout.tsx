import NavBar from "./NavBar";
import { ReactNode } from "react";

interface Props {
    children?: ReactNode
}

export default function Layout({ children, ...props }: Props) {
    return (
        <div{...props}>
            <NavBar />
            {children}
        </div>
    )
}