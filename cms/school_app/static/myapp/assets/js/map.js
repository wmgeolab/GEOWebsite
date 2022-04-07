/* global L Supercluster */

var map = L.map("map").setView([-29.106, 26.15], 6);

// Add map tiles to map
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

var markers = L.geoJson(null, {
  onEachFeature: function (feature, layer) {
    if (feature.properties.id) {
      // Create empty popup for each feature and add school ID as a property of the popup
      // We will use the ID to fetch the content to load when the popup is opened
      let p = L.popup();
      p.school_id = feature.properties.id;
      layer.bindPopup(p);
    }
  },
  pointToLayer: createClusterIcon,
}).addTo(map);

// Fetch popup contents on open
map.on("popupopen", (event) => {
  let p = event.popup;
  // Only do a new fetch if we haven't already filled in the contents
  if (p.getContent() === undefined) {
    fetch(`/api/${p.school_id}/`)
      .then((response) => response.json())
      .then((data) => {
        event.popup.setContent(
          `<h4><a href="/schools/${p.school_id}/">${data.name}</a></h4>School ID: ${p.school_id}<br>Country: ${data.country}<br>Sector: ${data.sector}`
        );
      });
  }
});

function createClusterIcon(feature, latlng) {
  if (!feature.properties.cluster) return L.marker(latlng);

  var count = feature.properties.point_count;
  var size = count < 100 ? "small" : count < 1000 ? "medium" : "large";
  var icon = L.divIcon({
    html:
      "<div><span>" +
      feature.properties.point_count_abbreviated +
      "</span></div>",
    className: "marker-cluster marker-cluster-" + size,
    iconSize: L.point(40, 40),
  });

  return L.marker(latlng, {
    icon: icon,
  });
}

// Cluster and display on map
const index = new Supercluster({
  radius: 100,
  maxZoom: 18,
});

// Fetch data from server
fetch("/geojson/")
  .then((response) => response.json())
  .then((data) => {
    index.load(data["features"]);
    console.log(`loaded ${data["features"].length} points`);
    update();
  })
  .catch((error) => console.log(error));

// Update the displayed clusters after user pan / zoom.
map.on("moveend", update);

function update() {
  var bounds = map.getBounds();
  var bbox = [
    bounds.getWest(),
    bounds.getSouth(),
    bounds.getEast(),
    bounds.getNorth(),
  ];
  var zoom = map.getZoom();
  var clusters = index.getClusters(bbox, zoom);
  markers.clearLayers();
  markers.addData(clusters);
}

markers.on("click", (e) => {
  if (e.layer.feature.properties.cluster_id) {
    map.flyTo(
      e.latlng,
      index.getClusterExpansionZoom(e.layer.feature.properties.cluster_id)
    );
  }
});
