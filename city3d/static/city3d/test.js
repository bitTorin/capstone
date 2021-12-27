// This is the default access token from your ion account
Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiIyZTYwYmFjNC0xNzA1LTRkZTEtOTA3Yi0xZGFjMjAzOTRlZmYiLCJpZCI6Nzc3NDMsImlhdCI6MTY0MDU3NDQ2Nn0.3UiO_F9WrMcflbYSNd3JIyAA_2qpkpYRxOA4uG6y9vE';

// Initialize the Cesium Viewer in the HTML element with the `cesiumContainer` ID.
const viewer = new Cesium.Viewer('cesiumContainer', {
  terrainProvider: Cesium.createWorldTerrain()
});

viewer.scene.globe.depthTestAgainstTerrain = true;

// Add Cesium OSM Buildings, a global 3D buildings layer.
const buildingTileset = viewer.scene.primitives.add(Cesium.createOsmBuildings());

// Fly the camera to selected city at the given longitude, latitude, and height.
viewer.camera.flyTo({
  destination : Cesium.Cartesian3.fromDegrees(long, lat, height),
  orientation : {
    heading : Cesium.Math.toRadians(-15.0),
    pitch : Cesium.Math.toRadians(-15.0),
  }
});

// HTML overlay for showing feature name on mouseover
var nameOverlay = document.createElement('div');
viewer.container.appendChild(nameOverlay);
nameOverlay.className = 'backdrop';
nameOverlay.style.display = 'none';
nameOverlay.style.position = 'absolute';
nameOverlay.style.bottom = '0';
nameOverlay.style.left = '0';
nameOverlay.style['pointer-events'] = 'none';
nameOverlay.style.padding = '4px';
nameOverlay.style.backgroundColor = 'black';
