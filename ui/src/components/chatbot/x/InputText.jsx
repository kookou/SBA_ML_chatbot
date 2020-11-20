import React, { useEffect, useState } from 'react'
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import { Link } from 'react-router-dom'
import ChatBot from 'react-simple-chatbot';
import ChatbotShopSearch from './ChatbotShopSearch';
import ChatbotMenuSearch from './ChatbotMenuSearch';
import axios from 'axios'



const InputText = (props) => {
    const [chatbotData, setChatbotData] = useState()
    // console.log('chatbot' + JSON.stringify(props.value))
    const {post} = props;
    alert(post)
    useEffect(()=>{
        axios.get(`http://localhost:8080/chatbot/${props.value}`)
            .then(res => {
                // alert(JSON.stringify(res.data[0][0]))
                // alert(JSON.stringify(res.data[0]))
                // console.log(res.data[1])
                console.log(typeof (res.data[1]))
                // setChatbotData(res.data[0])
                if (res.data[1] == '추천') {
                    alert("1")
                    setChatbotData('recommend')
                    // return 'recommend'
                }
                if (res.data[1] == '주문') {
                    alert('2')
                    setChatbotData('order')
                    // return 'order'
                }
                if (res.data[1] == '인사') {
                    alert('3')
                    setChatbotData('greeting')
                    // return 'greeting'
                }
            }).catch(err => {
                alert("안돼 돌아가")
            })
    })
    return(
        chatbotData
    )
}

export default InputText