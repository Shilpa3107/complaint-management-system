import { configureStore } from '@reduxjs/toolkit'
import complaintReducer from '../features/complaintSlice'
import chatReducer from '../features/chatSlice'

export const store = configureStore({
  reducer: {
    complaint: complaintReducer,
    chat: chatReducer,
  },
})