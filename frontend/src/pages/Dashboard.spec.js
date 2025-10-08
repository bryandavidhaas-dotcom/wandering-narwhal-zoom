import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import Dashboard from "./Dashboard";

describe("Dashboard", () => {
  it("should render the dashboard", () => {
    render(
      <Router>
        <Dashboard />
      </Router>
    );

    const title = screen.getByText("Your Career Recommendations");
    expect(title).toBeInTheDocument();
  });
});