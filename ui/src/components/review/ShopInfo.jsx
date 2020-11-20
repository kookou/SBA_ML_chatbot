import React from 'react';
import PropTypes from 'prop-types';

import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Hidden from '@material-ui/core/Hidden';
import Rating from '@material-ui/lab/Rating';


const useStyles = makeStyles({
  card: {
    display: 'flex',
  },
  cardDetails: {
    flex: 1,
  },
  cardMedia: {
    width: 250 ,
    height: 250,
    marginRight :40,
  },
  shopMain : {
    marginTop : 50,
    marginBottom : 30,
  },
  root: {
    display: 'flex',
    flexDirection: 'column',
    '& > * + *': {
    },
  },
  background:{
    backgroundColor : '#ffffff',
  },
  marginbottom:{
    marginBottom : 10,
  },
  rating:{
    marginLeft : -5,
    // marginbottom : 5,
  },
});




const ShopInfo = (props) => {
  const classes = useStyles();
  const { post } = props;
  // console.log("gl"+post.open_time)
  // console.log("===========test========"+post)

  function HalfRating() {
    const classes = useStyles();
    const [value, setValue] = React.useState(2);
    
    return (
      <div className={classes.rating}>
        <Rating name="halfrationg" defaultValue={post.shop_rev_avg} precision={0.5} size="large" readOnly />
      </div>
    );
  }

  return (
      <Grid className={classes.shopMain}>
        <Grid className={classes.card}>
          <Hidden xsDown>
            <CardMedia className={classes.cardMedia} image={'https://www.yogiyo.co.kr'+post.shop_img}/>
          </Hidden>
          <div className={classes.cardDetails}>
            <CardContent>
              <Typography component="h2" variant="h5" className={classes.marginbottom}>
                {post.shop_name}
              </Typography>
              <HalfRating/>
              <Typography variant="h6" color="textSecondary" className={classes.marginbottom}>
                {post.shop_addr}
              </Typography>
              <Typography variant="subtitle1"  paragraph>
                영업시간 : {post.open_time}
              </Typography>
            </CardContent>
          </div>
        </Grid>
      </Grid>
  );
}

ShopInfo.propTypes = {
  post: PropTypes.object,
};

export default ShopInfo