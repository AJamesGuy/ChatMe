import React from 'react'
import './login.css'

const Login = () => {
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

export default Log