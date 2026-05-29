import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import Layout from './components/layout/Layout';
import HomePage from './pages/HomePage';
import ForecastPage from './pages/ForecastPage';
import ClimateAnalysisPage from './pages/ClimateAnalysisPage';
import CropRecommendationPage from './pages/CropRecommendationPage';
import DiseaseRiskPage from './pages/DiseaseRiskPage';
import PredictionPage from './pages/PredictionPage';
import AdminPage from './pages/AdminPage';
import ReportsPage from './pages/ReportsPage';

function App() {
  return (
    <>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/forecast" element={<ForecastPage />} />
          <Route path="/climate-analysis" element={<ClimateAnalysisPage />} />
          <Route path="/recommendations" element={<CropRecommendationPage />} />
          <Route path="/disease-risk" element={<DiseaseRiskPage />} />
          <Route path="/predict" element={<PredictionPage />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
      <ToastContainer
        position="top-right"
        autoClose={3000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
        theme="light"
      />
    </>
  );
}

export default App;
