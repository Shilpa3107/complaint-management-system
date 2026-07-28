import { useState } from 'react'
import './ComplaintForm.css'

const initialFormState = {
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

function ComplaintForm() {
  const [form, setForm] = useState(initialFormState)

  const handleChange = (field) => (e) => {
    setForm({ ...form, [field]: e.target.value })
  }

  const handleReset = () => setForm(initialFormState)

  const handleSave = () => {
    console.log('Saving complaint:', form)
    // Real save logic comes in Phase 8
  }

  return (
    <div className="complaint-form">
      <div className="form-header">
        <div>
          <h1>Log Customer Complaint</h1>
          <p className="subtitle">API &amp; FDF Quality Assurance Module</p>
        </div>
        <span className="status-badge">Pending Triage</span>
      </div>
      <hr />

      <section>
        <h3>1. Origin &amp; Customer Details</h3>
        <div className="field-row">
          <div className="field">
            <label>Complaint Source</label>
            <input value={form.complaint_source} onChange={handleChange('complaint_source')} placeholder="e.g. Email, Phone, Portal" />
          </div>
          <div className="field">
            <label>Customer Name</label>
            <input value={form.customer_name} onChange={handleChange('customer_name')} />
          </div>
        </div>
      </section>

      <section>
        <h3>2. Product &amp; Batch Identification</h3>
        <div className="field-row">
          <div className="field">
            <label>Product Name</label>
            <input value={form.product_name} onChange={handleChange('product_name')} />
          </div>
          <div className="field">
            <label>Product Strength/Grade</label>
            <input value={form.product_strength} onChange={handleChange('product_strength')} />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label>Batch/Lot Number</label>
            <input value={form.batch_number} onChange={handleChange('batch_number')} />
          </div>
          <div className="field">
            <label>Manufacturing Date</label>
            <input type="date" value={form.manufacturing_date} onChange={handleChange('manufacturing_date')} />
          </div>
        </div>
        <div className="field-row">
          <div className="field">
            <label>Expiry Date</label>
            <input type="date" value={form.expiry_date} onChange={handleChange('expiry_date')} />
          </div>
          <div className="field">
            <label>Quantity Affected</label>
            <div className="input-with-unit">
              <input type="number" value={form.quantity_affected} onChange={handleChange('quantity_affected')} />
              <span className="unit">{form.quantity_unit}</span>
            </div>
          </div>
        </div>
      </section>

      <section>
        <h3>3. Complaint Details</h3>
        <div className="field-row">
          <div className="field">
            <label>Complaint Type</label>
            <input value={form.complaint_type} onChange={handleChange('complaint_type')} />
          </div>
          <div className="field">
            <label>Complaint Date</label>
            <input type="date" value={form.complaint_date} onChange={handleChange('complaint_date')} />
          </div>
        </div>
        <div className="field">
          <label>Detailed Complaint Description</label>
          <textarea rows={4} value={form.complaint_description} onChange={handleChange('complaint_description')} />
        </div>
      </section>

      <section>
        <h3>4. Initial Assessment &amp; Priority</h3>
        <div className="field-row">
          <div className="field">
            <label>Initial Severity</label>
            <select value={form.initial_severity} onChange={handleChange('initial_severity')}>
              <option value="">Select...</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Critical">Critical</option>
            </select>
          </div>
          <div className="field">
            <label>Priority</label>
            <select value={form.priority} onChange={handleChange('priority')}>
              <option value="">Select...</option>
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
            </select>
          </div>
        </div>
      </section>

      <div className="form-actions">
        <button className="btn-secondary" onClick={handleReset}>Reset Form</button>
        <button className="btn-primary" onClick={handleSave}>Save Complaint</button>
      </div>
    </div>
  )
}

export default ComplaintForm