import type {ReactNode} from "react";
import React from "react";
import type {NextPage} from "next";
import type {AppProps} from "next/app";
import {Provider} from "react-redux";
import {Helmet, HelmetProvider} from "react-helmet-async";
import {CacheProvider, EmotionCache} from "@emotion/react";

import {ThemeProvider as MuiThemeProvider} from "@mui/material/styles";
import {AdapterDateFns} from "@mui/x-date-pickers/AdapterDateFns";
import {LocalizationProvider} from "@mui/x-date-pickers/LocalizationProvider";

import "chart.js/auto";

import "../vendor/perfect-scrollbar.css";

import "../i18n";
import createTheme from "../theme";

import {ThemeProvider} from "../contexts/ThemeContext";
import useTheme from "../hooks/useTheme";
import {store} from "../redux/store";
import createEmotionCache from "../utils/createEmotionCache";

import {AuthProvider} from "../contexts/Auth0Context";

const clientSideEmotionCache = createEmotionCache();

type GetLayout = (page: ReactNode) => ReactNode;

type Page<P = {}, IP = P> = NextPage<P, IP> & {
    getLayout?: GetLayout;
};

type MyAppProps<P = {}> = AppProps<P> & {
    emotionCache?: EmotionCache;
    Component: Page<P>;
};

function App({
                 Component,
                 emotionCache = clientSideEmotionCache,
                 pageProps,
             }: MyAppProps) {
    const {theme} = useTheme();

    const getLayout = Component.getLayout ?? ((page: ReactNode) => page);

    return (
        <AuthProvider>
            <CacheProvider value={emotionCache}>
                <HelmetProvider>
                    <Helmet
                        titleTemplate="%s | Mira"
                        defaultTitle="Mira - React Material Admin Dashboard"
                    />
                    <Provider store={store}>
                        {/* @ts-ignore */}
                        <LocalizationProvider dateAdapter={AdapterDateFns}>
                            <MuiThemeProvider theme={createTheme(theme)}>
                                {getLayout(<Component {...pageProps} />)}
                            </MuiThemeProvider>
                        </LocalizationProvider>
                    </Provider>
                </HelmetProvider>
            </CacheProvider>
        </AuthProvider>
    );
}

const withThemeProvider = (Component: any) => {
    const AppWithThemeProvider = (props: JSX.IntrinsicAttributes) => {
        return (
            <ThemeProvider>
                <Component {...props} />
            </ThemeProvider>
        );
    };
    AppWithThemeProvider.displayName = "AppWithThemeProvider";
    return AppWithThemeProvider;
};

export default withThemeProvider(App);
