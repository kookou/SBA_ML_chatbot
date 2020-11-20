import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Rating from '@material-ui/lab/Rating';
import Divider from '@material-ui/core/Divider';



const useStyles = makeStyles((theme) => ({
    divroot: {
        flexGrow: 1,
        marginBottom: theme.spacing(2),
        width: "100%",
    },
    root: {
        // display: 'flex',
        width: 290,
    },
    details: {
        display: 'flex',
        flexDirection: 'column',
    },
    cover: {
        width: 150,
        height: 150,
    },
    paper: {
        // padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
    media: {
        height: 140,
    },
    mrr: {
        marginRight: theme.spacing(1)
    },
    mrb: {
        marginTop: theme.spacing(2),
    },
    rating: {
        marginTop: 2,
    }
}));


function HalfRating() {
    const classes = useStyles();
    const [value, setValue] = React.useState(4);
    return (
        <div className={classes.root}>
            <Rating name="read-only" value={value} readOnly />
        </div>
    );
}

const ChatbotOrderContents = (props) => {
    console.log("뭐올거니" + JSON.stringify(props))
    // console.log("아악"+props)
    const classes = useStyles();
    const theme = useTheme();
    const post = props.order[0][0][0];
    // console.log("post "+props.menu[0].food_img)
    const userid = sessionStorage.getItem("sessionUser");
    return (

        <div className={classes.divroot}>
            <Grid container justify="flex-start" >
                <Grid>
                    <Card className={classes.root} square elevation={0} variant="outlined" >
                        <CardActionArea >
                            <CardContent>
                                <Typography variant="h6" className={classes.title}>
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

                            </CardContent>
                        </CardActionArea>
                    </Card>
            
                </Grid>

            </Grid>
        </div >


    );
}

ChatbotOrderContents.propTypes = {
    post: PropTypes.object,
};

export default ChatbotOrderContents