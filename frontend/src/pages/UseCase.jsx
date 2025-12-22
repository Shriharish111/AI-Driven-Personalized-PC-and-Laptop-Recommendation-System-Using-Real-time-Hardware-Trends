import { useState } from "react"
import Header from "../components/layout/Header"
import Container from "../components/layout/Container"
import { useNavigate } from "react-router-dom"
import { useUserFlow } from "../context/UserFlowContext"

function UseCase() {
  const navigate = useNavigate()
  const {
    setUseCase,
    setSubUseCase
  } = useUserFlow()

  const [showDevOptions, setShowDevOptions] = useState(false)

  function handlePrimarySelect(type) {
    setUseCase(type)
    setSubUseCase(null)

    if (type === "developing") {
      setShowDevOptions(true)
    } else {
      navigate("/configure")
    }
  }

  function handleDevSelect(subType) {
    setSubUseCase(subType)
    navigate("/configure")
  }

  return (
    <>
      <Header />
      <Container>
        <h1 className="text-2xl font-bold mb-6">
          What will you mainly use it for?
        </h1>

        <div className="space-y-4 mb-6">
          <button
            onClick={() => handlePrimarySelect("gaming")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Gaming</h2>
            <p className="text-gray-600 text-sm">
              High FPS, GPU-focused performance.
            </p>
          </button>

          <button
            onClick={() => handlePrimarySelect("editing")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Editing</h2>
            <p className="text-gray-600 text-sm">
              Video editing, rendering, and creative work.
            </p>
          </button>

          <button
            onClick={() => handlePrimarySelect("developing")}
            className="w-full p-4 border rounded-lg text-left hover:bg-gray-50"
          >
            <h2 className="font-semibold">Developing</h2>
            <p className="text-gray-600 text-sm">
              Programming, AI, game dev, and server workloads.
            </p>
          </button>
        </div>

        {showDevOptions && (
          <>
            <h2 className="text-lg font-semibold mb-4">
              Select development type
            </h2>

            <div className="space-y-3">
              <button
                onClick={() => handleDevSelect("game_dev")}
                className="w-full p-3 border rounded-lg text-left hover:bg-gray-50"
              >
                Game Development
              </button>

              <button
                onClick={() => handleDevSelect("app_dev")}
                className="w-full p-3 border rounded-lg text-left hover:bg-gray-50"
              >
                App Development
              </button>

              <button
                onClick={() => handleDevSelect("ai_ml")}
                className="w-full p-3 border rounded-lg text-left hover:bg-gray-50"
              >
                AI / ML
              </button>

              <button
                onClick={() => handleDevSelect("3d_animation")}
                className="w-full p-3 border rounded-lg text-left hover:bg-gray-50"
              >
                3D Animation
              </button>

              <button
                onClick={() => handleDevSelect("server")}
                className="w-full p-3 border rounded-lg text-left hover:bg-gray-50"
              >
                Server / Backend
              </button>
            </div>
          </>
        )}
      </Container>
    </>
  )
}

export default UseCase
