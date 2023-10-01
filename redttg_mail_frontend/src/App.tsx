import './App.css';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import 'bootstrap/dist/css/bootstrap.min.css'
import { Container } from 'react-bootstrap';
import MailView from './pages/MailView';

function App() {
	return (
		<Container className="vh-100">
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/mail/:mailId" element={<MailView />} />
				<Route path="/login" element={<Login />} />
				{/* <Route path="/register" element={<Register />} /> */}
			</Routes>
		</Container>
	);
}

export default App;
