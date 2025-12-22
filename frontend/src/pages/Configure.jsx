import Header from "../components/layout/Header"
import Container from "../components/layout/Container"
import { useNavigate } from "react-router-dom"
import { useUserFlow } from "../context/UserFlowContext"

function Configure() {
  const navigate = useNavigate()
  const {
    difficulty,
    budget,
    setBudget,
    preferences,
    setPreferences
  } = useUserFlow()

  function handleChange(field, value) {
    setPreferences(prev => ({
      ...prev,
      [field]: value
    }))
  }

  function handleContinue() {
    navigate("/recommendation")
  }

  return (
    <>
      <Header />
      <Container>
        <h1 className="text-2xl font-bold mb-6">
          Configuration
        </h1>

        {/* Budget (for all users) */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">
            Budget (₹)
          </label>
          <input
            type="number"
            value={budget || ""}
            onChange={(e) => setBudget(Number(e.target.value))}
            placeholder="e.g. 80000"
            className="w-full p-3 border rounded-lg"
          />
        </div>

        {/* Beginner */}
        {difficulty === "beginner" && (
          <p className="text-gray-600 mb-6">
            You don’t need to select any components.  
            We’ll recommend the best configuration for you.
          </p>
        )}

        {/* Intermediate & Expert */}
        {(difficulty === "intermediate" || difficulty === "expert") && (
          <>
            <h2 className="text-lg font-semibold mb-4">
              Component Preferences (Optional)
            </h2>

            <div className="space-y-4 mb-6">
              <input
                type="text"
                placeholder="Preferred CPU (e.g. Ryzen 5, i5)"
                className="w-full p-3 border rounded-lg"
                value={preferences.cpu}
                onChange={(e) => handleChange("cpu", e.target.value)}
              />

              <input
                type="text"
                placeholder="Preferred GPU (e.g. RTX 3060)"
                className="w-full p-3 border rounded-lg"
                value={preferences.gpu}
                onChange={(e) => handleChange("gpu", e.target.value)}
              />

              <input
                type="text"
                placeholder="RAM (e.g. 16GB)"
                className="w-full p-3 border rounded-lg"
                value={preferences.ram}
                onChange={(e) => handleChange("ram", e.target.value)}
              />

              <input
                type="text"
                placeholder="Storage (e.g. 1TB SSD)"
                className="w-full p-3 border rounded-lg"
                value={preferences.storage}
                onChange={(e) => handleChange("storage", e.target.value)}
              />
            </div>
          </>
        )}

        {/* Expert-only */}
        {difficulty === "expert" && (
          <>
            <h2 className="text-lg font-semibold mb-4">
              Advanced Notes (Optional)
            </h2>

            <textarea
              placeholder="Any specific requirement? (CUDA, low noise, future upgrade, etc.)"
              className="w-full p-3 border rounded-lg mb-6"
              rows={4}
              value={preferences.notes}
              onChange={(e) => handleChange("notes", e.target.value)}
            />
          </>
        )}

        <button
          onClick={handleContinue}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg"
        >
          Continue to Recommendations
        </button>
      </Container>
    </>
  )
}

export default Configure
