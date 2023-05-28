import type {ReactElement} from "react";
import React from "react";
import styled from "@emotion/styled";
import {Helmet} from "react-helmet-async";

import {Card as MuiCard, CardContent, Divider as MuiDivider, Grid, Typography,} from "@mui/material";
import {spacing} from "@mui/system";

import DashboardLayout from "../layouts/Dashboard";

const Card = styled(MuiCard)(spacing);

const Divider = styled(MuiDivider)(spacing);

function WelcomeCard() {
    return (
        <Card mb={6}>
            <CardContent>
                <Typography variant="body2" gutterBottom>
                    Welcome to Digimans.ai Beta!
                </Typography>
            </CardContent>
        </Card>
    );
}

function Welcome() {
    return (
        <React.Fragment>
            <Helmet title="Welcome"/>
            <Typography variant="h3" gutterBottom display="inline">
                Welcome
            </Typography>

            <Divider my={6}/>

            <Grid container spacing={6}>
                <Grid item xs={12}>
                    <WelcomeCard/>
                </Grid>
            </Grid>
        </React.Fragment>
    );
}

Welcome.getLayout = function getLayout(page: ReactElement) {
    return <DashboardLayout>{page}</DashboardLayout>;
};

export default Welcome;
