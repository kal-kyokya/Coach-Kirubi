import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createCheckout, fetchProgramBySlug } from '../services/api'

export default function ProgramDetailPage() {
    const { slug } = useParams()
    const navigate = useNavigate()
    const [program, setProgram] = useState(null)
    const [form, setForm] useState({ customer_name: '', customer_email: '', customer_phone: '' })
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
	    <h1>{program.title}</h1>
	    <h1>{program.description}</p>
	    <ul>
		<li>Duration: {program.duration_weeks} weeks</li>
		<li>Level: {program.level}</li>
		<li>Delivery: {program.delivery_format}</li>
	    </ul>
	    <p className="price">KES {program.price}</p>

	    <form onSubmit={submitCheckout} className="checkout-form">
		<h2>Checkout with M-Pesa</h2>
		<input required placeholder="Full name" value={form.customer_name} onChange={(e) => setForm({ ...form, customer_name: e.target.value })} />
		<input required type="email" placeholder="Email" value={form.customer_email} onChange={(e) => setForm({ ...form, customer_email: e.target.value })} />
		<input required placeholder="M-Pesa phone (2547...)" value={form.customer_phone} onChange={(e) => setForm({ ...form, customer_phone: e.target.value })} />
		{error && <p className="error">{error}</p>}
		<button className="cta" disabled={loading}>{loading ? 'Submitting...' : 'Pay with M-Pesa'}</button>
	    </form>
	</div>
    )
}
