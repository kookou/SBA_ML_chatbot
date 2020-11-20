import React from 'react';
import { Link, useHistory } from "react-router-dom";
import { useState } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';

import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Divider from '@material-ui/core/Divider';
import Dialog from '@material-ui/core/Dialog';
import DialogActions from '@material-ui/core/DialogActions';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import Button from '@material-ui/core/Button';
import Rating from '@material-ui/lab/Rating';
import Chip from '@material-ui/core/Chip';

const useStyles = makeStyles((theme) => ({
  divroot: {
    flexGrow: 1,
    // marginTop: theme.spacing(3),
    padding: 0

  },
  root: {
    display: 'flex',
    width: "100%",
    padding: 20
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
    padding: 0,
    height: "100"

  },
  content: {
    padding: 0,
    '&:last-child': {
      paddingBottom: 0,
    },
    paddingRight: 20,

  },
  cover: {
    width: 150,
    height: 100,
  },
  modalcover: {
    width: 444,
    height: 310,
  },
  modalsize: {
    // maxWidth:350,
    margin: 0,
  },
  paper: {
    // padding: theme.spacing(2),
    // textAlign: 'center',
    color: theme.palette.text.secondary,
  },
  toolbarLink: {
    textDecoration: 'none',
  },
  marr: {
    marginRight: theme.spacing(1),
  },
  marl: {
    marginLeft: -4,
  }

}));


const ShopMenuInfo = (props) => {
  const { post } = props;
  const classes = useStyles();
  const date = new Date();
  const order_time = date.getFullYear() + "-" + (date.getMonth() + 1) + "-" + date.getDate() + "/" + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
  const userid = sessionStorage.getItem("sessionUser");
  const food_id = post.food_id;
  const shop_id = post.shop_id;
  // const order_time = date.getFullYear()+"-"+date.getMonth()+"-"+date.getDate()+" " + date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
  // const [userid, setUserid] = useState();
  // const [food_id, setFoodid] = useState();
  // const [order_time,setOrderTime] = useState();
  // const [shop_id,setShopid] = useState();
  const history = useHistory();
  const [open, setOpen] = React.useState(false);
  // console.log(post)  
  const handleClickOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };
  const newOrder = (e) => {
    e.preventDefault()
    // setUserid(sessionStorage.getItem("sessionUser"));
    // setFoodid(post.food_id);
    // setOrderTime(date.getFullYear()+"-"+date.getMonth()+"-"+date.getDate()+"' '" + date.getHours()+":"+date.getMinutes()+":"+date.getSeconds())
    // setShopid(post.shop_id)
    // debugger
    // alert(userid)
    axios.post(`http://localhost:8080/order`, { userid, food_id, order_time, shop_id })
      .then(res => {
        history.push("/order/" + userid)
      })
      .catch(err => {
        alert("실패")
      })
  }


  return (

    <div className={classes.divroot}>
      <Dialog className={classes.modalsize}
        maxWidth="xs"
        wrap="nowrap"
        open={open}
        onClose={handleClose}
        aria-labelledby="alert-dialog-title"
      >
        <CardMedia
          className={classes.modalcover}
          image={post.food_img !== 'no_image' ? post.food_img : 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAD8CAMAAAAFbRsXAAAAY1BMVEX////39/eysrJjY2O5ublgYGCJiYmdnZ2mpqbt7e1nZ2ecnJz6+vqpqalpaWm/v79ycnLh4eF+fn5tbW3y8vLY2NjNzc2Dg4ORkZHo6OjFxcXZ2dm3t7dcXFyAgICWlpZUVFRdQGDEAAADyUlEQVR4nO3YW3OqOgCGYSCAEDEEApFDlf7/X7kTUEFrZ9aeNbJu3ueiTWmk+ciJNAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4M8UedX8vJpX+d/eYidFf2tq85XauVDd9UUQRF281m2+4o2v+VrYhI9vTZQOhb/DUz27T5AmS8u5kB8uw1xIna5zXw4u4VFka93+O3GElP5b8u0vFXayvu3x0d0lPyaRjzVcNvUu6U5BuiS6BUmWINfzuVamPl8nH0RugjSld1AqG3zBXwqjy9z2OXB+EPMPlf/t19mYk6+3V4904iVIn+et0GXe58VLkKAoiiCflDw1hS/OQZKvOYjcBHH1gqLUSrk+vdX7F0F8lqS+PcfnIL6NmVHGPCbO+yBBMGZa1bXpduqO4JcgrVDLVP4RxKaqtqUxU7X87ILMoQ6bII2Nzq47osbWQuvT0O+R422Qwk2Drv8RpKjiqxJ1GwSlkSqdGxhG0izWIJWSiZiT5pFJhIiDPYxneXoNYhOtxal4DdJooXQ07xT90aik+yVIUGY2vH+oKqddcgS2VnWxBFHy8u2f4yjNqdVybvLT0Oqn4dHAvpzCOYg4Dta6EfcIUoR+tocLP9X3me4nZZLqFkTXuncjXKqpcYtOkrodYhOkCN1aFIZrC8Nwmey+nZs5UqavjjvkqDqlVbYEEafWhn2XmKPf621qumYbpDq9cn32ZtWKr/VMu81o0X0+R/FlrpGWY/CYI2F2jpahUEXPG6Kt9UJJsxSu+bsgfbvIZDqMc2n8fJD2LOLmqM75OtnDpz+7CZLbYRan8rSU3JR+M7Ru3OyZ9ll4Az+wErfM9rV0i+Vm1ept9SaI/4V/j3RvVOs255p7sO6Zd+opSDMOUSrrrGz3yBLaTp7drhC4JSptmzVIrB+tn5LD5hPp1Pql9ylIov00ME89Mh6uiaivV3WppyH4uCZLrvOra9DWabUJEiWPdWZcO8dJjPWL8PcapLDHw2JYg+RnWcftOFbt0Cmzw1tKFdvbEl89DS03XN5/QGjrOzLejJcwv2nWIJHU9xv37pXmU83f2G5Vfxzkd/cgR6UfUVN1+dtW/k/bIFKvu1m3OesKc93scz9C3YO0iZnG+Rn1kRbZa7UPe5wQ/RyR4i7Rm3F0Wa8Lcfkxje8nxCC+KL1siibp9j7GuwP3/RG32zN3Ga51ns7icfXmFsMyWN1LpT/uXkTX7tH2z+r7/t/9TwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgL/xH1ogO7FfoVLsAAAAAElFTkSuQmCC'}
        />
        <Grid container justify="center" direction="row">
          <Typography>
            <DialogTitle id="alert-dialog-title" >{post.food_name}</DialogTitle>
          </Typography>
        </Grid>
        <DialogContent>
          <Grid container justify="space-between" direction="row">
            <DialogContentText id="alert-dialog-description">
              <Typography variant="h6">
                주문 금액
              </Typography>
            </DialogContentText>
            <DialogContentText id="alert-dialog-description">
              <Typography variant="h6" color="secondary">
                가격 : {post.price}
              </Typography>
            </DialogContentText>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary">
            취소
          </Button>
          {/* <Link to={"/order/"+post.food_id} className={classes.toolbarLink}>
            <Button onClick={newOrder}  color="primary" autoFocus>
              주문하기
            </Button>
          </Link> */}
          {/* <Link to={"/order/"+post.food_id} className={classes.toolbarLink}> */}
          <Button onClick={newOrder} color="primary" autoFocus>
            주문하기
            </Button>
          {/* </Link> */}
        </DialogActions>
      </Dialog>
      <CardActionArea onClick={handleClickOpen}>
        <Grid alignItems="center">
          <Card className={classes.root} square elevation={0} >
            <Grid item xs className={classes.details}>
              <CardContent className={classes.content}>
                <Typography variant="h6">
                  {post.food_name}
                </Typography>
                <Typography variant="subtitle1" color="textSecondary">
                  {post.price} 원
                </Typography>
                {/* 음식 예상평점 추가 영역 */}
                <Grid container direction="row" className={classes.marl}>
                  <Rating name="iconstar" defaultValue={1} max={1} readOnly />
                  {post.food_user_avg === undefined
                    ?
                    <Typography variant="subtitle1" color="textSecondary" >
                      예상 {post.food_pred_avg}
                    </Typography>
                    :
                    <>
                      <Typography variant="subtitle1" color="textSecondary" className={classes.marr}>
                        예상 {post.food_pred_avg}
                      </Typography>
                      <Chip color="secondary" size="small" label={'내 평점  ' + post.food_user_avg} />
                    </>
                  }
                </Grid>
              </CardContent>
            </Grid>
            <CardMedia
              className={classes.cover}
              image={post.food_img !== 'no_image' ? post.food_img : 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAAD8CAMAAAAFbRsXAAAAY1BMVEX////39/eysrJjY2O5ublgYGCJiYmdnZ2mpqbt7e1nZ2ecnJz6+vqpqalpaWm/v79ycnLh4eF+fn5tbW3y8vLY2NjNzc2Dg4ORkZHo6OjFxcXZ2dm3t7dcXFyAgICWlpZUVFRdQGDEAAADyUlEQVR4nO3YW3OqOgCGYSCAEDEEApFDlf7/X7kTUEFrZ9aeNbJu3ueiTWmk+ciJNAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4M8UedX8vJpX+d/eYidFf2tq85XauVDd9UUQRF281m2+4o2v+VrYhI9vTZQOhb/DUz27T5AmS8u5kB8uw1xIna5zXw4u4VFka93+O3GElP5b8u0vFXayvu3x0d0lPyaRjzVcNvUu6U5BuiS6BUmWINfzuVamPl8nH0RugjSld1AqG3zBXwqjy9z2OXB+EPMPlf/t19mYk6+3V4904iVIn+et0GXe58VLkKAoiiCflDw1hS/OQZKvOYjcBHH1gqLUSrk+vdX7F0F8lqS+PcfnIL6NmVHGPCbO+yBBMGZa1bXpduqO4JcgrVDLVP4RxKaqtqUxU7X87ILMoQ6bII2Nzq47osbWQuvT0O+R422Qwk2Drv8RpKjiqxJ1GwSlkSqdGxhG0izWIJWSiZiT5pFJhIiDPYxneXoNYhOtxal4DdJooXQ07xT90aik+yVIUGY2vH+oKqddcgS2VnWxBFHy8u2f4yjNqdVybvLT0Oqn4dHAvpzCOYg4Dta6EfcIUoR+tocLP9X3me4nZZLqFkTXuncjXKqpcYtOkrodYhOkCN1aFIZrC8Nwmey+nZs5UqavjjvkqDqlVbYEEafWhn2XmKPf621qumYbpDq9cn32ZtWKr/VMu81o0X0+R/FlrpGWY/CYI2F2jpahUEXPG6Kt9UJJsxSu+bsgfbvIZDqMc2n8fJD2LOLmqM75OtnDpz+7CZLbYRan8rSU3JR+M7Ru3OyZ9ll4Az+wErfM9rV0i+Vm1ept9SaI/4V/j3RvVOs255p7sO6Zd+opSDMOUSrrrGz3yBLaTp7drhC4JSptmzVIrB+tn5LD5hPp1Pql9ylIov00ME89Mh6uiaivV3WppyH4uCZLrvOra9DWabUJEiWPdWZcO8dJjPWL8PcapLDHw2JYg+RnWcftOFbt0Cmzw1tKFdvbEl89DS03XN5/QGjrOzLejJcwv2nWIJHU9xv37pXmU83f2G5Vfxzkd/cgR6UfUVN1+dtW/k/bIFKvu1m3OesKc93scz9C3YO0iZnG+Rn1kRbZa7UPe5wQ/RyR4i7Rm3F0Wa8Lcfkxje8nxCC+KL1siibp9j7GuwP3/RG32zN3Ga51ns7icfXmFsMyWN1LpT/uXkTX7tH2z+r7/t/9TwUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgL/xH1ogO7FfoVLsAAAAAElFTkSuQmCC'}
            />
          </Card>
          <Divider />
        </Grid>
      </CardActionArea>
    </div >
  );
}

ShopMenuInfo.propTypes = {
  post: PropTypes.object,
};

export default ShopMenuInfo