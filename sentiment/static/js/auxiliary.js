function getChildrenOfElement(parentId, childrenTag) {
  const p = document.getElementById(parentId);
  return p.querySelectorAll(childrenTag);
}

function hasActiveShape(featureGroup, shapeType) {
  var flag = false;
  featureGroup.eachLayer(function(layer) {
    const color = layer.options.color;
    if (color == Colors.darkred && layer instanceof shapeType)
      flag = true;
  });
  return flag;
}
