import React , {useEffect, useState} from 'react'
import axios from 'axios'

import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import ReviewWriteSub from './ReviewWriteSub';

const useStyles = makeStyles((theme) => ({
  mainGrid: {
    marginTop: theme.spacing(3),
  },
  root: {
    flexGrow: 1,
  },

}));


const ReviewWritePage = ({match}) =>{

const [orderData , setOrderData] = useState([]) 
useEffect(() => {
  axios.get(`http://localhost:8080/reviewwrite/${match.params.or_id}`)
  .then(res=>{
      // alert(`List Success`)
      setOrderData(res.data[0])
      console.log(res.data[0])
  })
  .catch(e=>{
      alert(`List Failure`)
      throw(e)
  })
},[])




return(

  <React.Fragment>
    <CssBaseline />
    <Grid container justify="center" spacing={5} className={useStyles.mainGrid}>
      <ReviewWriteSub post={orderData}/>
    </Grid>
  </React.Fragment>
)
}


export default ReviewWritePage