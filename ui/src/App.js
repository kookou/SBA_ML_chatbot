import React, { useState } from 'react'
import { BrowserRouter as Router, Route, Switch, Redirect } from 'react-router-dom'
import { Header, Footer, Navigation, MainNavigation } from './components/common'
import { Review, Main, ReviewWritePage, UserInfo, UserPage, ShopMain, Order, ShopSearch } from './components'
import { SignIn, SignUp } from './containers/user'
// import {Home, User, Article, Item} from './templates'  
import { createStore, applyMiddleware, combineReducers } from 'redux'
import { Provider } from 'react-redux'
import ReduxThunk from 'redux-thunk'
import axios from 'axios'

import Fab from '@material-ui/core/Fab';
import { makeStyles, useTheme } from '@material-ui/core/styles';

import { Chatbot } from 'react-chatbot-kit'
import config from './components/chatbot/config'
import ActionProvider from './components/chatbot/ActionProvider'
import MessageParser from './components/chatbot/MessageParser'

axios.defaults.withCredentials = true

// 아직 의미 모름
const rootReducer = combineReducers({
    // itemReducer
})

const useStyles = makeStyles((theme) => ({
    root: {
      backgroundColor: theme.palette.background.paper,
      width: 500,
      position: 'relative',
      minHeight: 200,
    },
    fab: {
      position: 'fixed',
      bottom: theme.spacing(4),
      right: theme.spacing(4),
    },
    chat:{
        position: 'fixed',
        bottom: theme.spacing(4),
        right: theme.spacing(4),
    }
}));


const App = () => {
    const classes = useStyles();
    const [loggedIn, setLoggedIn] = useState(sessionStorage.getItem('sessionUser'))
    const [toggle, setToggle] = useState(false)

    return (<>
        {/* <div style={{ width: "1000px", margin: "0 auto" }}> */}

        <Router>
            <Header isAuth={loggedIn} />
            <main>
                <Switch>
                    <Provider store={createStore(rootReducer, applyMiddleware(ReduxThunk))}>
                        <Route exact path="/" component={Main} />
                        <Route path="/main" component={Main} />
                        <Route path="/signIn" component={SignIn} />
                        <Route path="/signUp" component={SignUp} />
                        <Route path="/shop/:shop_id" component={Review} />
                        <Route path="/search/:key" component={ShopSearch} />
                        <Switch>
                            <Route path="/shops/:cat_id" component={ShopMain} />
                            <Route path="/shops" component={ShopMain} />
                        </Switch>
                        <Route path="/reviewwrite/:or_id" component={ReviewWritePage} />
                        {/* <Route path="/userinfo" component={UserInfo} /> */}
                        <Switch>
                            <Route path="/mypage/:userid" component={UserPage} />
                            <Route path="/mypage" component={UserPage} />
                        </Switch>
                        <Route path="/order/:userid" component={Order} />
                        {/* <Redirect from={"/history"} to ={"/about/history"}/>
                        <Redirect from={"/services"} to ={"/about/services"}/>
                        <Redirect from={"/location"} to ={"/about/location"}/>
                        <Route path="/contact" component={Contact}/>
                        <Route path="/events" component={Events}/>
                        <Route path="/products" component={Products}/>
                        <Route component={Error}/> */}
                    </Provider>,
                </Switch>
                <Fab color="secondary" aria-label="add" className={classes.fab} onClick={()=>setToggle(!toggle)}>
                    Chat
                </Fab>
                {toggle &&
                   <div style={{position: 'fixed', right: '35px',  bottom: '80px'}} >
                    <Chatbot config={config} messageParser={MessageParser} actionProvider={ActionProvider} />
                    </div>
                }
            </main>
            <Footer title="Footer" description="SBA React Machine Learning Project Team#1" />
        </Router>
        {/* </div> */}
    </>)
}

export default App