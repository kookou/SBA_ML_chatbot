export const addTodoAction = todo => ({ // action creator
    type : "ADD_TODO",  // action 객체(type + payload)
    payload : todo
})
export const toggleTodoAction = todoId => ({
    type : "TOGGLE_TODO",
    payload : todoId
})
export const deleteTodoAction = todoId => ({
    type : "DELETE_TODO",
    payload : todoId
})

// Initial State
const initialState = {todos: []}

// Reducer
const todoReducer = (state = initialState, action) => {
    switch(action.type){
        case "ADD_TODO" : 
            return {...state, todos: [...state.todos, action.payload ]}

        case "TOGGLE_TODO" : 
            return {...state, todos: 
                        state.todos.map(todo => todo.todoId === action.payload ?
                            {...todo, complete: !todo.complete} : todo)
            }
        case "DELETE_TODO" : 
            return {...state, todos: state.todos.filter(todo => todo.todoId !== action.payload)}
        default:
            return state
    }
}

export default todoReducer