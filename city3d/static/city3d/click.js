var longitude, latitude, diff, map, destLongitude, destLatitude, distFrmlast = 0;
var interval = 5000; // initial condition
var assetArr = [];
var modelOrigin, modelOrigin2;
var modelAltitude, modelAltitude2;
var modelRotate, modelRotate2;
var modelAsMercatorCoordinate, modelAsMercatorCoordinate2;
var modelTransform, modelTransform2;
var THREE;
var customLayer, customLayer2;
var previousDistance = 0, currentDistance = 0;
var clock = new THREE.Clock();
var mixer;
var renderer = null;
var sceneTransform;
// $(document).ready(function(){
//   longitude = 77.123643;
//   latitude =  28.707272;
//   assetArr.push({id: "3d0", cord:{lng:longitude,lat:latitude}, url:'https://docs.mapbox.com/mapbox-gl-js/assets/34M_17/34M_17.gltf', scaleFactor:3, rad: 0.02});
//   assetArr.push({ id: "3d2", cord: { lng: 77.125959, lat: 28.707724 }, url: 'https://www.zamit.one/location/gun/scene.gltf', scaleFactor: 30, rad: 0.015 });
//   showmap();
// });
function showmap(callback){
    mapboxgl.accessToken = 'pk.eyJ1IjoiYml0dG9yaW4iLCJhIjoiY2t5Ymh6cTNzMGZvNjJ5cXU3ZHJ5OXlrbyJ9.ODsNhwGJBciLEXvPu8Nw4w';
    map = new mapboxgl.Map({
        container: 'cube',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [ -97.739377, 30.261696 ],
        zoom: 17.6,
        pitch: 95,
        bearing: -17.6,
        antialias: false,
    });
    var geojson = {
            'type': 'FeatureCollection',
            'features': [
              {
                'type': 'Feature',
                'geometry': {
                  'type': 'Point',
                  'coordinates': [longitude,latitude]
                },
                'properties': {
                  'title': 'Mapbox',
                  'description': 'Park Centra'
                }
              }
            ]
          };
    // The 'building' layer in the mapbox-streets vector source contains building-height
    // data from OpenStreetMap.
    map.on('zoom',function(){
       //map.jumpTo({ center: [longitude,latitude] });
    });
    map.on('rotate',function(){
        document.getElementById('info').innerHTML = JSON.stringify(longitude +" : : "+latitude+" : : "+diff);
        map.jumpTo({center: [longitude,latitude]});
    });
    map.on('load', function() {
        // Insert the layer beneath any symbol layer.
        console.log("map loaded");
        var layers = map.getStyle().layers;
        console.log(layers);
        var labelLayerId;
        for (var i = 0; i < layers.length; i++) {
            if (layers[i].type === 'symbol' && layers[i].layout['text-field']) {
                labelLayerId = layers[i].id;
                break;
            }
        }
        map.addLayer(
            {
                'id': '3d-buildings',
                'source': 'composite',
                'source-layer': 'building',
                'filter': ['==', 'extrude', 'true'],
                'type': 'fill-extrusion',
                'minzoom': 15,
                'paint': {
                    'fill-extrusion-color': '#aaa',
                    // use an 'interpolate' expression to add a smooth transition effect to the
                    // buildings as the user zooms in
                    'fill-extrusion-height': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15,
                        0,
                        15.05,
                        ['get', 'height']
                    ],
                    'fill-extrusion-base': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15,
                        0,
                        15.05,
                        ['get', 'min_height']
                    ],
                    'fill-extrusion-opacity': 0.6
                }
            },
            labelLayerId
        );
        addThreeLayer();
        map.addLayer(customLayer3, 'waterway-label');
    });
    map.on('click', e => {
        onClick(e);
    });
}
function addThreeLayer() {
    const originAsset = assetArr[0].cord;
    const mc = mapboxgl.MercatorCoordinate.fromLngLat([originAsset.lng, originAsset.lat], 0);
    const meterScale = mc.meterInMercatorCoordinateUnits();
    sceneTransform = {};
    sceneTransform.matrix = new THREE.Matrix4()
        .makeTranslation(mc.x, mc.y, mc.z)
        .scale(new THREE.Vector3(meterScale, -meterScale, meterScale));
    sceneTransform.origin = new THREE.Vector3(mc.x, mc.y, mc.z);
    THREE = window.THREE;
    // configuration of the custom layer for a 3D model per the CustomLayerInterface
    customLayer3 = {
        id: 'customLayer3',
        type: 'custom',
        renderingMode: '3d',
        onAdd: function (map, gl) {
            this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000)
            this.scene = new THREE.Scene();
            camera = this.camera;
            scene = this.scene;
            // create two three.js lights to illuminate the model
            var light1 = new THREE.AmbientLight( 0xffffff );
            light1.position.set(0, -70, 100).normalize();
            this.scene.add(light1);
            var light2 = new THREE.AmbientLight( 0xffffff );
            light2.position.set(0, 70, 100).normalize();
            this.scene.add(light2);
            var loader = new THREE.GLTFLoader();
            // use the three.js GLTF loader to add the 3D model to the three.js scene
            for (var i = 0; i < assetArr.length; i++) {
                const modelOrigin3 = [assetArr[i].cord.lng, assetArr[i].cord.lat];
                const modelAltitude3 = 0;
                const modelRotate3 = new THREE.Euler(Math.PI / 2, 0, 0, 'XYZ');
                const modelScale = assetArr[i].scaleFactor;
                const mc = mapboxgl.MercatorCoordinate.fromLngLat(modelOrigin3, modelAltitude3);
                loader.load(
                    assetArr[i].url,
                    function (gltf) {
                        const scene = gltf.scene;
                        const origin = sceneTransform.origin;
                        scene.position.set((mc.x - origin.x) / meterScale, -(mc.y - origin.y) / meterScale, (mc.z - origin.z) / meterScale);
                        scene.quaternion.setFromEuler(modelRotate3);
                        scene.scale.set(modelScale, modelScale, modelScale)
                        this.scene.add(gltf.scene);
                    }.bind(this)
                );
            }
            this.map = map;
            // use the Mapbox GL JS map canvas for three.js
            this.renderer = new THREE.WebGLRenderer({
                canvas: map.getCanvas(),
                context: gl,
                antialias: true
            });
            this.renderer.autoClear = false;
            if(renderFlag == true){
                renderFlag = false;
                this.renderer.domElement.addEventListener( 'touchend', onClick, false );
            }
        },
        render: function (gl, matrix) {
            this.camera.projectionMatrix =  new THREE.Matrix4().fromArray(matrix).multiply(sceneTransform.matrix);
            this.renderer.state.reset();
            this.renderer.render(this.scene, this.camera);
            this.map.triggerRepaint();
        }
    }
}
var renderFlag = true, scene, camera;
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2( Infinity, Infinity );
function onClick( event ) {
    event.preventDefault();
    mouse.x = ( event.point.x / window.innerWidth ) * 2 - 1;
    mouse.y = - ( event.point.y / window.innerHeight ) * 2 + 1;
    const camInverseProjection =
        new THREE.Matrix4().getInverse(this.camera.projectionMatrix);
const cameraPosition =
        new THREE.Vector3().applyMatrix4(camInverseProjection);
const mousePosition =
        new THREE.Vector3(mouse.x, mouse.y, 1)
        .applyMatrix4(camInverseProjection);
const viewDirection = mousePosition.clone()
        .sub(cameraPosition).normalize();
        this.raycaster.set(cameraPosition, viewDirection);
    var intersects = raycaster.intersectObjects( scene.children, true );
    console.log("Here",intersects);
    if ( intersects.length > 0 ) {
        console.log("hi");
        console.log( 'Intersection:', intersects[ 0 ].object.name == "");
    }
}
