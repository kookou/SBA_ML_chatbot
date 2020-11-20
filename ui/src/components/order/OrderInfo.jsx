import React from 'react';
import PropTypes from 'prop-types';

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Button from '@material-ui/core/Button';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    wd: {
        width: 1050,
        margin: "auto",
        marginTop: theme.spacing(3),
        marginBottom: theme.spacing(6)
    },
    title: {
        marginBottom: theme.spacing(3),
        marginTop: theme.spacing(4),
    },
    subtitle:{
        marginBottom: theme.spacing(3),
        marginTop: theme.spacing(4),

    }
}));

const OrderInfo = (props) => {
    const classes = useStyles();
    const {post} = props;
    console.log(post)

    return (
        <div className={classes.root} >
            <Grid item md={12} justify="center" align="center">
                <Typography variant="h5" className={classes.title}>
                    {sessionStorage.getItem("sessionUser")} 님의 주문이 완료 되었습니다.
                </Typography>
                <Divider variant="inset" variant="middle" />
                <Typography variant="h6" className={classes.subtitle}>
                    주문정보
                </Typography>
                <Typography variant="subtitle1">
                    주문 번호 : {post.or_id}
                </Typography>
                <Typography variant="subtitle1">
                    배달 주소 : {post.addr}
                </Typography>
                <Typography variant="subtitle1">
                    메뉴 : {post.food_name}
                </Typography>
                <Typography variant="subtitle1">
                    가격 : {post.price}원
                </Typography>

                <Typography variant="subtitle1" className={classes.subtitle}>
                주문하신 음식은 약 40분 뒤에 배달이 될 예정입니다.
                </Typography>
                <Button variant="contained" color="primary" disableElevation href="/mypage">
                    주문내역
                </Button>
            </Grid>
        </div>


    );
}


export default OrderInfo