import {
  useEffect,
  useState,
} from "react";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

import {
  getMapData,
} from "../services/api";


function InvestmentMap() {

  const [
    locations,
    setLocations
  ] = useState([]);

  const [
    loading,
    setLoading
  ] = useState(true);

  const [
    error,
    setError
  ] = useState(null);


  useEffect(() => {

    const loadMap = async () => {

      try {

        const data =
          await getMapData();

        setLocations(data);

      } catch (err) {

        console.error(err);

        setError(
          "Could not load investment map."
        );

      } finally {

        setLoading(false);

      }
    };


    loadMap();

  }, []);


  const formatCurrency =
    (value) => {

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


  const formatNumber =
    (value) => {

      return new Intl.NumberFormat(
        "en-US"
      ).format(value);
    };


  const markerRadius =
    (projectCount) => {

      return Math.max(
        6,
        Math.min(
          22,
          5 +
          Math.sqrt(projectCount) * 4
        )
      );
    };


  if (loading) {

    return (

      <section
        className="map-card"
      >

        <div
          className="map-message"
        >
          Loading investment map...
        </div>

      </section>

    );
  }


  if (error) {

    return (

      <section
        className="map-card"
      >

        <div
          className="map-message"
        >
          {error}
        </div>

      </section>

    );
  }


  return (

    <section
      className="map-card"
    >

      <div
        className="chart-header"
      >

        <div>

          <h3>
            Global FDI Investment Map
          </h3>

          <p>
            Destination countries sized
            by number of investment projects
          </p>

        </div>


        <div
          className="map-location-count"
        >
          {locations.length}
          {" "}
          markets
        </div>

      </div>


      <div
        className="investment-map"
      >

        <MapContainer
          center={[20, 10]}
          zoom={2}
          minZoom={2}
          maxZoom={7}
          scrollWheelZoom={true}
          worldCopyJump={true}
          style={{
            height: "100%",
            width: "100%",
          }}
        >

          <TileLayer
            attribution={
              "&copy; OpenStreetMap contributors"
            }
            url={
              "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            }
          />


          {locations.map(
            (location) => (

              <CircleMarker
                key={
                  location.country_code
                }

                center={[
                  location.latitude,
                  location.longitude,
                ]}

                radius={
                  markerRadius(
                    location.project_count
                  )
                }

                pathOptions={{
                  fillOpacity: 0.7,
                  weight: 1.5,
                }}
              >

                <Popup>

                  <div
                    className="map-popup"
                  >

                    <strong>
                      {
                        location
                          .country_name
                      }
                    </strong>

                    <span>
                      {
                        location
                          .region
                      }
                    </span>

                    <hr />

                    <div>
                      <b>
                        Projects:
                      </b>
                      {" "}
                      {
                        formatNumber(
                          location
                            .project_count
                        )
                      }
                    </div>

                    <div>
                      <b>
                        Capex:
                      </b>
                      {" "}
                      {
                        formatCurrency(
                          location
                            .total_capex_usd
                        )
                      }
                    </div>

                    <div>
                      <b>
                        Jobs:
                      </b>
                      {" "}
                      {
                        formatNumber(
                          location
                            .total_jobs
                        )
                      }
                    </div>

                  </div>

                </Popup>

              </CircleMarker>

            )
          )}

        </MapContainer>

      </div>


      <div
        className="map-note"
      >
        Markers represent country-level
        destination locations for synthetic
        demonstration data.
      </div>

    </section>

  );
}


export default InvestmentMap;