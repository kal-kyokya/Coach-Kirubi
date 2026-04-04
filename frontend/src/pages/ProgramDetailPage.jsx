import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createCheckout, fetchProgramBySlug } from '../services/api'

export default function ProgramDetailPage() {
    const { slug } = useParams()
    const navigate = useNavigate()
    const [program, setProgram] = useState(null)
    const [form, setForm] = useState({ customer_name: '', customer_email: '', customer_phone: '' })
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)

    useEffect(() => {
	fetchProgramBySlug(slug).then(setProgram)
    }, [slug])

    const submitCheckout = async (e) => {
	e.preventDefault()
	setError('')
	setLoading(true)
	try {
	    const response = await createCheckout({ ...form, program_slug: slug })
	    navigate(`/checkout/${response.order_id}`)
	} catch {
	    setError('We could not initiate payment. Please verify your details and try again.')
	} finally {
	    setLoading(false)
	}
    }

    if (!program) return <p className="page">Loading program...</p>

    return (
	<div className="page program-detail">
	    <section className="program-detail-header content-card">
		<h1>{program.title}</h1>
		<p>{program.description}</p>
		<ul>
		    <li>Duration: {program.duration_weeks} weeks</li>
		    <li>Level: {program.level}</li>
		    <li>Delivery: {program.delivery_format}</li>
		</ul>
		<p className="price">KES {program.price}</p>
	    </section>

	    <form onSubmit={submitCheckout} className="checkout-form">
		<h2>Checkout with M-Pesa</h2>
		<div className="form-field">
		    <label htmlFor="customer_name">Full name</label>
		    <input
			id="customer_name"
			required
			placeholder="Full name"
			value={form.customer_name}
			onChange={(e) => setForm({ ...form, customer_name: e.target.value })}
		    />
		</div>
		<div className="form-field">
		    <label htmlFor="customer_email">Email</label>
		    <input
			id="customer_email"
			required
			type="email"
			placeholder="Email"
			value={form.customer_email}
			onChange={(e) => setForm({ ...form, customer_email: e.target.value })}
		    />
		</div>
		<div className="form-field">
		    <label htmlFor="customer_phone">M-Pesa phone</label>
		    <input
			id="customer_phone"
			required
			placeholder="M-Pesa phone (2547...)"
			value={form.customer_phone}
			onChange={(e) => setForm({ ...form, customer_phone: e.target.value })}
		    />
		</div>
		{error && <p className="error">{error}</p>}
		<button className="button button-primary" disabled={loading}>{loading ? 'Submitting...' : 'Pay with M-Pesa'}</button>
	    </form>
	</div>
    )
}
