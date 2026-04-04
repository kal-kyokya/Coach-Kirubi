import { useEffect, useState } from 'react'
import ProgramCard from '../components/ProgramCard'
import { fetchPrograms } from '../services/api'

export default function CatalogPage() {
    const [programs, setPrograms] = useState([])

    useEffect(() => {
	fetchPrograms().then(setPrograms)
    }, [])

    return (
	<div className="page">
	    <section className="section-stack">
		<h1>Training Programs</h1>
		<p>Choose a structured plan built for measurable athletic progress</p>
	    </section>
	    <div className="grid">
		{programs.map((program) => <ProgramCard key={program.id} program={program} />)}
	    </div>
	</div>
    )
}
