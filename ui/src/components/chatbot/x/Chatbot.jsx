import React, { useEffect, useState, Component } from 'react'
import PropTypes from 'prop-types';
import { makeStyles, useTheme } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import { Link } from 'react-router-dom'
import ChatBot from 'react-simple-chatbot';
import ChatbotShopSearch from './ChatbotShopSearch';
import ChatbotMenuSearch from './ChatbotMenuSearch';
// import InputText from './InputText';
import axios from 'axios'
import { ThemeProvider } from 'styled-components';



const theme = {
    background: '#f5f8fb',
    fontFamily: 'Helvetica Neue',
    headerBgColor: '#3f51b5',
    headerFontColor: '#fff',
    headerFontSize: '15px',
    botBubbleColor: '#3f51b5',
    botFontColor: '#fff',
    userBubbleColor: '#fff',
    userFontColor: '#3f51b5',
};



export const MenuSearch = () => {
    return (
        <ChatbotMenuSearch />
    )
}

export const ShopSearch = () => {

    return (
        <p>정보가 없습니다.</p>
    )
}

// export const Input = (props) => {
//     // alert(JSON.stringify(props.value))
//     const {post} = props.value;

//     return (
//         <>
//         <InputText post ={post}/>
//         </>
//     )
// }

// export const InputText = (props) => {
//     // const [chatbotData, setChatbotData] = useState()
//     const [intent, setIntent] = useState()
//     console.log('chatbot' + JSON.stringify(props.value))
//     alert(JSON.stringify(props))
//     // const re = ''
//     // useEffect(()=>{
//     axios.get(`http://localhost:8080/chatbot/${props.value}`)
//         .then(res => {

//             alert(JSON.stringify(res.data[0][0]))
//             // alert(JSON.stringify(res.data[0]))
//             // console.log(res.data[1])
//             // console.log(typeof (res.data[1]))
//             // setChatbotData(res.data[0])

//             setIntent(res.data[1])
//             if (res.data[1] == '추천') {
//                 alert("1")
//                 // setChatbotData('recommend')
//             }
//             if (res.data[1] == '주문') {
//                 alert('2')
//                 // setChatbotData('order')
//             }
//             if (res.data[1] == '인사') {
//                 alert('3')
//                 // setChatbotData('greeting')
//             }
//         }).catch(err => {
//             alert("안돼 돌아가")
//         })
//     // })
    
// }

// InputText.propTypes = {
//     steps: PropTypes.object,
// };


const Test2 = (props)=>{

    props.triggerNextStep({trigger: localStorage.getItem('intent')})
    

}

class Test extends Component {
    constructor(props) {

        // console.log(props)
        super(props);
        this.state = {
            inte:'',
            food_name :'',
            food_img:'',
            price:'',
            food_rev_cnt:'',
            shop_id: '',
            result:[],
            // trigger: false,
        };
        // this.triggerNext()
    }
    
    componentWillMount() {
        console.log('죽여')
        const { steps } = this.props;
        this.state.input = steps.input.value;
        // const [chatbotData, setChatbotData] = useState()
        console.log(this.state.input)
        axios.get(`http://localhost:8080/chatbot/${this.state.input}`)
        .then(res => {
            this.state.inte = res.data[1]
            res.data[0].forEach(item => {this.state.result.push({
                food_name : item.food_name,
                food_img: item.food_img,
                price : item.price,
                food_rev_cnt : item.food_rev_cnt,
                shop_id : item.shop_id
            })})
            
            // res.data.forEach
            // alert(JSON.stringify(res.data))
            // console.log('????????????'+res.data[1])
            // setChatbotData(res.data)
            console.log("iiiiiiiiiiiiiiiiiii"+this.state.inte)
            }).catch(err => {
                alert("안돼 돌아가")
            })
        }
        
    // triggetNext() {
    //     this.setState({ trigger: true }, () => {
    //       this.props.triggerNextStep();
    //     });
    // }
    render(){
        // const { trigger} = this.state;
        return(
            <div>
            <p>시ㅏ리ㅏㅓ이라ㅓㅁ</p>
            <ChatbotMenuSearch post={this.state.result}/>
            </div>
        )
    }
}




class Input extends Component {
    constructor(props) {

        // console.log(props)
        super(props);
        this.state = {
            inte:'',
            food_name :'',
            food_img:'',
            price:'',
            food_rev_cnt:'',
            shop_id: '',
            result:[],
            // trigger: false,
        };
        // this.triggerNext()
    }
    
    componentWillMount() {
        console.log('죽여')
        const { steps } = this.props;
        this.state.input = steps.input.value;
        // const [chatbotData, setChatbotData] = useState()
        console.log(this.state.input)
        axios.get(`http://localhost:8080/chatbot/${this.state.input}`)
        .then(res => {
            this.state.inte = res.data[1]
            res.data[0].forEach(item => {this.state.result.push({
                food_name : item.food_name,
                food_img: item.food_img,
                price : item.price,
                food_rev_cnt : item.food_rev_cnt,
                shop_id : item.shop_id
            })})
            
            // res.data.forEach
            // alert(JSON.stringify(res.data))
            // console.log('????????????'+res.data[1])
            // setChatbotData(res.data)
            console.log("iiiiiiiiiiiiiiiiiii"+this.state.inte)
            }).catch(err => {
                alert("안돼 돌아가")
            })
        }
        
    // triggetNext() {
    //     this.setState({ trigger: true }, () => {
    //       this.props.triggerNextStep();
    //     });
    // }
    render(){
        // const { trigger} = this.state;
        return(
            <ChatbotMenuSearch post={this.state.result}/>
        )
    }
}

Component.propTypes = {
    steps: PropTypes.object,
    triggerNextStep: PropTypes.func,
};


Test.propTypes = {
    steps: PropTypes.object,
    triggerNextStep: PropTypes.func,
};

const ItemChatBot = () => {
    const userid = sessionStorage.getItem("sessionUser");
    // const [intent, setIntent] = useState('')
    let intent = ''

    const inputText = async (props) => {
        console.log('chatbot' + JSON.stringify(props.value))
        alert(JSON.stringify(props))
        // const re = ''
        // useEffect(()=>{
        await axios.get(`http://localhost:8080/chatbot/${props.value}`)
            .then(res => {

                alert(JSON.stringify(res.data[0][0]))
                // alert(JSON.stringify(res.data[0]))
                // console.log(res.data[1])
                // console.log(typeof (res.data[1]))
                // setChatbotData(res.data[0])
                alert(res.data[1])
                intent = res.data[1]
                // setIntent(res.data[1])
                localStorage.setItem('intent', res.data[1])
                
                // if (res.data[1] == '추천') {
                //     alert("1")
                //     // setChatbotData('recommend')
                // }
                // if (res.data[1] == '주문') {
                //     alert('2')
                //     // setChatbotData('order')
                // }
                // if (res.data[1] == '인사') {
                //     alert('3')
                //     // setChatbotData('greeting')
                // }
                return intent
            })
            .catch(err => {
                alert("안돼 돌아가")
                return err
            })
            
    }

    return (
        <ThemeProvider theme={theme}>
            <ChatBot
                floating={true}
                headerTitle={'메추리'}
                enableSmoothScroll={true}
                steps={[
                    {
                        id: '1',
                        message: userid + ' 님 어서오세요 메추리 입니다.',
                        trigger: '2',
                    },
                    {
                        id: '2',
                        message: '무엇을 도와드릴 까요?',
                        trigger: 'input',
                    },
                    {
                        id: 'input',
                        user: true,
                        validator: (value) => {
                            if (!value) {
                                return '입력된 내용이 없습니다.';
                            }
                            return true;
                        },
                        // trigger: (value) => {
                            // inputText(value);                             
                        //     setTimeout(() => {}, 50000)
                        //     return intent
                        //     // return localStorage.getItem('intent')
                        // },
                        // component:<Test/>
                        trigger : 'test'
                    },
                    {
                        id: '추천',
                        asMessage: true,
                        message: '{previousValue} 을(를) 찾으시는군요!',
                        trigger: '1',

                    },
                    {
                        id: '주문',
                        message: '오늘 어떠신가요?',
                        trigger: '1',
                    },
                    {
                        id: '인사',
                        message: '오늘 이런 메뉴는 어떠신가요?',
                        trigger: '1',
                    },
                    {
                        id: 'test',
                        component: <Test/>,
                        // message: 'ㅅㅄㅄㅄㅄ',
                        trigger:'1',
                        // end: true,
                    },
                    {
                        id: '12',
                        component: <Test2 />,
                        // message: 'ㅅㅄㅄㅄㅄ',
                        trigger:'1',
                        // end: true,
                    },


                ]}
            />
        </ThemeProvider>
    );
}

export default ItemChatBot;