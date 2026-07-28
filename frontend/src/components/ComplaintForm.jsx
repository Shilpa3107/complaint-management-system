import { useSelector, useDispatch } from 'react-redux'
import axios from 'axios'
import { formReset, saveStarted, saveSucceeded, saveFailed } from '../features/complaintSlice'
import './ComplaintForm.css'

const API_BASE = 'http://127.0.0.1:8000'

function ComplaintForm() {
  const dispatch = useDispatch()
  const form = useSelector((state) => state.complaint.form)
  const aiMeta = useSelector((state) => state.complaint.aiMeta)
  const hasComplaintLoaded = useSelector((state) => state.complaint.hasComplaintLoaded)
  const saveStatus = useSelector((state) => state.complaint.saveStatus)

  const handleReset = () => dispatch(formReset())

  const handleSave = async () => {
    dispatch(saveStarted())
    try {
      const payload = {
        ...form,
        quantity_affected: form.quantity_affected === '' ? null : Number(form.quantity_affected),
        manufacturing_date: form.manufacturing_date || null,
        expiry_date: form.expiry_date || null,
        complaint_date: form.complaint_date || null,
      }
      await axios.post(`${API_BASE}/complaints/`, payload)
      dispatch(saveSucceeded())
    } catch (err) {
      console.error('Save failed:', err)
      dispatch(saveFailed())
    }
  }

  const displayValue = (val) => val || ''

  return (
    <div className="complaint-form">
      <div className="form-header">
        <div>
          <h1>Log Customer Complaint</h1>
          <p className="subtitle">API &amp; FDF Quality Assurance Module</p>
        </div>
        <span className="status-badge">{hasComplaintLoaded ? 'Pending Triage' : 'Awaiting Input'}</span>
      </div>
      <p className="readonly-hint">Fields are populated automatically by the AIVOA Copilot — describe or upload a complaint on the right to get started.</p>
      <hr />

      <section>
        <h3>1. Origin &amp; Customer Details</h3>
        <div className="field-row">
          <div className="field">
            <label>Complaint Source</label>
            <input readOnly value={displayValue(form.complaint_source)} placeholder="Awaiting AI extraction..." />
          </div>
          <div className="field">
            <label>Customer Name</label>
            <input readOnly value={displayValue(form.customer_name)} placeholder="Awaiting AI extraction..." />
          </div>
        </div>
      </section>

      <section>
        <h3>2. Product &amp; Batch Identification</h3>
        <div className="field-row">
          <div className="field">
            <label>Product Name</label>
            <input readOnly value={displayValue(form.product_name)} placeholder="Awaiting AI extraction..." />
          </div>
          <div className="field">
            <label>Product Strength/Grade</label>
            <input readOnly value={displayValue(form.product_strength)} placeholder="Awaiting AI extraction..." />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label>Batch/Lot Number</label>
            <input readOnly value={displayValue(form.batch_number)} placeholder="Awaiting AI extraction..." />
          </div>
          <div className="field">
            <label>Manufacturing Date</label>
            <input readOnly value={displayValue(form.manufacturing_date)} placeholder="dd-mm-yyyy" />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label>Expiry Date</label>
            <input readOnly value={displayValue(form.expiry_date)} placeholder="dd-mm-yyyy" />
          </div>
          <div className="field">
            <label>Quantity Affected</label>
            <div className="input-with-unit">
              <input readOnly value={displayValue(form.quantity_affected)} />
              <span className="unit">{form.quantity_unit || 'units'}</span>
            </div>
          </div>
        </div>
      </section>

      <section>
        <h3>3. Complaint Details</h3>
        <div className="field-row">
          <div className="field">
            <label>Complaint Type</label>
            <input readOnly value={displayValue(form.complaint_type)} placeholder="Awaiting AI extraction..." />
          </div>
          <div className="field">
            <label>Complaint Date</label>
            <input readOnly value={displayValue(form.complaint_date)} placeholder="dd-mm-yyyy" />
          </div>
        </div>
        <div className="field">
          <label>Detailed Complaint Description</label>
          <textarea readOnly rows={4} value={displayValue(form.complaint_description)} placeholder="Awaiting AI extraction..." />
        </div>
      </section>

      <section>
        <h3>4. Initial Assessment &amp; Priority</h3>
        <div className="field-row">
          <div className="field">
            <label>Initial Severity</label>
            <input readOnly value={displayValue(form.initial_severity)} placeholder="Awaiting AI extraction..." />
          </div>
          <div className="field">
            <label>Priority</label>
            <input readOnly value={displayValue(form.priority)} placeholder="Awaiting AI extraction..." />
          </div>
        </div>
      </section>

      {hasComplaintLoaded && (
        <section className="risk-assessment">
          <h3>🛡 AI Copilot Risk Assessment</h3>
          <div className="field-row">
            <div className="field">
              <label>Severity (Suggested)</label>
              <input readOnly value={displayValue(form.initial_severity)} />
            </div>
            <div className="field">
              <label>Suggested Next Action</label>
              <input readOnly value={displayValue(aiMeta.suggestedNextAction)} />
            </div>
          </div>
          <div className="field">
            <label>Initial Risk Assessment</label>
            <textarea readOnly rows={3} value={displayValue(aiMeta.severityReasoning)} />
          </div>
          {aiMeta.likelyCauses?.length > 0 && (
            <div className="field">
              <label>Likely Root Cause(s)</label>
              <ul className="cause-list">
                {aiMeta.likelyCauses.map((c, i) => <li key={i}>{c}</li>)}
              </ul>
            </div>
          )}
          {aiMeta.isDuplicate && (
            <div className="duplicate-warning">
              ⚠ This may be a duplicate of an existing complaint: {aiMeta.duplicateReasoning}
            </div>
          )}
        </section>
      )}

      <div className="form-actions">
        <button className="btn-secondary" onClick={handleReset}>Reset Form</button>
        <button className="btn-primary" onClick={handleSave} disabled={!hasComplaintLoaded || saveStatus === 'loading'}>
          {saveStatus === 'loading' ? 'Saving...' : saveStatus === 'succeeded' ? '✓ Saved' : 'Commit to QMS Ledger'}
        </button>
      </div>
      {saveStatus === 'failed' && (
        <p className="save-error">Save failed. Please check the backend connection and try again.</p>
      )}       
     
    </div>
  )
}

export default ComplaintForm