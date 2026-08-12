import Login from './pages/login'
import Chatrooms from './pages/chatrooms'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


function App() {
    return (
        <Router>
            <Routes>
                <Route path="" element={<Login />} />
                <Route path="/chatrooms" element={<Chatrooms />} />
            </Routes>
        </Router>
    )
}

export default App
