import { BrowserRouter, Routes, Route } from "react-router-dom"

import Landing from "./pages/Landing"
import Difficulty from "./pages/Difficulty"
import Category from "./pages/Category"
import UseCase from "./pages/UseCase"
import Configure from "./pages/Configure"
import Recommendation from "./pages/Recommendation"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/difficulty" element={<Difficulty />} />
        <Route path="/category" element={<Category />} />
        <Route path="/use-case" element={<UseCase />} />
        <Route path="/configure" element={<Configure />} />
        <Route path="/recommendation" element={<Recommendation />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
