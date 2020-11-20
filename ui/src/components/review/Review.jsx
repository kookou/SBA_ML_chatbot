import React , {useEffect, useState} from 'react'
import axios from 'axios'

import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import CircularProgress from '@material-ui/core/CircularProgress';

import ShopInfo from './ShopInfo';
import MenuAndReviewArea from './MenuAndReviewArea';


const useStyles = makeStyles((theme) => ({
  mainGrid: {
    marginTop: theme.spacing(3),
  },
  root: {
    flexGrow: 1,
    minHeight : 600,
  },

  bg: {
    backgroundColor: theme.palette.background.paper,
  },


}));

const Review = ({match}) => {
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (loading) {
        setTimeout(() => {
            setLoading(false);
        }, 2000);
    }
}, [loading]);

  // console.log(match.params.shopid)
  const classes = useStyles();
  const [shopdata, setDataShop] = useState([])
  const [fooddata, setDataFood] = useState([])
  const [reviewdata, setDatareview] = useState([])
  useEffect(() => {
      // alert(match.params.shopid)
      axios.get(`http://localhost:8080/shop/${match.params.shop_id}`)
      .then(res=>{
          // alert(`List Success`)
          setDataShop(res.data[0].Shop[0])
          setDataFood(res.data[1].Food)
          setDatareview(res.data[2].Review)
          
          // console.log("Review" +res.data[2].Review)
          // console.log("Food" +res.data[1].Food)
      })
      .catch(e=>{
          alert(`List Failure`)
          throw(e)
      })

  },[])


  return (
    <React.Fragment>
      <CssBaseline />
      <Grid container justify="center" alignItems="center" className={classes.root}>
      {loading ? <CircularProgress /> :
       <>
      <Grid container justify="center" >
          <ShopInfo post={shopdata}/> {/* {} 객체만 보내줌 */}
      </Grid>
      <Grid container justify="center" spacing={5} className={useStyles.mainGrid}>
         <MenuAndReviewArea reviews={reviewdata} food={fooddata}/>
      </Grid>
      </>
      }
      </Grid>
    </React.Fragment>
  )
}

export default Review