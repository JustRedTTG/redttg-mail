import './App.scss';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import Navbar from './components/Navbar';
import { Container } from 'react-bootstrap';
import MailView from './pages/MailView';
import User from './interfaces/User';
import { useEffect, useState } from 'react';
import { getUser } from './controllers/User';
import Account from './pages/Account';

function App() {
	const [user, setUser] = useState<User | undefined | null>(undefined);

	useEffect(() => {
		getUser().then(setUser).catch(() => setUser(null));
	}, [])

	return (
		<Container fluid>
			<Navbar user={user} className="mx-3" />
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/mail/:mailId" element={<MailView />} />
				<Route path="/login" element={<Login />} />
				<Route path="/account" element={<Account currentUser={user} onUpdate={setUser}/>} />
				<Route path="/account/:mode" element={<Account currentUser={user} onUpdate={setUser}/>} />
				{/* <Route path="/register" element={<Register />} /> */}
			</Routes>
		</Container>
	);
}

export default App;
