import type {ReactElement} from "react";
import React from "react";
import styled from "@emotion/styled";

import {Paper} from "@mui/material";

import AuthLayout from "../layouts/Auth";

import SignInComponent from "../components/auth/SignIn";

import useAuth from "../hooks/useAuth";
import {useRouter} from "next/router";

const logo = "/static/img/logo_digimans.png";

const Brand = styled.img`
  width: 18rem;
  height: 18rem;
  margin-bottom: 32px;
`;


const Wrapper = styled(Paper)`
  padding: ${(props) => props.theme.spacing(6)};

  ${(props) => props.theme.breakpoints.up("md")} {
    padding: ${(props) => props.theme.spacing(10)};
  }
`;

function SignIn() {
    const {isAuthenticated, user} = useAuth();
    const router = useRouter();
    if (isAuthenticated) {
        router.push("/models");
    }

    return (
        <React.Fragment>
            <Brand src={logo}/>
            <Wrapper>
                <SignInComponent/>
            </Wrapper>
        </React.Fragment>
    );
}

SignIn.getLayout = function getLayout(page: ReactElement) {
    return <AuthLayout>{page}</AuthLayout>;
};

export default SignIn;
