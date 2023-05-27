import type {ReactElement} from "react";
import React from "react";
import styled from "@emotion/styled";
import NextLink from "next/link";
import {Helmet} from "react-helmet-async";
import AuthGuard from "../components/guards/AuthGuard";

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

const Breadcrumbs = styled(MuiBreadcrumbs)(spacing);

function EmptyCard() {
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

function Blank() {
    return (
        <React.Fragment>
            <AuthGuard>
                <Helmet title="Blank"/>
                <Typography variant="h3" gutterBottom display="inline">
                    Blank
                </Typography>

                <Breadcrumbs aria-label="Breadcrumb" mt={2}>
                    <Link component={NextLink} href="/">
                        Dashboard
                    </Link>
                    <Link component={NextLink} href="/">
                        Pages
                    </Link>
                    <Typography>Blank</Typography>
                </Breadcrumbs>

                <Divider my={6}/>

                <Grid container spacing={6}>
                    <Grid item xs={12}>
                        <EmptyCard/>
                    </Grid>
                </Grid>
            </AuthGuard>
        </React.Fragment>
    );
}

Blank.getLayout = function getLayout(page: ReactElement) {
    return <DashboardLayout>{page}</DashboardLayout>;
};

export default Blank;
