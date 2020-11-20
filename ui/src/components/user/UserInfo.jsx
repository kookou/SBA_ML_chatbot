import React from 'react';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import Grid from '@material-ui/core/Grid';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import GpsFixedIcon from '@material-ui/icons/GpsFixed';

const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(1),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(3),
  },
  submit: {
    margin: theme.spacing(1, 0, 2),
    height:45
  },
  root: {
    padding: '2px 4px',
    alignItems: 'center',
    
  },
  input: {
    marginLeft: theme.spacing(1),
    flex: 1,
  },
  iconButton: {
    padding: 10,
  },
  divider: {
    height: 28,
    margin: 4,
  },
  location :{
    margin: theme.spacing(1, 0, 2),
  },
  width:{
    // width:"50%"
  },
}));



const UserInfo = () => {
  const classes = useStyles();
  return <>
      <CssBaseline />
      <div className={classes.paper}>

        <form className={classes.form} noValidate>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                autoComplete="fname"
                name="nick"
                variant="outlined"
                required
                fullWidth
                id="nick"
                label="닉네임"
                size="small"
                autoFocus
                
              />
            </Grid>

            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                id="email"
                label="이메일 주소"
                name="email"
                autoComplete="email"
                size="small"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="현재 비밀번호"
                type="password"
                id="password"
                size="small"
                autoComplete="current-password"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="새로운 비밀번호"
                type="password"
                id="password"
                size="small"
                autoComplete="current-password"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="새로운 비밀번호 확인"
                type="password"
                id="password"
                size="small"
                autoComplete="current-password"
              />
            </Grid>

            <Grid item xs={12}>
              <Typography variant="h6" align="center">
                지역 설정
              </Typography>
              <TextField
                variant="outlined"
                required
                fullWidth
                name="password"
                label="동명(읍,면)으로 검색 (ex.서초동)"
                type="password"
                id="password"
                size="small"
                // autoComplete="current-password"
              />
              <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.location}
                startIcon={<GpsFixedIcon />}
              >
                현재 위치로 찾기
              </Button>
            </Grid>

          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            수정 완료
          </Button>

        </form>
      </div>
  </>
}

export default UserInfo