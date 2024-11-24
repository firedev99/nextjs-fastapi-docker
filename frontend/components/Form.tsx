
"use client"
import React from "react";
import { firey } from "@/utils"

export default function Signup(){
  const [email, setEmail] = React.useState('')
  const [password, setPassword] = React.useState('')

  // create a new user email n password  
  async function handleRegistration() {
    const encryptedPassword = await firey.generateEncryption(password)
    const response = await fetch(`/api/v1/auth/signup`, {
      method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ email, password: encryptedPassword })
    })
    const data = await response.json()
    console.log(data)
  }

  return (
    <div className="flex flex-col mx-auto gap-2 max-w-96">
      <input className="border p-1.5 rounded-md indent-1" placeholder="random@example.com" type="email" name="email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input className="border p-1.5 rounded-md indent-1" placeholder="password" type="password" name="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button className="p-3 mt-3 rounded-lg bg-blue-500 text-white" onClick={handleRegistration}>Register User</button>
    </div>
  )
}