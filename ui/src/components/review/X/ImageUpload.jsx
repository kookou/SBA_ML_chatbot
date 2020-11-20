
import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
    root: {
      flexGrow: 1,
      width: '100%',
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
      marginBottom: theme.spacing(5),
    },
    marginzero:{
      margin : theme.spacing(0),
    },
    marginmenu: {
      marginTop: theme.spacing(0),
      marginBottom: theme.spacing(5),
    },
  
  }));
  
  


class fileupload extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            file: '',
            previewURL: ''
        }
    }
    
  }
<Grid container alignItems="center" justify="flex-end">
    <Grid>
        <input
            accept='image/jpg,impge/png,image/jpeg,image/gif'
            name='profile_img'
            onChange={this.handleFileOnChange}
            className={classes.input}
            id="contained-button-file"
            multiple
            type="file"
        />

        <label htmlFor="contained-button-file">
            <Button className={classes.button} variant="contained" color="primary" component="span" alignItems="center">
                사진 등록
        </Button>
        </label>
    </Grid>
</Grid>