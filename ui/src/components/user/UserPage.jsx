import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Usernav from './Usernav';



const useStyles = makeStyles((theme) => ({
    mainGrid: {
        marginTop: theme.spacing(0),
        backgroundColor: theme.palette.background.paper,
    },
}));

const UserPage = () => {
const classes = useStyles();

  return(
    <React.Fragment>
        <CssBaseline />
        <Grid container justify="center"className={classes.mainGrid}>
            <Usernav/>
        </Grid>
    </React.Fragment>
  )
}
export default UserPage