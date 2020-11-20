import React from 'react';
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import Rating from '@material-ui/lab/Rating';
import { Link } from 'react-router-dom'
import ChatBot from 'react-simple-chatbot';
import ChatbotShopSearch from './ChatbotShopSearch';
import ChatbotMenuSearch from './ChatbotMenuSearch';




export const MenuSearch = () => {
    return (
        <ChatbotMenuSearch/>
    )
}
export const ShopSearch = () => {
    return (
            <p>정보가 없습니다.</p>

    )

}

const ItemChatBot = () => {
const userid = sessionStorage.getItem("sessionUser");

    return(
        <ChatBot
        floating = {true}
        headerTitle = {'메추리'}
        enableSmoothScroll = {true}
        steps={[
            {
                id: '1',
                message: userid+' 님 어서오세요 메추리 입니다.',
                trigger: '2',
            },

            {
                id: '2',
                message: '오늘은 어떤 메뉴를 추천해드릴까요?',
                trigger: '3',
            },
            // {
            //     id: '3',
            //     options: [
            //         { value: 1, label: '메뉴 추천', trigger: 'menu' },
            //         { value: 2, label: '가게 추천', trigger: 'shop' },
            //         { value: 3, label: '메추리 추천', trigger: 'itemSearch' },
            //     ],
            // },
            {
                id: 'menu',
                message: '원하는 메뉴를 말씀해 주세요',
                trigger: '4',
            },
            {
                id: '4',
                user: true,
                validator : (value) => {
                    if (!value) {
                        return '메뉴를 입력해 주세요';
                    }
                    return true;
                },
                trigger: '5',
            },
            {
                id: '5',
                message :'{previousValue} 을(를) 찾으시는군요!',
                trigger: 'inputmenusearch',
            },
            {
                id: 'inputmenusearch',
                message:'{previousValue} 으(로) 로 검색해본 메뉴입니다. ',
                trigger: 'menusearchresult',
            },
            {
                id: 'itemSearch',
                message:'오늘 이런 메뉴는 어떠신가요?',
                trigger: 'menusearchresult',
            },
            {
                id: 'menusearchresult',
                component:  <MenuSearch/>,
                trigger: 'option',
            },
            {
                id: 'option',
                options: [
                    { value: 1, label: '주문 시작', trigger: 'orderstart' },
                    { value: 2, label: '다른메뉴 찾기', trigger: 'menu' },
                    { value: 3, label: '다른가게 찾기', trigger: 'shop' },
                ],
            },

            {
                id: 'shop',
                message: '원하는 가게를 말씀해 주세요',
                trigger: '6',
            },
            {
                id: '6',
                user: true,
                validator : (value) => {
                    if (!value) {
                        return '메뉴를 입력해 주세요';
                    }
                    return true;
                },
                trigger: '7',
            },
            
            {
                id: '7',
                message :'{previousValue} 을(를) 찾으시는군요!',
                trigger: 'inputshopsearch',
            },
            {
                id: 'inputshopsearch',
                message:'{previousValue} 으(로) 로 검색해본 매장입니다. ',
                trigger: 'shopsearchresult',
            },
            {
                id: 'shopsearchresult',
                component: <ShopSearch/>,
                trigger: 'option',
            },
            {
                id: 'orderstart',
                user: true,
                trigger: '6',
            },
        ]}
    />
    );
    
}

export default ItemChatBot;