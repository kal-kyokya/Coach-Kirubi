import { Link, Route, Routes } from 'react-router-dom'
import HomePage from './pages/HomePage'
import CatalogPage from './pages/CatalogPage'
import ProgramDetailPage from './pages/ProgramDetailPage'
import CheckoutStatusPage from './pages/CheckoutStatusPage'

function App() {
    return (
	<div className="app-shell">
	    <header className="topbar">
		<div className="topbar-content">
		    <Link to="/" className="brand">
			<img src='/keruvim-logo.jpg'
			     alt='Logo of the Futtech Company'
			/>
			Coach Kirubi
		    </Link>
		    <nav>
			<Link to="/programs">Programs</Link>
			<a href="#contact">Contact</a>
		    </nav>
		</div>
	    </header>
	    <main>
		<Routes>
		    <Route path="/" element={<HomePage />} />
		    <Route path="/programs" element={<CatalogPage />} />
		    <Route path="/programs/:slug" element={<ProgramDetailPage />} />
		    <Route path="/checkout/:orderId" element={<CheckoutStatusPage />} />
		</Routes>
	    </main>
	    <footer className="footer" id="contact">
		<p>Contact Coach Kirubi: coach@keruvimperformance.com | +254700000000</p>
		<p>© {new Date().getFullYear()} Keruvim Performance</p>
	    </footer>
	</div>
    )
}

export default App
