import React, {useState} from 'react';
import axios from 'axios'
import { Link, useHistory } from "react-router-dom";
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
// import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';
import GpsFixedIcon from '@material-ui/icons/GpsFixed';

const Copyright = () => {
  return (
    <Typography variant="body2" color="textSecondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://material-ui.com/">
        Your Website
        </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const useStyles = makeStyles((theme) => ({
  location: {
    margin: theme.spacing(1, 0, 2),
  },
  paper: {
    marginTop: theme.spacing(8),
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
    height: 45
  },
  root: {
    padding: '2px 4px',
    display: 'flex',
    alignItems: 'center',
    width: 400,
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
}));


const SignUp = () => {

  const classes = useStyles();
  const history = useHistory();
  const [userid, setUserid] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [name, setName] = useState('')
  const [addr, setAddr] = useState('')

  const onSubmitHandler = (e) => {
      e.preventDefault(); // 아무 동작 안하고 버튼만 눌러도 리프레쉬 되는 것을 막는다

      if(password !== confirmPassword){
          return alert('비밀번호와 비밀번호 확인은 같아야 합니다.')
      }
      axios.post(`http://localhost:8080/user`, { 
        userid, password, name,addr
      })
      .then(res => {
       alert(`signUp SUCCESS. ${res.data["userid"]} 가입완료`)
      })
      .then(
        history.push("/signin")
      )
      .catch(error => {
        alert(`signUp FAIL`)
      })
 
}


  return <>
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          회원가입
        </Typography>
        <form className={classes.form} noValidate onSubmit={onSubmitHandler}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField onChange={e => setUserid(e.target.value)}
                variant="outlined"
                required={true}
                fullWidth
                id="email"
                label="이메일 주소"
                name="email"
                autoComplete="email"
                autoFocus
                // error={userid === "" ? true : false }
                // error={false}
                // helperText="This is Helper Text"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField  onChange={e => setName(e.target.value)}
                autoComplete="fname"
                name="nick"
                variant="outlined"
                required="true"
                fullWidth
                id="nick"
                label="닉네임"

               
              />
            </Grid>
            <Grid item xs={12}>
              <TextField onChange={e => setPassword(e.target.value)}
                variant="outlined"
                required
                fullWidth
                name="password"
                label="비밀번호"
                type="password"
                id="password"
                autoComplete="current-password"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField onChange={e => setConfirmPassword(e.target.value)}
                variant="outlined"
                required
                fullWidth
                name="password"
                label="비밀번호 확인"
                type="password"
                id="password"
                autoComplete="current-password"
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="h6" align="center">
                지역 설정
              </Typography>
              <TextField onChange={e => setAddr(e.target.value)}
                variant="outlined"
                required
                fullWidth
                name="password"
                label="동명(읍,면)으로 검색 (ex.서초동)"
                id="password"
                autoComplete="current-password"
              />
              {/* <Button
                type="submit"
                fullWidth
                variant="contained"
                color="primary"
                className={classes.location}
                startIcon={<GpsFixedIcon />}
              >
                현재 위치로 찾기
              </Button> */}
            </Grid>

          </Grid>

          <Button 
            // onSubmit={onSubmitHandler}
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            className={classes.submit}
          >
            회원가입 완료
          </Button>
          <Grid container justify="flex-end">
            <Grid item>
              <Link href="/signin" variant="body2">
                이미 회원이신가요?
              </Link>
            </Grid>
          </Grid>
        </form>
      </div>
      <Box mt={5}>
        <Copyright />
      </Box>
    </Container>
  </>
}

export default SignUp