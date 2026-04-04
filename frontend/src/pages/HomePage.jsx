import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import ProgramCard from '../components/ProgramCard'
import { fetchHome, fetchPrograms } from '../services/api'

export default function HomePage() {
    const [home, setHome] = useState(null)
    const [programs, setPrograms] = useState([])

    useEffect(() => {
	Promise.all([fetchHome(), fetchPrograms()]).then(([homeData, programData]) => {
	    setHome(homeData)
	    setPrograms(programData.filter((p) => p.is_featured).slice(0, 3))
	})
    }, [])

    return (
	<div className="page">
	    <section className="hero">
		<h1>{home?.hero_title || 'Train with purpose'}</h1>
		<p>{home?.hero_subtitle}</p>
		<Link className="cta" to="/programs">{home?.primary_cat_label || 'Shop Programs'}</Link>
	    </section>
	    <section className="section-stack">
		<h2>Featured Programs</h2>
		<div className="grid">
		    {programs.map((program) => <ProgramCard key={program.id} program={program} />)}
		</div>
	    </section>
	</div>
    )
}
