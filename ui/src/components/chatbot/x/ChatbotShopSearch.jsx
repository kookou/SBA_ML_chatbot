import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import MainList from '../mainPage/MainList';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Chatbot from './Chatbot';
import ChatbotShopSearchContents from './ChatbotShopSearchContents';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    wd: {
        width:"100%"
    }
}));


const shoplistl = [
    {
        shop_img: 'https://www.yogiyo.co.kr/media/restaurant_logos/베이컨포테이토골드피자02_20131128_FoodAD_crop_200x200_I47tFRa.jpg',
        shop_name: '네네치킨1',
        shop_rev_avg:
            '4.5',
        pred_rev_avg:
            '4.7',
        shop_rev_amt:
            '304',
        food_name: '뿌링치즈볼',
        shop_pred_avg: '4.7'

    },
    {
        shop_img: 'https://rev-static.yogiyo.co.kr/restaurants/thumbnail/stock_img/족발보쌈/족발/5fb02edc8f0531ede141222ae99cafcc_tn.jpg',
        shop_name: '네네치킨1',
        shop_rev_avg:
            '4.5',
        pred_rev_avg:
            '4.7',
        shop_rev_amt:
            '304',
        food_name: '뿌링치즈볼',
        shop_pred_avg: '4.7'

    },
    {
        shop_img: 'https://rev-static.yogiyo.co.kr/franchise/thumbnail/20181228144604231071_c1167f872d2823627279e43082f41e0e_tn.jpg',
        shop_name: '네네치킨1',
        shop_rev_avg:
            '4.5',
        pred_rev_avg:
            '4.7',
        shop_rev_amt:
            '304',
        food_name: '뿌링치즈볼',
        shop_pred_avg: '4.7'

    },
];




const ChatbotShopSearch = () => {
    const classes = useStyles();

    return (
        <React.Fragment>
            <CssBaseline />
            <Grid container  direction="row" justify="flex-start" className={classes.wd}>
                    {shoplistl.map((post) => (
                        <ChatbotShopSearchContents key={post.shop_name} post={post} />
                    ))}
            </Grid>        
        </React.Fragment>
    );
}


export default ChatbotShopSearch