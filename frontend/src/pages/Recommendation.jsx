import Header from "../components/layout/Header"
import Container from "../components/layout/Container"
import { useNavigate } from "react-router-dom"
import { useUserFlow } from "../context/UserFlowContext"

function Recommendation() {
  const navigate = useNavigate()
  const {
    difficulty,
    category,
    useCase,
    subUseCase,
    budget,
    preferences
  } = useUserFlow()

  function handleProceed() {
    // Phase 4 will replace this with API call
    alert("Recommendation engine will run in Phase 4")
  }

  return (
    <>
      <Header />
      <Container>
        <h1 className="text-2xl font-bold mb-6">
          Review Your Choices
        </h1>

        <div className="space-y-4 mb-8">
          <div>
            <strong>Experience Level:</strong> {difficulty}
          </div>

          <div>
            <strong>Category:</strong> {category}
          </div>

          <div>
            <strong>Use Case:</strong>{" "}
            {useCase === "developing" && subUseCase
              ? `${useCase} (${subUseCase})`
              : useCase}
          </div>

          <div>
            <strong>Budget:</strong> ₹{budget}
          </div>

          {(difficulty === "intermediate" || difficulty === "expert") && (
            <div>
              <strong>Component Preferences:</strong>
              <ul className="list-disc list-inside text-gray-700">
                {preferences.cpu && <li>CPU: {preferences.cpu}</li>}
                {preferences.gpu && <li>GPU: {preferences.gpu}</li>}
                {preferences.ram && <li>RAM: {preferences.ram}</li>}
                {preferences.storage && <li>Storage: {preferences.storage}</li>}
                {!preferences.cpu &&
                  !preferences.gpu &&
                  !preferences.ram &&
                  !preferences.storage && (
                    <li>No specific components selected</li>
                  )}
              </ul>
            </div>
          )}

          {difficulty === "expert" && preferences.notes && (
            <div>
              <strong>Advanced Notes:</strong>
              <p className="text-gray-700">{preferences.notes}</p>
            </div>
          )}
        </div>

        <div className="flex gap-4">
          <button
            onClick={() => navigate("/configure")}
            className="px-6 py-3 border rounded-lg"
          >
            Edit Choices
          </button>

          <button
            onClick={handleProceed}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg"
          >
            Get Recommendations
          </button>
        </div>
      </Container>
    </>
  )
}

export default Recommendation
