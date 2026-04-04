import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { fetchOrderStatus } from '../services/api'

export default function CheckoutStatusPage() {
    const { orderId } = useParams()
    const [statusData, setStatusData] = useState(null)

    useEffect(() => {
	fetchOrderStatus(orderId).then(setStatusData)
    }, [orderId])

    if (!statusData) return <p className="page">Checking payment status...</p>

    return (
	<div className="page status-page">
	    <section className="section-stack">
		<h1>Order Status</h1>
		<p>Track your latest payment and access update:</p>
	    </section>
	    <section className="status-card">
		<p><strong>Program:</strong> {statusData.program_title}</p>
		<p><strong>Status:</strong> {statusData.status}</p>
		<p><strong>Access:</strong> {statusData.access_granted ? 'Granted' : 'Pending payment confirmation'}</p>
		{statusData.mpesa_receipt_number && <p><strong>Receipt:</strong> {statusData.mpesa_receipt_number}</p>}
	    </section>
	</div>
    )
}
