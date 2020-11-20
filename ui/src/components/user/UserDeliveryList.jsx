import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import Button from '@material-ui/core/Button';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';
import { Link } from 'react-router-dom';


const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
        // minWidth:600,
    },

    paper: {
        marginTop: theme.spacing(1),
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        // maxWidth: 1000,
    },

    avatar: {
        margin: theme.spacing(1),
        backgroundColor: theme.palette.secondary.main,
    },
    inline: {
        // display: 'inline',
    },
    marginzero: {
        margin: 0,
    },

    listtext: {
       paddingRight : 100,
       width : 520,
    },

    paddingzero:{
        padding : 0,
    },
    toolbarLink: {
        
        flexShrink: 0,
        textDecoration: 'none',
        color: 'inherit',
    },

}));

const UserDeliveryList = (props) => {
    const classes = useStyles();
    const { post } = props;
    const date = post.order_time;
    const rdate = new Date(date);

    const day =() =>{
        if (rdate.getDay() == 0) {
            return ' (일)'
        }
        else if (rdate.getDay() == 1) {
            return ' (월)'
        }
        else if (rdate.getDay() == 2) {
            return ' (화)'
        }
        else if (rdate.getDay() == 3) {
            return ' (수)'
        }
        else if (rdate.getDay() == 4) {
            return ' (목)'
        }
        else if (rdate.getDay() == 5) {
            return ' (금)'
        }
        else if (rdate.getDay() == 6) {
            return ' (토)'
        }
    }

    // console.log(date)

    return (
            <Grid item xs={12}>
                <List className={classes.root}>
                    <ListItem alignItems="flex-start">
                        <Link to={"/shop/" + post.shop_id} className={classes.toolbarLink}>
                        <ListItemText
                            primary={post.shop_name}
                            variant="h5"
                            secondary={
                                <React.Fragment>
                                    <Typography 
                                        component="span"
                                        variant="body2"
                                        className={classes.inline}
                                        color="textPrimary"
                                    >
                                        {rdate.getFullYear() + "-" + (rdate.getMonth()+1) + "-" + rdate.getDate()+" "+ rdate.getHours()+":"+rdate.getMinutes()+ day()}
                                    </Typography>
                                    <Typography color="textSecondary" className={classes.listtext}>{post.food_name}</Typography>
                                </React.Fragment>
                            }
                        />
                        </Link>
                        <ListItemSecondaryAction>
                            <Button variant="outlined" color="primary" href={"/reviewwrite/"+post.or_id}>
                                리뷰쓰기
                            </Button>
                        </ListItemSecondaryAction>
                    </ListItem>
                    <Divider variant="inset" component="li" variant="middle" />
                </List>
            </Grid>

    );
}

export default UserDeliveryList