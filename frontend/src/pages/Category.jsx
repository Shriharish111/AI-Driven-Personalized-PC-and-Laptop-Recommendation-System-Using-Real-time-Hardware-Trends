import Header from "../components/layout/Header"
import Container from "../components/layout/Container"
import { useNavigate } from "react-router-dom"
import { useUserFlow } from "../context/UserFlowContext"

function Category() {
  const navigate = useNavigate()
  const { setCategory } = useUserFlow()

  function handleSelect(type) {
    setCategory(type)
    navigate("/use-case")
  }

  return (
    <>
      <Header />
      <Container>
        <h1 className="text-2xl font-bold mb-6">
          What are you planning to buy?
        </h1>

        <div className="space-y-4">
          <button
            onClick={() => handleSelect("pc")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">PC (Desktop)</h2>
            <p className="text-gray-600 text-sm">
              Best performance, upgrade-friendly, long-term value.
            </p>
          </button>

          <button
            onClick={() => handleSelect("laptop")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Laptop</h2>
            <p className="text-gray-600 text-sm">
              Portable, compact, and ready to use anywhere.
            </p>
          </button>
        </div>
      </Container>
    </>
  )
}

export default Category
