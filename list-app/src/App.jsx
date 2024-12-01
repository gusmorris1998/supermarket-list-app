import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Section from './Section'

function App() {
  return (
    <>
      <Section heading="Day" initialItems={["Bread", "Milk"]}/>
      <Section heading="Week" initialItems={["Soap", "Soda", "Tomato Sauce"]}/>
      <Section heading="Month" initialItems={["Shampoo", "Detergent"]}/>
    </>
  )
}

export default App
