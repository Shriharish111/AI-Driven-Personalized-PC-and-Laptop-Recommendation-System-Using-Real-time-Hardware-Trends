import { useEffect, useState } from "react"
import Header from "../components/layout/Header"
import Container from "../components/layout/Container"
import TrendingChart from "../components/charts/TrendingChart"
import { fetchTrendingComponents } from "../api/trending.api"
import { useNavigate } from "react-router-dom"

function Landing() {
  const [trendingData, setTrendingData] = useState([])
  const [updatedAt, setUpdatedAt] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(false)

  const navigate = useNavigate()

  useEffect(() => {
    async function loadTrending() {
      try {
        const data = await fetchTrendingComponents()
        setTrendingData(data.components)
        setUpdatedAt(data.updated_at)
      } catch (err) {
        setError(true)
      } finally {
        setLoading(false)
      }
    }

    loadTrending()
  }, [])

  return (
    <>
      <Header />
      <Container>
        {/* App Identity */}
        <h1 className="text-3xl font-bold mb-2">
          AI PC Recommendation System
        </h1>
        <p className="text-gray-600 mb-6">
          Get the best PC or laptop recommendations based on real-world usage
          and your needs.
        </p>

        {/* Trending Section */}
        <section className="mb-10 p-4 border rounded-lg bg-gray-50">
          <h2 className="text-xl font-semibold mb-4">
            Trending Components (Average PCs Today)
          </h2>

          {loading && (
            <div className="text-gray-500">
              Analyzing current hardware trends…
            </div>
          )}


          {!loading && error && (
            <div className="text-gray-500">
              Unable to load trending hardware data right now.
              <br />
              You can still continue and get recommendations.
            </div>
        )}

          {!loading && !error && (
            <>
              <TrendingChart data={trendingData} />
              {updatedAt && (
                <p className="text-sm text-gray-500 mt-2">
                  Last updated: {updatedAt}
                </p>
              )}
            </>
          )}
        </section>

        {/* Entry Point */}
        <button
          onClick={() => navigate("/difficulty")}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg"
        >
          Get Started
        </button>
      </Container>
    </>
  )
}

export default Landing
