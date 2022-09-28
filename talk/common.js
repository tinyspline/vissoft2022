var slider = document.getElementById("morph");
var canvas = document.getElementById("canvas");
var origin, target, morphism;
var morphOverride, drawMorphOverride = false;
var originAligned, targetAligned, drawAligned = false;

function clear() {
    let ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

function draw(polyline, controlPoints) {
    let ctx = canvas.getContext("2d");

    // Draw spline as polyline.
    ctx.fillStyle = "black";
    ctx.beginPath();
    ctx.moveTo(polyline[0], polyline[1]);
    for (var i = 1; i < polyline.length; i++) {
        ctx.lineTo(polyline[i*2], polyline[i*2 + 1]);
    }
    ctx.stroke();

    // Draw control points.
    ctx.fillStyle = "red";
    let rectSize = 6;
    for (var i = 0; i < controlPoints.length; i++) {
        ctx.fillRect(controlPoints[i*2] - rectSize/2,
                     controlPoints[i*2 + 1] - rectSize/2,
                     rectSize, rectSize);
    }
}

function update() {
    clear();

    let spline = morphism.eval(slider.value / slider.max);
    if (drawMorphOverride) {
        morphOverride.controlPoints = spline.controlPoints;
        draw(morphOverride.sample(), []);
    } else {
        draw(spline.sample(), []);
    }
    spline.delete();

    if (drawAligned) {
        draw(originAligned.sample(), originAligned.controlPoints);
        draw(targetAligned.sample(), targetAligned.controlPoints);
    } else {
        draw(origin.sample(), origin.controlPoints);
        draw(target.sample(), target.controlPoints);
    }
}

function easeInOutQuart(x) {
    return x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2;
}

function animateMorphism() {
    slider.value = 0;
    let val = 0.0;

    let id = null;
    clearInterval(id);
    id = setInterval(frame, 5);
    function frame() {
        if (val > 1) {
            clearInterval(id);
        } else {
            val += 0.005;
            slider.value = easeInOutQuart(val) * slider.max;
            update();
        }
    }
}

function toggleMorphOverride() {
    drawMorphOverride = !drawMorphOverride;
    update();
}

function toggleAligned() {
    drawAligned = !drawAligned;
    update();
}

slider.addEventListener('input', function() {
    update();
});
slider.value = slider.min;
