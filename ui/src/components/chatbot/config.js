// Config starter code
import React from 'react';
import { createChatBotMessage } from "react-chatbot-kit";
import BotAvatar from "./BotAvatar";
import ChatbotMenuSearchContents from './ChatbotMenuSearchContents'
import ChatbotOrderContents from './ChatbotOrderContents'
import './Chatbot.css'

const config = {
  initialMessages: [createChatBotMessage(`어서오세요 메추리 입니다.`)],
  botName :"메추리",
  customComponents: {
    header: () => <div className="react-chatbot-kit-chat-header">메추리</div>,
    botAvatar:(props) => <BotAvatar {...props} />
  },
  customStyles:{
    botMessageBox:{
      backgroundColor : "#f50057",
    },
    chatButton :{
      backgroundColor:"#f50057",
    },
  },
  state:{
    menu:'',
    order:'',
  },
  widgets:[
    {
      widgetName: "ChatbotMenuSearchContents",
      widgetFunc: (props) => <ChatbotMenuSearchContents {...props} />,
      mapStateToProps: ["menu"],
    },
    {
      widgetName: "ChatbotOrderContents",
      widgetFunc: (props) => <ChatbotOrderContents {...props} />,
      mapStateToProps: ["order"],
    },
    {

    }
  ],
}

export default config