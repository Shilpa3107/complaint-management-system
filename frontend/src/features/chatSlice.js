import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  messages: [
    { role: 'assistant', content: 'Send a message describing a complaint, or attach a document, and I\'ll extract the details automatically.' },
  ],
  status: 'idle',
}

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    messageSent(state, action) {
      state.messages.push({ role: 'user', content: action.payload })
      state.status = 'loading'
    },
    fileAttached(state, action) {
      state.messages.push({ role: 'user', content: `📎 ${action.payload}`, isFile: true })
      state.status = 'loading'
    },
    responseReceived(state, action) {
      state.messages.push({ role: 'assistant', content: action.payload })
      state.status = 'succeeded'
    },
    responseFailed(state, action) {
      state.messages.push({ role: 'assistant', content: action.payload || 'Something went wrong. Please try again.' })
      state.status = 'failed'
    },
  },
})

export const { messageSent, fileAttached, responseReceived, responseFailed } = chatSlice.actions
export default chatSlice.reducer