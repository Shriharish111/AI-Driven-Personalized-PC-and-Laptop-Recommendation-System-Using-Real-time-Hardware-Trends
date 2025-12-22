import { createContext, useContext, useState } from "react"

const UserFlowContext = createContext(null)

export function UserFlowProvider({ children }) {
  const [difficulty, setDifficulty] = useState(null)
  const [category, setCategory] = useState(null)
  const [useCase, setUseCase] = useState(null)
  const [subUseCase, setSubUseCase] = useState(null)
  const [budget, setBudget] = useState(null)

  const value = {
    difficulty,
    setDifficulty,
    category,
    setCategory,
    useCase,
    setUseCase,
    subUseCase,
    setSubUseCase,
    budget,
    setBudget
  }

  return (
    <UserFlowContext.Provider value={value}>
      {children}
    </UserFlowContext.Provider>
  )
}

export function useUserFlow() {
  return useContext(UserFlowContext)
}
