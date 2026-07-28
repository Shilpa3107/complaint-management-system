import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  messages: [
    { role: 'assistant', content: 'Upload a complaint document or paste text above. I will automatically extract the details and populate the form for you.' },
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
    responseReceived(state, action) {
      state.messages.push({ role: 'assistant', content: action.payload })
      state.status = 'succeeded'
    },
    responseFailed(state) {
      state.status = 'failed'
    },
  },
})

export const { messageSent, responseReceived, responseFailed } = chatSlice.actions
export default chatSlice.reducer