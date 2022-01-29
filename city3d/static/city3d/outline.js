const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
const cube = new THREE.Mesh( geometry, material );
scene.add( cube );

camera.position.z = 5;

var controls = new THREE.OrbitControls(camera, renderer.domElement);

// Postprocessing - outline
var selectedObjects = []

var renderPass = new THREE.RenderPass( scene, camera );

var outlinePass = new THREE.OutlinePass( new THREE.Vector2( window.innerWidth, window.innerHeight ), scene, camera );
outlinePass.edgeStrength = 3.0
outlinePass.edgeGlow  = 0.5
outlinePass.edgeThickness = 1.0;
outlinePass.visibleEdgeColor.set('#ffffff');
outlinePass.hiddenEdgeColor.set('#000000');
outlinePass.selectedObjects = selectedObjects;

var effectFXAA = new THREE.ShaderPass(THREE.FXAAShader);
effectFXAA.uniforms['resolution'].value.set(1 / window.innerWidth, 1 / window.innerHeight);
effectFXAA.renderToScreen = true;

var composer = new THREE.EffectComposer( renderer );
composer.setSize(window.innerWidth, window.innerHeight);

composer.addPass( renderPass );
composer.addPass( outlinePass );
composer.addPass( effectFXAA );

const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

window.addEventListener( 'pointermove', onPointerMove );

function onPointerMove( event ) {

  if ( event.isPrimary === false ) return;

  mouse.x = ( event.clientX / window.innerWidth ) * 2 - 1;
  mouse.y = - ( event.clientY / window.innerHeight ) * 2 + 1;

  checkIntersection();

}

function addSelectedObject( object ) {

  selectedObjects = [];
  selectedObjects.push( object );

}

function checkIntersection() {

  raycaster.setFromCamera( mouse, camera );

  const intersects = raycaster.intersectObject( scene, true );

  if ( intersects.length > 0 ) {

    const selectedObject = intersects[ 0 ].object;
    addSelectedObject( selectedObject );
    outlinePass.selectedObjects = selectedObjects;

  } else {

    selectedObjects = [];
    // outlinePass.selectedObjects = selectedObjects;
  }

}

function animate() {
	requestAnimationFrame( animate );

  cube.rotation.x += 0.01;
	cube.rotation.y += 0.01;

	// renderer.render( scene, camera );
  controls.update();
  composer.render();
};

animate();
