import Header from "../components/layout/Header"
import Container from "../components/layout/Container"
import { useNavigate } from "react-router-dom"
import { useUserFlow } from "../context/UserFlowContext"

function Difficulty() {
  const navigate = useNavigate()
  const { setDifficulty } = useUserFlow()

  function handleSelect(level) {
    setDifficulty(level)
    navigate("/category")
  }

  return (
    <>
      <Header />
      <Container>
        <h1 className="text-2xl font-bold mb-6">
          Choose Your Experience Level
        </h1>

        <div className="space-y-4">
          <button
            onClick={() => handleSelect("beginner")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Beginner</h2>
            <p className="text-gray-600 text-sm">
              I don’t know PC parts. Recommend the best for me.
            </p>
          </button>

          <button
            onClick={() => handleSelect("intermediate")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Intermediate</h2>
            <p className="text-gray-600 text-sm">
              I know basic components like CPU, GPU, RAM.
            </p>
          </button>

          <button
            onClick={() => handleSelect("expert")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Expert</h2>
            <p className="text-gray-600 text-sm">
              I want a precise build tailored to my workload.
            </p>
          </button>
        </div>
      </Container>
    </>
  )
}

export default Difficulty
