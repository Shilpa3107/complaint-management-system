import { createSlice } from '@reduxjs/toolkit'

const initialState = {
  form: {
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
  },
  aiMeta: {
    missingFields: [],
    clarification: null,
    severityReasoning: null,
    likelyCauses: [],
    rootCauseReasoning: null,
    isDuplicate: false,
    duplicateOf: [],
    duplicateReasoning: null,
  },
  extractionStatus: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
  saveStatus: 'idle',
}

const complaintSlice = createSlice({
  name: 'complaint',
  initialState,
  reducers: {
    fieldChanged(state, action) {
      const { field, value } = action.payload
      state.form[field] = value
    },
    formReset(state) {
      state.form = initialState.form
      state.aiMeta = initialState.aiMeta
      state.extractionStatus = 'idle'
      state.saveStatus = 'idle'
    },
    extractionStarted(state) {
      state.extractionStatus = 'loading'
    },
    extractionSucceeded(state, action) {
      const { extracted, ...meta } = action.payload
      state.form = { ...state.form, ...extracted }
      state.aiMeta = {
        missingFields: meta.missing_fields || [],
        clarification: meta.clarification,
        severityReasoning: meta.severity_reasoning,
        likelyCauses: meta.likely_causes || [],
        rootCauseReasoning: meta.root_cause_reasoning,
        isDuplicate: meta.is_duplicate || false,
        duplicateOf: meta.duplicate_of || [],
        duplicateReasoning: meta.duplicate_reasoning,
      }
      state.extractionStatus = 'succeeded'
    },
    extractionFailed(state) {
      state.extractionStatus = 'failed'
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
  fieldChanged,
  formReset,
  extractionStarted,
  extractionSucceeded,
  extractionFailed,
  saveStarted,
  saveSucceeded,
  saveFailed,
} = complaintSlice.actions

export default complaintSlice.reducer