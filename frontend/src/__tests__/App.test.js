import React from "react";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import { MemoryRouter } from "react-router-dom";
import App from "../App";

jest.mock("../pages/HomePage", () => () => <div>HomePage</div>);
jest.mock("../pages/ForecastPage", () => () => <div>ForecastPage</div>);
jest.mock("../pages/ClimateAnalysisPage", () => () => <div>ClimateAnalysisPage</div>);
jest.mock("../pages/CropRecommendationPage", () => () => <div>CropRecommendationPage</div>);
jest.mock("../pages/DiseaseRiskPage", () => () => <div>DiseaseRiskPage</div>);
jest.mock("../pages/PredictionPage", () => () => <div>PredictionPage</div>);
jest.mock("../pages/AdminPage", () => () => <div>AdminPage</div>);
jest.mock("../pages/ReportsPage", () => () => <div>ReportsPage</div>);

jest.mock("../components/layout/Layout", () => ({ children }) => (
  <div data-testid="layout">{children}</div>
));

describe("App Component", () => {
  test("renders without crashing", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByTestId("layout")).toBeInTheDocument();
  });

  test("renders HomePage on root route", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("HomePage")).toBeInTheDocument();
  });

  test("renders ForecastPage on /forecast route", () => {
    render(
      <MemoryRouter initialEntries={["/forecast"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("ForecastPage")).toBeInTheDocument();
  });

  test("renders ClimateAnalysisPage on /climate-analysis route", () => {
    render(
      <MemoryRouter initialEntries={["/climate-analysis"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("ClimateAnalysisPage")).toBeInTheDocument();
  });

  test("renders CropRecommendationPage on /recommendations route", () => {
    render(
      <MemoryRouter initialEntries={["/recommendations"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("CropRecommendationPage")).toBeInTheDocument();
  });

  test("renders DiseaseRiskPage on /disease-risk route", () => {
    render(
      <MemoryRouter initialEntries={["/disease-risk"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("DiseaseRiskPage")).toBeInTheDocument();
  });

  test("renders PredictionPage on /predict route", () => {
    render(
      <MemoryRouter initialEntries={["/predict"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("PredictionPage")).toBeInTheDocument();
  });

  test("renders AdminPage on /admin route", () => {
    render(
      <MemoryRouter initialEntries={["/admin"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("AdminPage")).toBeInTheDocument();
  });

  test("renders ReportsPage on /reports route", () => {
    render(
      <MemoryRouter initialEntries={["/reports"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("ReportsPage")).toBeInTheDocument();
  });

  test("redirects unknown routes to home", () => {
    render(
      <MemoryRouter initialEntries={["/unknown"]}>
        <App />
      </MemoryRouter>
    );
    expect(screen.getByText("HomePage")).toBeInTheDocument();
  });

  test("renders ToastContainer", () => {
    render(
      <MemoryRouter initialEntries={["/"]}>
        <App />
      </MemoryRouter>
    );
    const toastContainer = document.querySelector(".Toastify");
    expect(toastContainer).toBeInTheDocument();
  });
});
