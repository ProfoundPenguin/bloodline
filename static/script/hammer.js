const imageContainer = treeEl;
const displayImage = treeSvg;

let minScale = 0.2;
let maxScale = 4;
let imageWidth;
let imageHeight;
let containerWidth;
let containerHeight;
let displayImageX = 0;
let displayImageY = 0;
let displayImageScale = 1;

let rangeX = 0;
let rangeMaxX = 0;
let rangeMinX = 0;

let rangeY = 0;
let rangeMaxY = 0;
let rangeMinY = 0;

let displayImageRangeY = 0;

let displayImageCurrentX = 0;
let displayImageCurrentY = 0;
let displayImageCurrentScale = 1;


function resizeContainer() {
  containerWidth = imageContainer.offsetWidth;
  console.log(containerWidth);
  containerHeight = imageContainer.offsetHeight;
  if (displayDefaultWidth !== undefined && displayDefaultHeight !== undefined) {
    displayDefaultWidth = width;
    displayDefaultHeight = height;
    updateRange();
    displayImageCurrentX = clamp( displayImageX, rangeMinX, rangeMaxX );
    displayImageCurrentY = clamp( displayImageY, rangeMinY, rangeMaxY );
    updateDisplayImage(
      displayImageCurrentX,
      displayImageCurrentY,
      displayImageCurrentScale );
  }
}

resizeContainer();

function clamp(value, min, max) {
    return Math.min(Math.max(min, value), max);
}

function clampScale(newScale) {
  return clamp(newScale, minScale, maxScale);
}

window.addEventListener('resize', resizeContainer, true);

imageContainer.addEventListener('wheel', e => {
  displayImageScale = displayImageCurrentScale = clampScale(displayImageScale + (e.wheelDelta / 800));
  updateRange();
  
  displayImageCurrentX = clamp(displayImageCurrentX, rangeMinX, rangeMaxX)
  displayImageCurrentY = clamp(displayImageCurrentY, rangeMinY, rangeMaxY)
	updateDisplayImage(displayImageCurrentX, displayImageCurrentY, displayImageScale);  
}, false);

function updateDisplayImage(x, y, scale) {
    const transform = 'translateX(' + x + 'px) translateY(' + y + 'px) translateZ(0px) scale(' + scale + ',' + scale + ')';
    displayImage.style.transform = transform;
    displayImage.style.WebkitTransform = transform;
    displayImage.style.msTransform = transform;
}

function updateRange() {
  rangeX = Math.max(0, Math.round(displayDefaultWidth * displayImageCurrentScale));
  rangeY = Math.max(0, Math.round(displayDefaultHeight * displayImageCurrentScale));
  
  // rangeMaxX = Math.round(rangeX / 2);
  rangeMaxX = 9000000
  rangeMinX = 0 - rangeMaxX;

  rangeMaxY = 9000000
  rangeMinY = 0 - rangeMaxY;

  console.log(rangeMaxY);
}
updateRange()


const hammertime = new Hammer(imageContainer);

hammertime.get('pinch').set({ enable: true });
hammertime.get('pan').set({ direction: Hammer.DIRECTION_ALL });

hammertime.on('pan', ev => {  
  displayImageCurrentX = clamp(displayImageX + ev.deltaX, rangeMinX, rangeMaxX);
  displayImageCurrentY = clamp(displayImageY + ev.deltaY, rangeMinY, rangeMaxY);
	updateDisplayImage(displayImageCurrentX, displayImageCurrentY, displayImageScale);
});

hammertime.on('pinch pinchmove', ev => {
  displayImageCurrentScale = clampScale(ev.scale * displayImageScale);
  updateRange();
  displayImageCurrentX = clamp(displayImageX + ev.deltaX, rangeMinX, rangeMaxX);
  displayImageCurrentY = clamp(displayImageY + ev.deltaY, rangeMinY, rangeMaxY);
  updateDisplayImage(displayImageCurrentX, displayImageCurrentY, displayImageCurrentScale);
});

hammertime.on('panend pancancel pinchend pinchcancel', () => {
  displayImageScale = displayImageCurrentScale;
  displayImageX = displayImageCurrentX;
  displayImageY = displayImageCurrentY;
});  