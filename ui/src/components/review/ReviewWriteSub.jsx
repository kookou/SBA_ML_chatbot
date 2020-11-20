import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import axios from 'axios';
import { Link, useHistory } from "react-router-dom";

import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Rating from '@material-ui/lab/Rating';
import Divider from '@material-ui/core/Divider';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
    maxWidth: 1000,
    marginTop : theme.spacing(7)
    // backgroundColor: theme.palette.background.paper,
    // margin:theme.spacing(0),
  },
  input: {
    display: 'none',
  },
  rating: {
    display: 'flex',
    flexDirection: 'column',
    '& > * + *': {
      marginTop: theme.spacing(1),
    },
  },
  button: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(1),
  },
  textfield: {
    marginTop: theme.spacing(1),
  },
  smallbutton: {
    marginRight: theme.spacing(1),
  },
  divider: {
    width: 'fit-content',
    border: `1px solid ${theme.palette.divider}`,
    borderRadius: theme.shape.borderRadius,
    backgroundColor: theme.palette.background.paper,
    color: theme.palette.text.secondary,
    '& svg': {
      margin: theme.spacing(1.5),
    },
    '& hr': {
      margin: theme.spacing(0),
    },
    marginRight: theme.spacing(1),
  },
  margin: {
    marginTop: theme.spacing(5),
    marginBottom: theme.spacing(2),
  },
  marginzero: {
    margin: theme.spacing(0),
  },
  marginmenu: {
    marginTop: theme.spacing(0),
    marginBottom: theme.spacing(5),
  },

}));


const ReviewWriteSub = (props) => {
  const { post } = props;
  const classes = useStyles();
  // const [value, setValue] = React.useState(0);
  const or_id = post.or_id;
  // const order_time = post.order_time;
  // const userid = sessionStorage.getItem("sessionUser");
  // const shop_id = post.shop_id;
  // const food_id = post.food_id;
  const [quantity_rate, setQuantity] = React.useState(5);
  const [taste_rate, setTeste] = React.useState(5);
  const [delivery_rate, setDelivery] = React.useState(5);
  const date = new Date();
  const review_time = date.getFullYear()+"-"+(date.getMonth()+1)+"-"+date.getDate()+"/"+ date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
  const [review_cmnt, setReviewCmnt] = useState();
  const history = useHistory();

  const reviewWrite = () => {
    axios.post(`http://localhost:8080/reviewwrite`,
      { or_id, quantity_rate, taste_rate, delivery_rate, review_time, review_cmnt })
      .then(res => {
        // alert("리뷰작성완료")
      }).then(
        history.push("/mypage")
      ).catch(error => {
        alert("안돼 돌아가")
      })
  }

  return (


    <div className={classes.root}>
      <Grid item xs={12} md={12} justify="center">
        <Grid container justify="center" item xs={12} md={12} className={classes.margin}>
          <Typography variant="h4">
            {post.shop_name}
          </Typography>
        </Grid>
        <Grid container justify="center" item xs={12} md={12} className={classes.marginmenu}>
          <Typography color="textSecondary" variant="h6">
            {post.food_name}
          </Typography>
        </Grid>
        <Divider variant="middle" className={classes.marginzero} />
        <Grid container justify="center" item xs={12} md={12} className={classes.margin}>
          <Typography color="textSecondary" variant="h6">
            이 음식점에 대한 상세한 평가를 해주세요.
          </Typography>
        </Grid>
        <Grid container justify="center" item xs={12} md={12} className={classes.margin}>
          <Grid container item xs={12} md={3} alignItems="center" justify="center">
            <Grid container>
              <Grid item xs>
                <Typography gutterBottom variant="h6">
                  맛
              </Typography>
              </Grid>
              <Grid item>
                <Rating name="teste" defaultValue={2.5} precision={0.5} size="large"
                  value={taste_rate}
                  onChange={(event, newValue) => {
                    setTeste(newValue);
                  }} />
              </Grid>
            </Grid>

            <Grid container >
              <Grid item xs >
                <Typography gutterBottom variant="h6">
                  양
              </Typography>
              </Grid>
              <Grid item>
                <Rating name="quantity" defaultValue={2.5} precision={0.5} size="large"
                  value={quantity_rate}
                  onChange={(event, newValue) => {
                    setQuantity(newValue);
                  }} />
              </Grid>
            </Grid>

            <Grid container >
              <Grid item xs>
                <Typography gutterBottom variant="h6">
                  배달
              </Typography>
              </Grid>
              <Grid item>
                <Rating name="delivery" defaultValue={2.5} precision={0.5} size="large"
                  value={delivery_rate}
                  onChange={(event, newValue) => {
                    setDelivery(newValue);
                  }} />
              </Grid>
            </Grid>
          </Grid>
        </Grid>
        <Grid container>
          <form className={classes.root} noValidate autoComplete="off">
            <TextField className={classes.textfield}
              onChange={e => setReviewCmnt(e.target.value)}
              id="outlined-multiline-static"
              fullWidth
              multiline
              rows={20}
              defaultValue="리뷰를 작성해 주세요"
              variant="outlined"
            />
          </form>
        </Grid>
        <Grid container className={classes.button} justify="flex-end">
          <Button onClick={reviewWrite} className={classes.smallbutton} variant="contained" color="primary" disableElevation>
            등록 완료
          </Button>
          <Button variant="contained" color="primary" disableElevation>
            등록 취소
          </Button>
        </Grid>
      </Grid >
    </div>

  );
}

ReviewWriteSub.propTypes = {
  archives: PropTypes.array,
  description: PropTypes.string,
  social: PropTypes.array,
  title: PropTypes.string,
};

export default ReviewWriteSub