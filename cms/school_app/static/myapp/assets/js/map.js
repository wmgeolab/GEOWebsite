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
      layer.bindPopup(feature.properties.id.toString());
    }
  },
  pointToLayer: createClusterIcon,
}).addTo(map);

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
