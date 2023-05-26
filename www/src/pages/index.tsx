import React from "react";
import type { ReactElement } from "react";
import styled from "@emotion/styled";
import { Helmet } from "react-helmet-async";

import { Avatar, Paper, Typography } from "@mui/material";

import AuthLayout from "../layouts/Auth";

import SignInComponent from "../components/auth/SignIn";

import Logo from "../vendor/logo.svg";

const Brand = styled(Logo)`
  fill: ${(props) => props.theme.palette.primary.main};
  width: 64px;
  height: 64px;
  margin-bottom: 32px;
`;

const Wrapper = styled(Paper)`
  padding: ${(props) => props.theme.spacing(6)};

  ${(props) => props.theme.breakpoints.up("md")} {
    padding: ${(props) => props.theme.spacing(10)};
  }
`;

function SignIn() {
    return (
        <React.Fragment>
            <Brand />
            <Wrapper>
                <SignInComponent />
            </Wrapper>
        </React.Fragment>
    );
}

SignIn.getLayout = function getLayout(page: ReactElement) {
    return <AuthLayout>{page}</AuthLayout>;
};

export default SignIn;
