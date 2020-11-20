import React, { useEffect, useState } from 'react'
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios'

import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Pagination from "@material-ui/lab/Pagination";
import Typography from '@material-ui/core/Typography';

import Navigation from '../common/Navigation';
import ShopList from './ShopList';

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    wd: {
        width: 1050,
        margin: "auto"
    },
    spacing: {
        marginRight: theme.spacing(3),
    },
    pagi: {
        marginTop: theme.spacing(5)
    },
    top:{
        marginTop : theme.spacing(8),
        marginBottom : theme.spacing(3),
    }
}));


const ShopMain = ({ match }) => {

    const classes = useStyles();
    const [searchData, setSearchData] = useState([]);
    const post = searchData;
    const key = match.params.key;

    useEffect(() => {
        axios.get(`http://localhost:8080/search/${match.params.key}`)
            .then(res => {
                setSearchData(res.data)
                // alert(res.data)
                console.log(res.data)
            })
            .catch(err => {
                alert("안돼 돌아가")
            })

    }, [key])

    console.log(searchData)

    const itemsPerPage = 10;
    const [page, setPage] = React.useState(1);
    const noOfPages = Math.ceil(post.length / itemsPerPage) /*Math.ceil 소수점 이하를 올림 한다. */

    const handleChange = (event, value) => {
        setPage(value);
    };


    return (
        <React.Fragment>
            <CssBaseline />
            <Navigation />
            <Grid>
                <Typography align='center' variant="h5" className={classes.top}>
                    "{key}" 에 대한 검색 결과 "{post.length}"건
                </Typography>
            </Grid>
            <Grid container className={classes.wd} >
                {post.slice((page - 1) * itemsPerPage, page * itemsPerPage)
                    .map((post) => (
                        <Grid className={classes.spacing}>
                            <ShopList post={post} />
                        </Grid>
                ))}
            </Grid>
            <Grid container justify="center" alignItems="flex-end" className={classes.pagi}>
                <Pagination
                    count={noOfPages}
                    page={page}
                    onChange={handleChange}
                    defaultPage={2}
                    color="primary"
                    showFirstButton
                    showLastButton
                    shape="rounded"
                />
            </Grid>
        </React.Fragment>
    );
}


export default ShopMain