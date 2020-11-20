import React from 'react';
import { Link } from 'react-router-dom'

import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { fade, makeStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles((theme) => ({
    '@global': {
        ul: {
            margin: 0,
            padding: 0,
            listStyle: 'none',
        },
    },
    root: {
        width: 1190,
        backgroundColor: fade(theme.palette.common.white, 0),
        marginBottom: theme.spacing(3),
    },
    appBar: {
        borderBottom: `1px solid ${theme.palette.divider}`,

    },
    toolbar: {
        flexWrap: 'wrap',
        width: 1200,

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
    colorback: {
        backgroundColor: theme.palette.primary,
    },
    large: {
        width: theme.spacing(9.5),
        height: theme.spacing(9.5),
        margin: theme.spacing(2),
    },
    margintop: {
        marginTop: theme.spacing(3),
        marginBottom : theme.spacing(6),
    },
    button: {
        border: "0px",
        background: fade(theme.palette.common.white, 0.0),
        justify : "center",
        alignItems : "center",
    },
    marginbottom: {
        marginBottom: theme.spacing(2)
    },
    ty:{
        align: 'center',
    }

}));


const Navigation = () => {
    const classes = useStyles();
    const [value, setValue] = React.useState(0);

    return (
        <React.Fragment>
            <CssBaseline />
            <Grid container item md={12} justify="center" className={classes.margintop}>
                <Button component={Link} to="/shops/전체보기" >
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="전체보기" src="https://images.unsplash.com/photo-1504754524776-8f4f37790ca0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            전체보기
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/프랜차이즈" >
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="프렌차이즈" src="https://img.khan.co.kr/news/2020/06/26/l_2020062701003314900262081.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            프렌차이즈
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/치킨">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="치킨" src="https://img2.quasarzone.co.kr/img/data/editor/1603/3e4a95bdfd6fc36718d2fdaf26baa43a_1457610150_9401.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            치킨
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/피자양식">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="피자/양식" src="https://cdn.dominos.co.kr/admin/upload/goods/20200311_5MGKbxlW.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            피자/양식
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/중식">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="중국집" src="https://imagescdn.gettyimagesbank.com/500/201708/jv10946106.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            중국집
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/한식">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="한식" src="https://t1.daumcdn.net/liveboard/SNUH/ae46c5665dd94ba4b124dd27365b45e3.JPG" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            한식
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/일식돈까스">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="일식/돈까스" src="https://funshop.akamaized.net/products/0000076768/vs_image800.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            일식/돈까스
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/족발보쌈">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="족발/보쌈" src="https://post-phinf.pstatic.net/MjAxOTA4MTlfMjgy/MDAxNTY2MTkzNDgyMDU5.k8dyis-tMy0GSiPkQDLveNQ8WEnpDpUg6fzAd-SAmXsg.LqfuUotXOPuObkao5cMb1Iqczzu2osIILHcjP3Vgf78g.JPEG/image_2219871881566193468342.jpg?type=w1200" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            족발/보쌈
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/야식">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="야식" src="https://recipe1.ezmember.co.kr/cache/recipe/2018/03/28/df63b2bf13484654a8267381ffa86e7a1.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            야식
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/분식">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="분식" src="https://m.donggangmaru.com/file_data/ywnh/2016/10/10/e1bd25f75242c1b493bf49a650179217.jpg" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            분식
                        </Typography>
                    </Grid>
                </Button>
                <Button component={Link} to="/shops/카페디저트">
                    <Grid direction="column" alignItems="center" justify="center">
                        <Avatar alt="카페/디저트" src="https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Ft1.daumcdn.net%2Fcfile%2Ftistory%2F992A713D5CAA224409" className={classes.large} />
                        <Typography color="textPrimary" variant="body2" align= 'center'>
                            카페/디저트
                        </Typography>
                    </Grid>
                </Button>

                {/* <BottomNavigation
                        value={value}
                        onChange={(event, newValue) => {
                            setValue(newValue);
                        }}
                        showLabels
                        className={classes.root}
                        >
                            <BottomNavigationAction label="전체보기" href="/shops"/>
                            <BottomNavigationAction label="프렌차이즈"/>
                            <BottomNavigationAction label="치킨"/>
                            <BottomNavigationAction label="피자/양식"/>
                            <BottomNavigationAction label="중국집"/>
                            <BottomNavigationAction label="한식"/>
                            <BottomNavigationAction label="일식/돈까스"/>
                            <BottomNavigationAction label="족발/보쌈"/>
                            <BottomNavigationAction label="야식"/>
                            <BottomNavigationAction label="분식"/>
                            <BottomNavigationAction label="카페/디저트"/>
                    </BottomNavigation> */}
            </Grid>
        </React.Fragment>
    );
}

export default Navigation