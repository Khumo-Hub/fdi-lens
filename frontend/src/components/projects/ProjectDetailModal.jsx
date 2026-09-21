import { useEffect } from "react";


function ProjectDetailModal({
  project,
  onClose,
}) {

  useEffect(() => {

    const handleEscape = (event) => {

      if (event.key === "Escape") {
        onClose();
      }
    };


    document.addEventListener(
      "keydown",
      handleEscape
    );


    return () => {

      document.removeEventListener(
        "keydown",
        handleEscape
      );
    };

  }, [onClose]);


  if (!project) {
    return null;
  }


  const formatCurrency = (value) => {

    if (
      value === null ||
      value === undefined
    ) {
      return "Not available";
    }


    return new Intl.NumberFormat(
      "en-US",
      {
        style: "currency",
        currency: "USD",
        maximumFractionDigits: 0,
      }
    ).format(value);
  };


  const formatNumber = (value) => {

    if (
      value === null ||
      value === undefined
    ) {
      return "Not available";
    }


    return new Intl.NumberFormat(
      "en-US"
    ).format(value);
  };


  const handleOverlayClick = (
    event
  ) => {

    if (
      event.target ===
      event.currentTarget
    ) {
      onClose();
    }
  };


  return (

    <div
      className="modal-overlay"
      onClick={handleOverlayClick}
    >

      <div
        className="project-modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="project-modal-title"
      >

        <div className="modal-header">

          <div>

            <div className="modal-eyebrow">
              FDI Project
            </div>

            <h2 id="project-modal-title">
              {project.company}
            </h2>

            <p>
              {project.source_country}
              {" → "}
              {project.destination_country}
            </p>

          </div>


          <button
            type="button"
            className="modal-close-button"
            onClick={onClose}
            aria-label="Close project details"
          >
            ×
          </button>

        </div>


        <div className="modal-status-row">

          <span
            className={
              `status-badge ${
                project.status
              }`
            }
          >
            {project.status}
          </span>

          <span className="modal-project-type">
            {project.project_type}
          </span>

        </div>


        <div className="modal-details-grid">

          <div className="modal-detail">

            <span className="detail-label">
              Company
            </span>

            <span className="detail-value">
              {project.company}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Sector
            </span>

            <span className="detail-value">
              {project.sector}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Source Country
            </span>

            <span className="detail-value">
              {project.source_country}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Destination Country
            </span>

            <span className="detail-value">
              {project.destination_country}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Capital Investment
            </span>

            <span className="detail-value">
              {formatCurrency(
                project.capex_usd
              )}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Jobs Created
            </span>

            <span className="detail-value">
              {formatNumber(
                project.jobs_created
              )}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Project Type
            </span>

            <span className="detail-value">
              {project.project_type}
            </span>

          </div>


          <div className="modal-detail">

            <span className="detail-label">
              Announcement Date
            </span>

            <span className="detail-value">
              {
                project
                  .announcement_date
              }
            </span>

          </div>

        </div>


        <div className="modal-description">

          <h3>
            Project Description
          </h3>

          <p>
            {
              project.description ||
              "No project description is available."
            }
          </p>

        </div>


        <div className="modal-footer">

          <span>
            Project ID: {project.id}
          </span>

          <button
            type="button"
            className="modal-done-button"
            onClick={onClose}
          >
            Close
          </button>

        </div>

      </div>

    </div>
  );
}


export default ProjectDetailModal;