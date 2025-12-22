import apiClient from "./axios"

export async function fetchTrendingComponents() {
  const response = await apiClient.get("/trending-components")
  return response.data
}
