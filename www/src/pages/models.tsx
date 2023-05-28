import type {ReactElement} from "react";
import React from "react";
import styled from "@emotion/styled";
import {Helmet} from "react-helmet-async";

import {
    Breadcrumbs as MuiBreadcrumbs,
    Card as MuiCard,
    CardContent,
    Divider as MuiDivider,
    Grid,
    Link,
    Typography,
} from "@mui/material";
import {spacing} from "@mui/system";

import DashboardLayout from "../layouts/Dashboard";

const Card = styled(MuiCard)(spacing);

const Divider = styled(MuiDivider)(spacing);


function ModelCard() {
    return (
        <Card mb={6}>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Empty card
                </Typography>
                <Typography variant="body2" gutterBottom>
                    Empty card
                </Typography>
            </CardContent>
        </Card>
    );
}

function Models() {
    return (
        <React.Fragment>
                <Helmet title="Models"/>
                <Typography variant="h3" gutterBottom display="inline">
                    Models
                </Typography>

                <Divider my={6}/>

                <Grid container spacing={6}>
                    <Grid item xs={4}>
                        <ModelCard/>
                    </Grid>
                    <Grid item xs={4}>
                        <ModelCard/>
                    </Grid>
                    <Grid item xs={4}>
                        <ModelCard/>
                    </Grid>
                    <Grid item xs={4}>
                        <ModelCard/>
                    </Grid>
                    <Grid item xs={4}>
                        <ModelCard/>
                    </Grid>
                </Grid>
        </React.Fragment>
    );
}

Models.getLayout = function getLayout(page: ReactElement) {
    return <DashboardLayout>{page}</DashboardLayout>;
};

export default Models;
