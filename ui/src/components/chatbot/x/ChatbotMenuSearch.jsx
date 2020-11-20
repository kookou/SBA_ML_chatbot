import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import ChatbotMenuSearchContents from '../ChatbotMenuSearchContents';


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
        shop_name: '맛자랑24시찜닭닭도리',
        food_name: '닭볶음탕',
        price:'20000',
        food_img:'https://images.deliveryhero.io/image/yogiyo/STOCK_IMG/%ED%95%9C%EC%8B%9D/%EA%B5%AD%EB%AC%BC%EC%9A%94%EB%A6%AC-%EC%B0%8C%EA%B0%9Cn%ED%83%95%EB%A5%98/%EC%8A%A4%ED%83%81_20170912_foodon_fon12432_%EB%8B%AD%EB%8F%84%EB%A6%AC%ED%83%9503_1080x640.jpg?width=384&height=273&quality=100',
        shop_rev_avg:
            '4.5',
        pred_rev_avg:
            '4.7',
        shop_rev_amt:
            '304',
        shop_pred_avg: '4.7'

    },
    {
        shop_name: '네네치킨1',
        food_name: '치즈왕돈까스',
        price:'20000',
        food_img:'https://rev-static.yogiyo.co.kr/franchise/thumbnail/20181228144604231071_c1167f872d2823627279e43082f41e0e_tn.jpg',
        shop_rev_avg:
            '4.5',
        pred_rev_avg:
            '4.7',
        shop_rev_amt:
            '304',
        shop_pred_avg: '4.7'

    },
    {
        shop_name: '미래향',
        food_name: '해물짬뽕탕',
        price:'20000',
        food_img:'https://rev-static.yogiyo.co.kr/restaurants/thumbnail/stock_img/족발보쌈/족발/5fb02edc8f0531ede141222ae99cafcc_tn.jpg',
        shop_rev_avg:
            '4.5',
        pred_rev_avg:
            '4.7',
        shop_rev_amt:
            '304',
        shop_pred_avg: '4.7'

    },
];




const ChatbotMenuSearch = (props) => {
    const {post} = props;
    const classes = useStyles();


    return (
        <React.Fragment>
            <CssBaseline />
            <Grid container  direction="row" justify="flex-start" className={classes.wd}>
                {shoplistl.map((post) => (
                    <ChatbotMenuSearchContents key={post.shop_name} post={post} />
                ))}
            </Grid>        
        </React.Fragment>
    );
}


export default ChatbotMenuSearch