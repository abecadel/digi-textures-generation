import {SidebarItemsType} from "../../types/sidebar";

import {Home, Sliders, Box} from "react-feather";

const pagesSection = [
    {
        href: "/welcome",
        icon: Home,
        title: "Welcome",
    },
    {
        href: "/models/list",
        icon: Box,
        title: "Models",
    },
] as SidebarItemsType[];

const navItems = [
    {
        title: "Pages",
        pages: pagesSection,
    }
];

export default navItems;
