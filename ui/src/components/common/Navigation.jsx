import React from 'react';
import { Link } from 'react-router-dom'

import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import { fade, makeStyles } from '@material-ui/core/styles';
import BottomNavigation from '@material-ui/core/BottomNavigation';
import BottomNavigationAction from '@material-ui/core/BottomNavigationAction';

const useStyles = makeStyles((theme) => ({
    '@global': {
        ul: {
            margin: 0,
            padding: 0,
            listStyle: 'none',
        },
    },
    root: {
        width: 1200,
        backgroundColor: fade(theme.palette.common.white, 0),
      },
    appBar: {
        borderBottom: `1px solid ${theme.palette.divider}`,
    },
    toolbar: {
        flexWrap: 'wrap',
        width:1200,
    },
    toolbarTitle: {
        flexGrow: 1,
    },
    link: {
        marginLeft: theme.spacing(1),
    },
    heroContent: {
        padding: theme.spacing(8, 0, 6),
    },
    cardHeader: {
        backgroundColor:
            theme.palette.type === 'light' ? theme.palette.grey[200] : theme.palette.main[700],
    },
    cardPricing: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'baseline',
        marginBottom: theme.spacing(2),
    },
    footer: {
        borderTop: `1px solid ${theme.palette.divider}`,
        marginTop: theme.spacing(8),
        paddingTop: theme.spacing(3),
        paddingBottom: theme.spacing(3),
        [theme.breakpoints.up('sm')]: {
            paddingTop: theme.spacing(6),
            paddingBottom: theme.spacing(6),
        },
    },
    search: {
        position: 'relative',
        borderRadius: theme.shape.borderRadius,
        backgroundColor: fade(theme.palette.common.white, 0.5),
        '&:hover': {
            backgroundColor: fade(theme.palette.common.white, 0.8),
        },
        marginRight: theme.spacing(2),
        marginLeft: 0,
        width: '100%',
        [theme.breakpoints.up('sm')]: {
            marginLeft: theme.spacing(3),
            width: 'auto',
        },
    },
    searchIcon: {
        padding: theme.spacing(0, 2),
        height: '100%',
        position: 'absolute',
        pointerEvents: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
    },
    inputRoot: {
        color: 'inherit',
    },
    inputInput: {
        padding: theme.spacing(1, 1, 1, 0),
        // vertical padding + font size from searchIcon
        paddingLeft: `calc(1em + ${theme.spacing(4)}px)`,
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: '20ch',
        },
    },
    colorback : {
        backgroundColor: theme.palette.primary,
    },

}));


const Navigation = () => {
    const classes = useStyles();
    const [value, setValue] = React.useState(0);

    return (
        <React.Fragment>
            <CssBaseline />
                <Grid container item md={12} justify="center" className={classes.appBar}>
                    <BottomNavigation
                        value={value}
                        onChange={(event, newValue) => {
                            setValue(newValue);
                        }}
                        showLabels
                        className={classes.root}
                        >   
                                <BottomNavigationAction label="전체보기" component={Link} to="/shops/전체보기" />
                                <BottomNavigationAction label="프랜차이즈" component={Link} to="/shops/프랜차이즈"/>
                                <BottomNavigationAction label="치킨"  component={Link} to="/shops/치킨"/>
                                <BottomNavigationAction label="피자/양식" component={Link} to="/shops/피자양식"/>
                                <BottomNavigationAction label="중국집" component={Link} to="/shops/중식"/>
                                <BottomNavigationAction label="한식" component={Link} to="/shops/한식"/>
                                <BottomNavigationAction label="일식/돈까스" component={Link} to="/shops/일식돈까스"/>
                                <BottomNavigationAction label="족발/보쌈"  component={Link} to="/shops/족발보쌈"/>
                                <BottomNavigationAction label="야식" component={Link} to="/shops/야식"/>
                                <BottomNavigationAction label="분식" component={Link} to="/shops/분식"/>
                                <BottomNavigationAction label="카페/디저트" component={Link} to="/shops/카페디저트"/>
                    </BottomNavigation>
                </Grid>
        </React.Fragment>
    );
}

export default Navigation