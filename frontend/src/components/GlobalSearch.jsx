import {
  useEffect,
  useRef,
  useState,
} from "react";

import {
  searchGlobal,
} from "../services/api";

import ProjectDetailModal
  from "./projects/ProjectDetailModal";


function GlobalSearch() {

  const [query, setQuery] =
    useState("");

  const [results, setResults] =
    useState(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState(null);

  const [selectedProject, setSelectedProject] =
    useState(null);

  const inputRef = useRef(null);

  useEffect(() => {

    const handleShortcut = (event) => {

      if (
        event.ctrlKey &&
        event.key.toLowerCase() === "k"
      ) {
        event.preventDefault();
        inputRef.current?.focus();
      }
    };

    document.addEventListener(
      "keydown",
      handleShortcut
    );

    return () => {
      document.removeEventListener(
        "keydown",
        handleShortcut
      );
    };

  }, []);


  useEffect(() => {

    const trimmedQuery =
      query.trim();

    if (trimmedQuery.length < 2) {
      setResults(null);
      setError(null);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    const timer = setTimeout(
      async () => {

        try {

          const data =
            await searchGlobal(
              trimmedQuery
            );

          setResults(data);

        } catch (err) {

          console.error(err);

          setError(
            "Search is temporarily unavailable."
          );

        } finally {

          setLoading(false);
        }
      },
      300
    );

    return () => {
      clearTimeout(timer);
    };

  }, [query]);


  const hasResults =
    results &&
    (
      results.projects.length > 0 ||
      results.companies.length > 0 ||
      results.countries.length > 0 ||
      results.sectors.length > 0
    );


  const handleProjectClick =
    (project) => {

      setSelectedProject(project);
      setResults(null);
    };


  return (
    <>
      <div className="global-search">

        <div className="global-search-input-wrap">

          <span
            className="global-search-icon"
            aria-hidden="true"
          >
            ⌕
          </span>

          <input
            ref={inputRef}
            type="search"
            value={query}
            onChange={
              (event) =>
                setQuery(
                  event.target.value
                )
            }
            placeholder=
              "Search companies, projects, countries, sectors..."
            aria-label="Global search"
          />

          <span
            className="global-search-shortcut"
          >
            Ctrl + K
          </span>

        </div>


        {
          (
            loading ||
            error ||
            results
          ) && (
            <div
              className="global-search-results"
            >

              {
                loading && (
                  <div
                    className=
                      "global-search-message"
                  >
                    Searching...
                  </div>
                )
              }


              {
                error && (
                  <div
                    className=
                      "global-search-message error"
                  >
                    {error}
                  </div>
                )
              }


              {
                (
                  !loading &&
                  !error &&
                  results &&
                  !hasResults
                ) && (
                  <div
                    className=
                      "global-search-message"
                  >
                    No matching results.
                  </div>
                )
              }


              {
                !loading &&
                !error &&
                hasResults && (
                  <div
                    className=
                      "global-search-groups"
                  >

                    {
                      results.projects.length >
                      0 && (
                        <section
                          className=
                            "global-search-group"
                        >
                          <h4>
                            Projects
                          </h4>

                          {
                            results.projects.map(
                              (project) => (
                                <button
                                  key={
                                    project.id
                                  }
                                  type="button"
                                  className=
                                    "global-search-result"
                                  onClick={() =>
                                    handleProjectClick(
                                      project
                                    )
                                  }
                                >
                                  <strong>
                                    {
                                      project.company
                                    }
                                  </strong>

                                  <span>
                                    {
                                      project
                                        .source_country
                                    }
                                    {" → "}
                                    {
                                      project
                                        .destination_country
                                    }
                                    {" · "}
                                    {
                                      project.sector
                                    }
                                  </span>
                                </button>
                              )
                            )
                          }
                        </section>
                      )
                    }


                    {
                      results.companies.length >
                      0 && (
                        <section
                          className=
                            "global-search-group"
                        >
                          <h4>
                            Companies
                          </h4>

                          {
                            results.companies.map(
                              (company) => (
                                <div
                                  key={
                                    company.id
                                  }
                                  className=
                                    "global-search-result static"
                                >
                                  <strong>
                                    {
                                      company.name
                                    }
                                  </strong>

                                  <span>
                                    {
                                      company.industry ||
                                      "Industry not listed"
                                    }
                                    {
                                      company
                                        .headquarters_country
                                        ? ` · ${company.headquarters_country}`
                                        : ""
                                    }
                                  </span>
                                </div>
                              )
                            )
                          }
                        </section>
                      )
                    }


                    {
                      results.countries.length >
                      0 && (
                        <section
                          className=
                            "global-search-group"
                        >
                          <h4>
                            Countries
                          </h4>

                          {
                            results.countries.map(
                              (country) => (
                                <div
                                  key={
                                    country.code
                                  }
                                  className=
                                    "global-search-result static"
                                >
                                  <strong>
                                    {
                                      country.name
                                    }
                                  </strong>

                                  <span>
                                    {
                                      country.code
                                    }
                                    {
                                      country.region
                                        ? ` · ${country.region}`
                                        : ""
                                    }
                                  </span>
                                </div>
                              )
                            )
                          }
                        </section>
                      )
                    }


                    {
                      results.sectors.length >
                      0 && (
                        <section
                          className=
                            "global-search-group"
                        >
                          <h4>
                            Sectors
                          </h4>

                          {
                            results.sectors.map(
                              (sector) => (
                                <div
                                  key={
                                    sector.id
                                  }
                                  className=
                                    "global-search-result static"
                                >
                                  <strong>
                                    {
                                      sector.name
                                    }
                                  </strong>

                                  <span>
                                    {
                                      sector.cluster ||
                                      "Sector"
                                    }
                                  </span>
                                </div>
                              )
                            )
                          }
                        </section>
                      )
                    }

                  </div>
                )
              }

            </div>
          )
        }

      </div>


      {
        selectedProject && (
          <ProjectDetailModal
            project={
              selectedProject
            }
            onClose={() =>
              setSelectedProject(null)
            }
          />
        )
      }
    </>
  );
}


export default GlobalSearch;
