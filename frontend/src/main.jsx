import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App"
import "./index.css"
import { UserFlowProvider } from "./context/UserFlowContext"

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <UserFlowProvider>
      <App />
    </UserFlowProvider>
  </React.StrictMode>
)
