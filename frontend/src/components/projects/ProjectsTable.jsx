import { useEffect, useState } from "react";

import {
  getProjects,
} from "../../services/api";


function ProjectsTable() {

  const [projects, setProjects] = useState([]);
  const [total, setTotal] = useState(0);

  const [page, setPage] = useState(1);
  const [pageSize] = useState(10);

  const [destination, setDestination] =
    useState("");

  const [sector, setSector] =
    useState("");

  const [company, setCompany] =
    useState("");

  const [sortBy, setSortBy] =
    useState("announcement_date");

  const [sortOrder, setSortOrder] =
    useState("desc");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);


  const loadProjects = async (
    overrides = {}
  ) => {

    try {

      setLoading(true);
      setError(null);


      const params = {
        page:
          overrides.page ??
          page,

        page_size:
          overrides.page_size ??
          pageSize,

        sort_by:
          overrides.sort_by ??
          sortBy,

        sort_order:
          overrides.sort_order ??
          sortOrder,
      };


      const destinationValue =
        overrides.destination_country !== undefined
          ? overrides.destination_country
          : destination.trim();


      const sectorValue =
        overrides.sector !== undefined
          ? overrides.sector
          : sector.trim();


      const companyValue =
        overrides.company_name !== undefined
          ? overrides.company_name
          : company.trim();


      if (destinationValue) {

        params.destination_country =
          destinationValue;

      }


      if (sectorValue) {

        params.sector =
          sectorValue;

      }


      if (companyValue) {

        params.company_name =
          companyValue;

      }


      const data =
        await getProjects(params);


      setProjects(data.items);
      setTotal(data.total);

    } catch (err) {

      console.error(err);

      setError(
        "Could not load investment projects."
      );

    } finally {

      setLoading(false);
    }
  };


  useEffect(() => {

    loadProjects();

  }, [
    page,
    sortBy,
    sortOrder,
  ]);


  const handleSearch = async (
    event
  ) => {

    event.preventDefault();

    setPage(1);

    await loadProjects({
      page: 1,
    });
  };


  const handleClear = async () => {

    setDestination("");
    setSector("");
    setCompany("");

    setPage(1);

    setSortBy(
      "announcement_date"
    );

    setSortOrder(
      "desc"
    );


    await loadProjects({
      page: 1,
      sort_by:
        "announcement_date",
      sort_order:
        "desc",
      destination_country:
        "",
      sector:
        "",
      company_name:
        "",
    });
  };


  const totalPages = Math.max(
    1,
    Math.ceil(
      total / pageSize
    )
  );


  const formatCurrency = (
    value
  ) => {

    if (
      value === null ||
      value === undefined
    ) {
      return "—";
    }


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


  const formatNumber = (
    value
  ) => {

    if (
      value === null ||
      value === undefined
    ) {
      return "—";
    }


    return new Intl.NumberFormat(
      "en-US"
    ).format(value);
  };


  return (

    <section className="projects-section">

      <div className="projects-heading">

        <div>

          <h2>
            Investment Projects
          </h2>

          <p>
            Search, filter and explore
            individual FDI projects.
          </p>

        </div>


        <div className="project-count">

          {formatNumber(total)}
          {" "}
          projects

        </div>

      </div>


      <form
        className="project-filters"
        onSubmit={handleSearch}
      >

        <div className="filter-field">

          <label>
            Destination
          </label>

          <input
            type="text"
            placeholder="e.g. ZAF"
            value={destination}
            onChange={(event) =>
              setDestination(
                event.target.value
              )
            }
          />

        </div>


        <div className="filter-field">

          <label>
            Sector
          </label>

          <input
            type="text"
            placeholder="e.g. Renewable Energy"
            value={sector}
            onChange={(event) =>
              setSector(
                event.target.value
              )
            }
          />

        </div>


        <div className="filter-field">

          <label>
            Company
          </label>

          <input
            type="text"
            placeholder="Search company"
            value={company}
            onChange={(event) =>
              setCompany(
                event.target.value
              )
            }
          />

        </div>


        <div className="filter-field">

          <label>
            Sort by
          </label>

          <select
            value={sortBy}
            onChange={(event) => {

              setSortBy(
                event.target.value
              );

              setPage(1);
            }}
          >

            <option
              value="announcement_date"
            >
              Announcement Date
            </option>

            <option
              value="capex_usd"
            >
              Capital Investment
            </option>

            <option
              value="jobs_created"
            >
              Jobs Created
            </option>

            <option
              value="company"
            >
              Company
            </option>

            <option
              value="sector"
            >
              Sector
            </option>

          </select>

        </div>


        <div className="filter-field">

          <label>
            Order
          </label>

          <select
            value={sortOrder}
            onChange={(event) => {

              setSortOrder(
                event.target.value
              );

              setPage(1);
            }}
          >

            <option value="desc">
              Descending
            </option>

            <option value="asc">
              Ascending
            </option>

          </select>

        </div>


        <div className="filter-actions">

          <button
            type="submit"
            className="search-button"
          >
            Search
          </button>

          <button
            type="button"
            className="clear-button"
            onClick={handleClear}
          >
            Clear
          </button>

        </div>

      </form>


      {error && (

        <div className="table-message">
          {error}
        </div>

      )}


      {loading ? (

        <div className="table-message">
          Loading projects...
        </div>

      ) : (

        <div className="table-wrapper">

          <table className="projects-table">

            <thead>

              <tr>

                <th>
                  Company
                </th>

                <th>
                  Source
                </th>

                <th>
                  Destination
                </th>

                <th>
                  Sector
                </th>

                <th>
                  Type
                </th>

                <th>
                  Capex
                </th>

                <th>
                  Jobs
                </th>

                <th>
                  Date
                </th>

                <th>
                  Status
                </th>

              </tr>

            </thead>


            <tbody>

              {projects.map(
                (project) => (

                  <tr
                    key={project.id}
                  >

                    <td
                      className="company-cell"
                    >
                      {project.company}
                    </td>

                    <td>
                      {
                        project
                          .source_country
                      }
                    </td>

                    <td>
                      {
                        project
                          .destination_country
                      }
                    </td>

                    <td>
                      {
                        project.sector
                      }
                    </td>

                    <td>
                      {
                        project
                          .project_type
                      }
                    </td>

                    <td>
                      {formatCurrency(
                        project.capex_usd
                      )}
                    </td>

                    <td>
                      {formatNumber(
                        project.jobs_created
                      )}
                    </td>

                    <td>
                      {
                        project
                          .announcement_date
                      }
                    </td>

                    <td>

                      <span
                        className={
                          `status-badge ${
                            project.status
                          }`
                        }
                      >

                        {
                          project.status
                        }

                      </span>

                    </td>

                  </tr>

                )
              )}

            </tbody>

          </table>

        </div>

      )}


      <div className="pagination">

        <button
          disabled={
            page === 1 ||
            loading
          }
          onClick={() =>
            setPage(
              (current) =>
                current - 1
            )
          }
        >
          Previous
        </button>


        <span>

          Page {page}
          {" "}
          of
          {" "}
          {totalPages}

        </span>


        <button
          disabled={
            page >= totalPages ||
            loading
          }
          onClick={() =>
            setPage(
              (current) =>
                current + 1
            )
          }
        >
          Next
        </button>

      </div>

    </section>
  );
}


export default ProjectsTable;