import React, {useState} from 'react'
import axios from 'axios'
import { Link, useHistory } from "react-router-dom";
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
// import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import Box from '@material-ui/core/Box';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';




const Copyright = () =>{
    return (
      <Typography variant="body2" color="textSecondary" align="center">
        {'Copyright © '}
        <Link color="inherit" href="https://material-ui.com/">
          챗봇
        </Link>{' '}
        {new Date().getFullYear()}
        {'.'}
      </Typography>
    );
  }
  
  const useStyles = makeStyles((theme) => ({
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
      marginTop: theme.spacing(1),
    },
    submit: {
      margin: theme.spacing(1, 0, 2),
      height:45
    },
  }));



const SignIn = () => {

    const classes = useStyles();
    const [userid, setUserid] = useState('')
    const [password, setPassword] = useState('')
    const history = useHistory();
    const login = e => {
      e.preventDefault()
      axios.post(`http://localhost:8080/access`, {userid, password})
          .then(res => {
              alert(`Welcome ! ${res.data["name"]}.  ${res.data["userid"]}'s connection is successful. ! `)
              
              sessionStorage.setItem("sessionUser", res.data['userid']);
              history.push("/main");
              window.location.reload()
    
          })
          .catch(error => {
              alert("Please check your ID or password.");
              window.location.reload();
          })

    }

  
    return (
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <div className={classes.paper} >
          <Avatar className={classes.avatar}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            로그인
          </Typography>         
          <form className={classes.form} noValidate>
            <TextField onChange={e => setUserid(`${e.target.value}`)}
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="email"
              label="이메일 주소"
              name="email"
              autoComplete="email"
              autoFocus
            />
            <TextField onChange={e => setPassword(`${e.target.value}`)}
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="비밀번호"
              type="password"
              id="password"
              autoComplete="current-password"
            />
            <FormControlLabel
              control={<Checkbox value="remember" color="textSecondary" />}
              label="자동 로그인"
            />
            <Button onClick= {login}
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
            >
              로그인
            </Button>
            <Grid container>
              <Grid item xs>
                <Link href="#" variant="body2">
                  패스워드 찾기
                </Link>
              </Grid>
              <Grid item>
                <Link href="/signUp" variant="body2">
                  {"아직 회원이 아니신가요?"}
                </Link>
              </Grid>
            </Grid>
          </form>
        </div>
        <Box mt={8}>
          <Copyright />
        </Box>
      </Container>
    );
  }

export default SignIn