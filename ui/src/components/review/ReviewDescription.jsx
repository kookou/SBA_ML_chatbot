import React from 'react';
import PropTypes from 'prop-types';

import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import CardContent from '@material-ui/core/CardContent';
import Rating from '@material-ui/lab/Rating';
import Divider from '@material-ui/core/Divider';
import Card from '@material-ui/core/Card';
import SubdirectoryArrowRightIcon from '@material-ui/icons/SubdirectoryArrowRight';
import Chip from '@material-ui/core/Chip';


const useStyles = makeStyles((theme) => ({
  card: {
    display: 'flex',
  },
  cardDetails: {
    maxwidth: 952,
    padding: 0,
    flex: 1,
    // padding : 20,
  },
  root: {
    display: 'flex',
    flexDirection: 'column',
    '& > * + *': {

    },
  },
  marginzero: {
    margin: 0,
  },
  marginbottom: {
    marginBottom: theme.spacing(2),
  },
  marginr: {
    marginRight: theme.spacing(2),
  },
  rating: {
    marginBottom: theme.spacing(1),
  },
  card:{
    marginBottom: theme.spacing(2),
    backgroundColor: theme.palette.grey[200]
  },
  marginl:{
    marginLeft : theme.spacing(2)
  },
  marginlm:{
    marginLeft : -3
  }

}));


const ReviewDescription = (props) => {
  const sessionuserid = sessionStorage.getItem("sessionUser");
  const classes = useStyles();
  const { post } = props;
  // console.log(post)
  const taste = post.taste_rate;
  const quan = post.quantity_rate;
  const deli = post.delivery_rate;
  const date = post.review_time;
  const rdate = new Date(date);


  function HalfRating() {
    const classes = useStyles();
    const rateavg = (taste + quan + deli) / 3
    return (
        <Rating name="rating" defaultValue={rateavg} max={5} precision={0.5} readOnly className={classes.marginlm}/>
    );
  }

  return (
    <Grid item xs={12}>
      <Grid container spacing={3}>
        <Grid alignItems="center" item xs={12}>
          <Grid container direction="row" alignItems="center">
            <Typography component="h6" variant="h6" className={classes.marginr}>
              {post.userid}
            </Typography>
            <Typography variant="body2" color="textSecondary" className={classes.marginr} >
              {rdate.getFullYear() + "-" + (rdate.getMonth()+1) + "-" + rdate.getDate()}
            </Typography>
            {post.userid === sessionuserid
                    ?
                    <Chip color="secondary" size="small" label="내 리뷰" />
                    :
                    <>
                    </>
                  }
          </Grid>
          <Grid container direction="row" alignItems="center">
            {/* <Rating name="avg" defaultValue={(post.taste_rate + post.quantity_rate + post.delivery_rate) / 3} max={5} className={classes.marginr} readOnly /> */}
            <HalfRating  />
            <Typography variant="subtitle1" color="textSecondary" className={classes.marginl}>
              맛
              </Typography>
            <Rating name="iconstar" defaultValue={1} max={1} readOnly />
            <Typography variant="subtitle1" color="textSecondary" className={classes.marginr}>
              {post.taste_rate}
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              양
              </Typography>
            <Rating name="iconstar" defaultValue={1} max={1} readOnly />
            <Typography variant="subtitle1" color="textSecondary" className={classes.marginr}>
              {post.quantity_rate}
            </Typography>
            <Typography variant="subtitle1" color="textSecondary">
              배달
              </Typography>
            <Rating name="iconstar" defaultValue={1} max={1} readOnly />
            <Typography variant="subtitle1" color="textSecondary" className={classes.marginr}>
              {post.delivery_rate}
            </Typography>
          </Grid>
          <Typography variant="subtitle1" color="textSecondary">
            {post.food_name}
          </Typography>
          <Typography variant="subtitle1" paragraph className={classes.marginbottom}>
            {post.review_cmnt}
          </Typography>
          {post.owner_cmnt !== "1"
          ?
          <Card className={classes.card} square elevation={0}>
            <CardContent>
              <Typography  component="h6"  variant="subtitle1">
                <SubdirectoryArrowRightIcon fontSize="inherit"/>사장님 
              </Typography>
              <Typography variant="body2" color="textSecondary" component="p">
               {post.owner_cmnt}
              </Typography>
            </CardContent>
          </Card>
          :
          <div></div>
          }

        </Grid>
      </Grid>
      <Divider variant="middle" className={classes.marginzero} />
    </Grid>
  );
}

ReviewDescription.propTypes = {
  post: PropTypes.object,
};

export default ReviewDescription