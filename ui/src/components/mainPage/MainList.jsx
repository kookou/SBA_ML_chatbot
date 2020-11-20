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
import Chip from '@material-ui/core/Chip';
import { Link } from 'react-router-dom'


const useStyles = makeStyles((theme) => ({
    divroot: {
        flexGrow: 1,
        marginTop: theme.spacing(3),

    },
    root: {
        display: 'flex',
        width: 270,
        // height: 329,
    },
    details: {
        display: 'flex',
        flexDirection: 'column',
    },
    content: {
        // flex: '1 0 auto',
    },
    paper: {
        padding: theme.spacing(2),
        textAlign: 'center',
        color: theme.palette.text.secondary,
    },
    media: {
        height: 180,
    },
    textOverflow: {
        textOverflow: 'ellipsis',
    },
    marr: {
        marginRight: theme.spacing(1),
    },
    marl: {
        marginLeft: -4,
    },
    toolbarLink: {
        textDecoration: 'none',
    },
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


const MainList = (props) => {
    const classes = useStyles();
    const theme = useTheme();
    const { post } = props;

    return (

        <div className={classes.divroot}>
            <Grid container justify="flex-start"  >
                <Link to={"/shop/" + post.shop_id} className={classes.toolbarLink}>
                    <Card className={classes.root} square elevation={0} variant="outlined" >
                        <CardActionArea>
                            <CardMedia
                                className={classes.media}
                                image={'https://www.yogiyo.co.kr' + post.shop_img}
                                title={post.shop_name}
                            />
                            <CardContent >
                                <Typography gutterBottom variant="h6" component="h6" noWrap>               {/* noWrap: test overflow 적용 */}
                                    {post.shop_name}
                                </Typography>
                                <Grid container direction="row">
                                    <Rating name="iconstar" defaultValue={1} max={1} />
                                    <Typography variant="subtitle1" color="textSecondary">
                                        {post.shop_rev_avg} /
                                    </Typography>
                                    <Rating name="iconstar" defaultValue={1} max={1} />
                                    
                                    <Typography variant="subtitle1" color="textSecondary" className={classes.marr}>
                                        예상 {post.shop_pred_avg}
                                    </Typography>
                                    {post.shop_user_avg !== undefined &&
                                        <Chip color="secondary" size="small" label={'내 평점  ' + post.shop_user_avg} />
                                    }
                                </Grid>
                                
                                <Typography variant="body2" color="textSecondary" component="p">
                                    리뷰 {post.shop_rev_cnt}개
                                </Typography>

                                <Typography variant="body2" color="textSecondary" component="p" noWrap>
                                    대표메뉴 {post.food_name}
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                </Link>
            </Grid>
        </div >


    );
}

MainList.propTypes = {
    post: PropTypes.object,
};

export default MainList