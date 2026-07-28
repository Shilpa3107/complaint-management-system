import { createSlice } from '@reduxjs/toolkit'

const emptyForm = {
  complaint_source: '',
  customer_name: '',
  product_name: '',
  product_strength: '',
  batch_number: '',
  manufacturing_date: '',
  expiry_date: '',
  quantity_affected: '',
  quantity_unit: 'units',
  complaint_type: '',
  complaint_date: '',
  complaint_description: '',
  initial_severity: '',
  priority: '',
}

const emptyAiMeta = {
  missingFields: [],
  clarification: null,
  severityReasoning: null,
  suggestedNextAction: null,
  likelyCauses: [],
  rootCauseReasoning: null,
  isDuplicate: false,
  duplicateOf: [],
  duplicateReasoning: null,
}

const initialState = {
  form: emptyForm,
  aiMeta: emptyAiMeta,
  hasComplaintLoaded: false,
  requestStatus: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
  saveStatus: 'idle',
}

const complaintSlice = createSlice({
  name: 'complaint',
  initialState,
  reducers: {
    formReset(state) {
      state.form = emptyForm
      state.aiMeta = emptyAiMeta
      state.hasComplaintLoaded = false
      state.requestStatus = 'idle'
      state.saveStatus = 'idle'
    },
    requestStarted(state) {
      state.requestStatus = 'loading'
    },
    requestFailed(state) {
      state.requestStatus = 'failed'
    },
    newComplaintApplied(state, action) {
      // action.payload is the `extracted` object from the API response
      state.form = { ...state.form, ...action.payload, quantity_unit: action.payload.quantity_unit || 'units' }
      state.hasComplaintLoaded = true
      state.requestStatus = 'succeeded'
    },
    editApplied(state, action) {
      // action.payload is the `field_edits` diff object from the API response
      state.form = { ...state.form, ...action.payload }
      state.requestStatus = 'succeeded'
    },
    aiMetaUpdated(state, action) {
      const meta = action.payload
      state.aiMeta = {
        missingFields: meta.missing_fields || [],
        clarification: meta.clarification,
        severityReasoning: meta.severity_reasoning,
        suggestedNextAction: meta.suggested_next_action,
        likelyCauses: meta.likely_causes || [],
        rootCauseReasoning: meta.root_cause_reasoning,
        isDuplicate: meta.is_duplicate || false,
        duplicateOf: meta.duplicate_of || [],
        duplicateReasoning: meta.duplicate_reasoning,
      }
    },
    saveStarted(state) {
      state.saveStatus = 'loading'
    },
    saveSucceeded(state) {
      state.saveStatus = 'succeeded'
    },
    saveFailed(state) {
      state.saveStatus = 'failed'
    },
  },
})

export const {
  formReset,
  requestStarted,
  requestFailed,
  newComplaintApplied,
  editApplied,
  aiMetaUpdated,
  saveStarted,
  saveSucceeded,
  saveFailed,
} = complaintSlice.actions

export default complaintSlice.reducer