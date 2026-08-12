import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { useNavigate } from 'react-router-dom'
import { loginUser } from '../services/api'
import './login.css'

const Login = () => {

    const handleLogin = (e) => {
        e.preventDefault();
        // Implement login logic here

    }


  return (<>
  <body>
    <div className="login-container">
      <h1>ChatMe</h1>
      <form>
        <input type="text" placeholder="Username" />
        <input type="password" placeholder="Password" />
        <div>
          <button type="submit" className="login-button">Login</button>
          <button type="button" className="signup-button">Sign Up</button>
        </div>
      </form>
    </div>
  </body>
  </>
  )
}

export default Login