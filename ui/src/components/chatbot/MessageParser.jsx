import axios from 'axios'
import React, { useEffect, useState } from 'react'
// MessageParser starter code
class MessageParser {
  constructor(actionProvider, state) {
    this.actionProvider = actionProvider;
    this.state = state;
  }

  parse(message) {
    console.log(message)
    let lowercase = message
    let key = ''
    // if (message == null){
    //   this.actionProvider.nonMassage()
    // } 
    const userid = sessionStorage.getItem("sessionUser");
    axios.get(`http://localhost:8080/chatbot/${lowercase}`)
      .then(res => {
        // alert(JSON.stringify(res.data[0][0]))
        key = res.data[1]
        // localStorage.setItem('intent', res.data[1])
        // localStorage.setItem('key' , res.data[2])
        // setKeyData(res.data[1])
        if (res.data[1].includes("추천")) {
          this.actionProvider.recommendSearchBotMessage(res.data[2], res.data[0][0], userid);
        }
        if (res.data[1].includes("주문")) {
          this.actionProvider.orderBotMessage(res.data);
        }
        if (res.data[1].includes("인사")) {
          if (userid != null) {
            this.actionProvider.greetingLoginUserBotMessage(userid);
          } else {
            this.actionProvider.greetingBotMessage();
          }
        }
        if (res.data[1].includes("언제")) {
          this.actionProvider.recommendBotMessage();
        }
        if (res.data[1].includes("none") || res.data == '') {
          this.actionProvider.sorryBotMessage();
        }

      }).catch(err => {
        this.actionProvider.sorryBotMessage();
      })
    // console.log(key)
    // lowercase = localStorage.getItem('intent')
    // key = localStorage.getItem('key')



  }
}

export default MessageParser;
