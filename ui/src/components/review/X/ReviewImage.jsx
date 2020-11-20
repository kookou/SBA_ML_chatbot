import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import GridList from '@material-ui/core/GridList';
import GridListTile from '@material-ui/core/GridListTile';

const tileData = [
    {
        img: 'https://source.unsplash.com/random',
        title:'하',
        author: 'author',
        featured: true,
    },
    {
      img: 'https://source.unsplash.com/random',
      title:'하',
      author: 'author',
      featured: true,
    },
    {
      img: 'https://source.unsplash.com/random',
      title:'하',
      author: 'author',
      featured: true,
    },
    {
      img: 'https://source.unsplash.com/random',
      title:'하',
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
    backgroundColor: theme.palette.background.paper,
  },
  gridList: {
    // Promote the list into his own layer on Chrome. This cost memory but helps keeping high FPS.
    transform: 'translateZ(0)',
  },


}));

export default function ReviewImage() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
        <GridList cellHeight={200} className={classes.gridList} cols={tileData.length}>
        {tileData.map((tile) => (
            <GridListTile key={tile.img} cols={tile.cols || 1}>
            <img src={tile.img} alt={tile.title} />
            </GridListTile>
        ))}
        </GridList>
    </div>
  );
}