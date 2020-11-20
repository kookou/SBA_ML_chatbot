import {createStore} from 'redux'
import todoReducer from './todoReducers'

const store = createStore(todoReducer)

export default store