import type {ReactElement} from "react";
import React from "react";
import styled from "@emotion/styled";
import {Helmet} from "react-helmet-async";

import DashboardLayout from "../layouts/Dashboard";

import {DollarSign, ShoppingBag, Box as BoxIcon, Zap} from "react-feather";

import {
    Avatar as MuiAvatar,
    Box,
    Breadcrumbs as MuiBreadcrumbs,
    Button as MuiButton,
    Card as MuiCard,
    CardContent,
    Chip as MuiChip,
    Divider as MuiDivider,
    Grid as MuiGrid,
    LinearProgress as MuiLinearProgress,
    Typography as MuiTypography,
} from "@mui/material";
import {spacing, SpacingProps} from "@mui/system";
import useAuth from "../hooks/useAuth";

const Button = styled(MuiButton)(spacing);

const Card = styled(MuiCard)(spacing);

const Divider = styled(MuiDivider)(spacing);

const Grid = styled(MuiGrid)(spacing);

const LinearProgress = styled(MuiLinearProgress)(spacing);

const Spacer = styled.div(spacing);

interface TypographyProps extends SpacingProps {
    component?: string;
}

const Typography = styled(MuiTypography)<TypographyProps>(spacing);

const Centered = styled.div`
  text-align: center;
`;

const Avatar = styled(MuiAvatar)`
  display: inline-block;
  height: 128px;
  width: 128px;
`;

const StatsIcon = styled.div`
  position: absolute;
  right: 16px;
  top: 32px;

  svg {
    width: 32px;
    height: 32px;
    color: ${(props) => props.theme.palette.secondary.main};
  }
`;

function Details() {
    const { user } = useAuth();
    return (
        <Card mb={6}>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Profile Details
                </Typography>

                <Spacer mb={4}/>

                <Centered>
                    <Avatar alt="Lucy Lavender" src={user?.picture}/>
                    <Typography variant="body2" component="div" gutterBottom>
                        <Box fontWeight="fontWeightMedium">{user?.name}</Box>
                    </Typography>

                    <Button mr={2} variant="contained" color="primary" size="small">
                        Follow
                    </Button>
                    <Button mr={2} variant="contained" color="primary" size="small">
                        Message
                    </Button>
                </Centered>
            </CardContent>
        </Card>
    );
}

function Subscription() {
    return (
        <Card mb={6}>
            <CardContent>
                <Typography variant="h6" gutterBottom>
                    Subscription
                </Typography>

                <Spacer mb={4}/>

                <Typography variant="h3" gutterBottom>
                    Creator
                </Typography>

            </CardContent>
        </Card>
    );
}

function LimitsModels() {
    return (
        <Box position="relative">
            <Card mb={6} pt={2}>
                <CardContent>
                    <Typography variant="h2" gutterBottom>
                        <Box fontWeight="fontWeightRegular">2/100</Box>
                    </Typography>
                    <Typography variant="body2" gutterBottom mt={3} mb={0}>
                        Total Number of Models
                    </Typography>

                    <StatsIcon>
                        <BoxIcon/>
                    </StatsIcon>
                    <LinearProgress
                        variant="determinate"
                        value={2}
                        color="secondary"
                        mt={4}
                    />
                </CardContent>
            </Card>
        </Box>
    );
}

function LimitsGenerations() {
    return (
        <Box position="relative">
            <Card mb={6} pt={2}>
                <CardContent>
                    <Typography variant="h2" gutterBottom>
                        <Box fontWeight="fontWeightRegular">30/100</Box>
                    </Typography>
                    <Typography variant="body2" gutterBottom mt={3} mb={0}>
                        Genertions this month
                    </Typography>

                    <StatsIcon>
                        <Zap/>
                    </StatsIcon>
                    <LinearProgress
                        variant="determinate"
                        value={30}
                        color="secondary"
                        mt={4}
                    />
                </CardContent>
            </Card>
        </Box>
    );
}

function TotalSomething() {
    return (
        <Box position="relative">
            <Card mb={6} pt={2}>
                <CardContent>
                    <Typography variant="h2" gutterBottom>
                        <Box fontWeight="fontWeightRegular">$ 1.224</Box>
                    </Typography>
                    <Typography variant="body2" gutterBottom mt={3} mb={0}>
                        Total Revenue
                    </Typography>

                    <StatsIcon>
                        <DollarSign/>
                    </StatsIcon>
                    <LinearProgress
                        variant="determinate"
                        value={50}
                        color="secondary"
                        mt={4}
                    />
                </CardContent>
            </Card>
        </Box>
    );
}


function Profile() {
    return (
        <React.Fragment>
            <Helmet title="Profile"/>

            <Typography variant="h3" gutterBottom display="inline">
                Profile
            </Typography>

            <Divider my={6}/>

            <Grid container spacing={6}>
                <Grid item xs={12} lg={4} xl={3}>
                    <Details/>
                </Grid>
                <Grid item xs={12} lg={8} xl={9}>
                    <Grid container spacing={6}>
                        <Grid item xs={12} lg={12}>
                            <Subscription/>
                        </Grid>
                    </Grid>
                    <Grid container spacing={6}>
                        <Grid item xs={12} lg={6}>
                            <LimitsModels/>
                        </Grid>
                        <Grid item xs={12} lg={6}>
                            <LimitsGenerations/>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </React.Fragment>
    );
}

Profile.getLayout = function getLayout(page: ReactElement) {
    return <DashboardLayout>{page}</DashboardLayout>;
};

export default Profile;
