import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types';
import { makeStyles } from '@material-ui/core/styles';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Typography from '@material-ui/core/Typography';
import Box from '@material-ui/core/Box';
import UserInfo from './UserInfo'
import { Grid } from '@material-ui/core';
import UserDeliveryList from './UserDeliveryList'
import Pagination from '@material-ui/lab/Pagination';
import axios from 'axios';


function TabPanel(props) {
    const { children, value, index, ...other } = props;

    return (
        <div
            role="tabpanel"
            hidden={value !== index}
            id={`vertical-tabpanel-${index}`}
            aria-labelledby={`vertical-tab-${index}`}
            {...other}
        >
            {value === index && (
                <Box p={4}>
                    <Typography>{children}</Typography>
                </Box>
            )}
        </div>
    );
}

TabPanel.propTypes = {
    children: PropTypes.node,
    index: PropTypes.any.isRequired,
    value: PropTypes.any.isRequired,
};

function a11yProps(index) {
    return {
        id: `vertical-tab-${index}`,
        'aria-controls': `vertical-tabpanel-${index}`,
    };
}

const useStyles = makeStyles((theme) => ({
    topmargin: {
        marginTop: theme.spacing(5),
        maxWidth: 800,
        // minHeight: 600,

    },
    nav: {
        flexGrow: 1,
        // backgroundColor: theme.palette.background.paper,
        display: 'flex',
        // minheight: 800,
        marginTop: theme.spacing(3),
        maxWidth: 912,

    },
    tabs: {
        borderRight: `1px solid ${theme.palette.divider}`,
        // marginTop: theme.spacing(3),
        paddingTop: 40,
    },
    pagi: {
        '& > *': {
            marginTop: theme.spacing(3),
        },
    },
    maxwidthmypage: {
        maxWidth: 800,
        paddingRight: 70,
        paddingLeft: 70,
    },
    maxwidthlist: {
        maxWidth: 800,
        paddingRight: 70,
        paddingLeft: 70,
    },
    small: {
        width: theme.spacing(3),
        height: theme.spacing(3),
    },


}));




const Usernav = () => {

    const userid = sessionStorage.getItem("sessionUser");
    const [userOderData, setuserOrderData] = useState([])
    const classes = useStyles();
    const [value, setValue] = React.useState(0);

    useEffect(() => {
        axios.get(`http://localhost:8080/mypage/${userid}`)
            .then(res => {
                setuserOrderData(res.data)
                // console.log(res.data)
            }).catch(error => {
                alert("안돼 돌아가")
            })
    }, [])


    const itemsPerPage = 10;
    const [page, setPage] = React.useState(1);
    const noOfPages = Math.ceil(userOderData.length / itemsPerPage) /*Math.ceil 소수점 이하를 올림 한다. */

    const handleChangepagi = (event, value) => {
        setPage(value);
    };

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <div className={classes.nav}>
            <Tabs
                orientation="vertical"
                variant="scrollable"
                value={value}
                onChange={handleChange}
                aria-label="Vertical tabs example"
                className={classes.tabs}
            >
                <Tab label="주문내역" {...a11yProps(0)} />
                <Tab label="정보수정" {...a11yProps(1)} />

            </Tabs>
            <TabPanel value={value} index={0} >
                <Grid container className={classes.topmargin} justify="center" >
                    <Typography component="h1" variant="h5" >
                        주문내역
                    </Typography>
                    <Grid container alignItems="flex-start" className={classes.maxwidthlist}>
                        {userOderData.slice((page - 1) * itemsPerPage, page * itemsPerPage)
                            .map((post) => (
                                <UserDeliveryList key={post.shop} post={post} />
                            ))}
                    </Grid>
                    <Grid container justify="center" alignItems="flex-end" className={classes.pagi}>
                        <Pagination
                            count={noOfPages}
                            page={page}
                            onChange={handleChangepagi}
                            defaultPage={2}
                            color="secondary"
                            showFirstButton
                            showLastButton
                            shape="rounded"
                        />
                    </Grid>
                </Grid>
            </TabPanel>
            <TabPanel value={value} index={1}>
                <Grid container className={classes.topmargin} justify="center">
                    <Typography component="h1" variant="h5" >
                        정보수정
                    </Typography>
                    <Grid container justify="center" className={classes.maxwidthmypage}>
                        <UserInfo />
                    </Grid>
                </Grid>
            </TabPanel>
        </div>
    );
}

export default Usernav