import { Link } from 'react-router-dom'

export default function ProgramCard({ program }) {
    return (
	<article className="program-card">
	    <h3>{program.title}</h3>
	    <p>{program.short_description}</p>
	    <div className="meta">
		<span>{program.duration_weeks} weeks</span>
		<span>{program.level}</span>
	    </div>
	    <strong>KES {program.price}</strong>
	    <Link to={`/programs/{program.slug`} className="cta">View program</Link>
	</article>
    )
}
