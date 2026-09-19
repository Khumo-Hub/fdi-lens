import { useEffect, useState } from "react";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import {
  getSummary,
  getTopDestinations,
  getTopSectors,
  getTrends,
} from "./services/api";

import "./App.css";


function App() {
  const [summary, setSummary] = useState(null);
  const [destinations, setDestinations] = useState([]);
  const [sectors, setSectors] = useState([]);
  const [trends, setTrends] = useState([]);

  const [trendMetric, setTrendMetric] = useState(
    "project_count"
  );

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  useEffect(() => {
    const loadDashboard = async () => {
      try {
        const [
          summaryData,
          destinationData,
          sectorData,
          trendData,
        ] = await Promise.all([
          getSummary(),
          getTopDestinations(),
          getTopSectors(),
          getTrends(),
        ]);

        setSummary(summaryData);
        setDestinations(destinationData);
        setSectors(sectorData);
        setTrends(trendData);

      } catch (err) {
        console.error(err);

        setError(
          "Could not load FDI data."
        );

      } finally {
        setLoading(false);
      }
    };

    loadDashboard();

  }, []);


  if (loading) {
    return (
      <div className="status">
        Loading FDI Lens...
      </div>
    );
  }


  if (error) {
    return (
      <div className="status">
        {error}
      </div>
    );
  }


  const formatCurrency = (value) => {
    return new Intl.NumberFormat(
      "en-US",
      {
        style: "currency",
        currency: "USD",
        notation: "compact",
        maximumFractionDigits: 1,
      }
    ).format(value);
  };


  const formatNumber = (value) => {
    return new Intl.NumberFormat(
      "en-US"
    ).format(value);
  };


  const getTrendLabel = () => {
    if (trendMetric === "total_capex_usd") {
      return "Capital Investment";
    }

    if (trendMetric === "total_jobs") {
      return "Jobs Created";
    }

    return "FDI Projects";
  };


  const formatTrendValue = (value) => {
    if (trendMetric === "total_capex_usd") {
      return formatCurrency(value);
    }

    return formatNumber(value);
  };


  return (
    <div className="app">

      <header className="header">

        <div>
          <h1>FDI Lens</h1>

          <p>
            Global Greenfield Investment
            Intelligence Platform
          </p>
        </div>

        <span className="data-badge">
          Synthetic Demo Data
        </span>

      </header>


      <main>

        <section className="dashboard-heading">

          <h2>
            Global Investment Overview
          </h2>

          <p>
            Explore investment activity,
            capital expenditure,
            employment creation and
            destination markets.
          </p>

        </section>


        <section className="kpi-grid">

          <div className="kpi-card">

            <div className="kpi-label">
              Total FDI Projects
            </div>

            <div className="kpi-value">
              {formatNumber(
                summary.total_projects
              )}
            </div>

            <div className="kpi-footer">
              Projects in database
            </div>

          </div>


          <div className="kpi-card">

            <div className="kpi-label">
              Capital Investment
            </div>

            <div className="kpi-value">
              {formatCurrency(
                summary.total_capex_usd
              )}
            </div>

            <div className="kpi-footer">
              Estimated total capex
            </div>

          </div>


          <div className="kpi-card">

            <div className="kpi-label">
              Jobs Created
            </div>

            <div className="kpi-value">
              {formatNumber(
                summary.total_jobs
              )}
            </div>

            <div className="kpi-footer">
              Estimated employment impact
            </div>

          </div>


          <div className="kpi-card">

            <div className="kpi-label">
              Countries Represented
            </div>

            <div className="kpi-value">
              {formatNumber(
                summary.countries_count
              )}
            </div>

            <div className="kpi-footer">
              Destination markets
            </div>

          </div>

        </section>


        <section className="charts-grid">

          <div className="chart-card">

            <div className="chart-header">

              <div>
                <h3>
                  Top FDI Destination Countries
                </h3>

                <p>
                  Ranked by number of
                  investment projects
                </p>
              </div>

            </div>


            <div className="chart-container">

              <ResponsiveContainer
                width="100%"
                height={400}
              >

                <BarChart
                  data={destinations}
                  layout="vertical"
                  margin={{
                    top: 10,
                    right: 30,
                    left: 20,
                    bottom: 10,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    type="number"
                    allowDecimals={false}
                  />

                  <YAxis
                    dataKey="country"
                    type="category"
                    width={60}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="project_count"
                    name="FDI Projects"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>


          <div className="chart-card">

            <div className="chart-header">

              <div>
                <h3>
                  Top FDI Sectors
                </h3>

                <p>
                  Ranked by total
                  capital investment
                </p>
              </div>

            </div>


            <div className="chart-container">

              <ResponsiveContainer
                width="100%"
                height={400}
              >

                <BarChart
                  data={sectors}
                  layout="vertical"
                  margin={{
                    top: 10,
                    right: 30,
                    left: 50,
                    bottom: 10,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    type="number"
                    tickFormatter={(value) =>
                      `$${(
                        value / 1_000_000_000
                      ).toFixed(0)}B`
                    }
                  />

                  <YAxis
                    dataKey="sector"
                    type="category"
                    width={125}
                  />

                  <Tooltip
                    formatter={(value) => [
                      formatCurrency(value),
                      "Capital Investment",
                    ]}
                  />

                  <Bar
                    dataKey="total_capex_usd"
                    name="Capital Investment"
                  />

                </BarChart>

              </ResponsiveContainer>

            </div>

          </div>

        </section>


        <section className="chart-card trend-card">

          <div className="chart-header">

            <div>
              <h3>
                Monthly FDI Investment Trend
              </h3>

              <p>
                Track investment activity
                over time
              </p>
            </div>


            <div className="trend-controls">

              <button
                className={
                  trendMetric === "project_count"
                    ? "trend-button active"
                    : "trend-button"
                }
                onClick={() =>
                  setTrendMetric(
                    "project_count"
                  )
                }
              >
                Projects
              </button>


              <button
                className={
                  trendMetric === "total_capex_usd"
                    ? "trend-button active"
                    : "trend-button"
                }
                onClick={() =>
                  setTrendMetric(
                    "total_capex_usd"
                  )
                }
              >
                Capex
              </button>


              <button
                className={
                  trendMetric === "total_jobs"
                    ? "trend-button active"
                    : "trend-button"
                }
                onClick={() =>
                  setTrendMetric(
                    "total_jobs"
                  )
                }
              >
                Jobs
              </button>

            </div>

          </div>


          <div className="trend-chart-container">

            <ResponsiveContainer
              width="100%"
              height={420}
            >

              <LineChart
                data={trends}
                margin={{
                  top: 15,
                  right: 30,
                  left: 20,
                  bottom: 15,
                }}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="month"
                />

                <YAxis
                  tickFormatter={(value) => {
                    if (
                      trendMetric ===
                      "total_capex_usd"
                    ) {
                      return `$${(
                        value /
                        1_000_000_000
                      ).toFixed(0)}B`;
                    }

                    if (
                      trendMetric ===
                      "total_jobs"
                    ) {
                      return `${(
                        value / 1000
                      ).toFixed(0)}K`;
                    }

                    return value;
                  }}
                />

                <Tooltip
                  formatter={(value) => [
                    formatTrendValue(value),
                    getTrendLabel(),
                  ]}
                />

                <Line
                  type="monotone"
                  dataKey={trendMetric}
                  name={getTrendLabel()}
                  strokeWidth={3}
                  dot={{
                    r: 3,
                  }}
                  activeDot={{
                    r: 6,
                  }}
                />

              </LineChart>

            </ResponsiveContainer>

          </div>

        </section>

      </main>

    </div>
  );
}


export default App;