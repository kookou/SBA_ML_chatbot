import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';
import GridListTileBar from '@material-ui/core/GridListTileBar';
import IconButton from '@material-ui/core/IconButton';
import Grid from '@material-ui/core/Grid';
import DeleteForeverIcon from '@material-ui/icons/DeleteForever';




const imageupload = [
  {
    defaultimg: 'https://beckie-khmer.com/storage/default.png',
    title: '이미지를 등록해 주세요',
    author: 'author',
    featured: true,
  },
  {
    defaultimg: 'https://beckie-khmer.com/storage/default.png',
    title: '이미지를 등록해 주세요',
    author: 'author',
    featured: true,
  },
  {
    defaultimg: 'https://beckie-khmer.com/storage/default.png',
    title: '이미지를 등록해 주세요',
    author: 'author',
    featured: true,
  },
  {
    defaultimg: 'https://beckie-khmer.com/storage/default.png',
    title: '이미지를 등록해 주세요',
    author: 'author',
    featured: true,
  },


]

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'space-around',
    overflow: 'hidden',
  },
  gridList: {
    flexWrap: 'nowrap',
    // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
    transform: 'translateZ(0)',
  },
  // title: {
  //   color: theme.palette.primary.light,
  // },
  
  titleBar: {
    background:
      'linear-gradient(to top, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.1) 70%, rgba(0,0,0,0) 100%)',
  },
  button: {
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(1),
  },
  input: {
    display: 'none',
  },
}));

const ReviewImageUpload = (props) => {
  const classes = useStyles();

  return (
    <Grid>
      <input
        accept='image/jpg,impge/png,image/jpeg,image/gif'
        name='profile_img'
        // onChange={this.handleFileOnChange}
        className={classes.input}
        id="contained-button-file"
        multiple
        type="file"
      />
      <label htmlFor="contained-button-file">
        <GridList className={classes.gridList} cols={4}>
          {imageupload.map((data) => (
            <GridListTile key={data.defaultimg}>
              <img src={data.defaultimg} alt={data.title} />
              <GridListTileBar
                classes={{
                  root: classes.titleBar,
                  title: classes.title,
                }}
                actionIcon={
                  <IconButton aria-label="delete" disabled color="primary">
                    <DeleteForeverIcon className={classes.title} />
                  </IconButton>
                }
              />
            </GridListTile>
          ))}
        </GridList>
        {/* <Button className={classes.button} variant="contained" color="primary" component="span" alignItems="center">
          사진 등록
        </Button> */}
      </label>
    </Grid>
  );
}
export default ReviewImageUpload