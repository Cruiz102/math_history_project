let points = [];
let weights = [0, 0];
let bias = 0;
let learningRate = 1;
let isTraining = false;
let currentClass = 1;
let trainButton, clearButton, classButton;
let canvas;
function setup() {
  let canvasContainer = document.getElementById('canvas-container');
  if (!canvasContainer) {
    console.error("Element with ID 'canvas-container' not found.");
    noLoop();
    return;
  }

  let canvasWidth = canvasContainer.offsetWidth;
  let canvasHeight = canvasContainer.offsetHeight;

  canvas = createCanvas(canvasWidth, canvasHeight);
  canvas.parent('canvas-container');

  // Assign existing buttons by their IDs
  trainButton = select('#trainButton');
  trainButton.mousePressed(startTraining);

  clearButton = select('#clearButton');
  clearButton.mousePressed(clearData);

  classButton = select('#classButton');
  classButton.mousePressed(switchClass);

  drawGrid();
}
function windowResized() {
  let canvasContainer = document.getElementById('canvas-container');
  let canvasWidth = canvasContainer.offsetWidth;
  let canvasHeight = canvasContainer.offsetHeight;
  resizeCanvas(canvasWidth, canvasHeight);
  drawGrid();
}

function draw() {
  // Only redraw when necessary
}

function mousePressed() {
  // Check if mouse is inside the canvas
  if (mouseX >= 0 && mouseX <= width && mouseY >= 0 && mouseY <= height) {
    // Add a new data point
    let x = map(mouseX, 0, width, -1, 1);
    let y = map(mouseY, height, 0, -1, 1); // Invert y-axis
    points.push({
      x: x,
      y: y,
      label: currentClass
    });
    // Draw the point
    noStroke();
    fill(currentClass === 1 ? color(255, 0, 0) : color(0, 0, 255));
    ellipse(mouseX, mouseY, 8, 8);
  }
}

function drawGrid() {
  background(255);
  stroke(200);
  
  // Draw horizontal lines
  for (let i = 0; i <= height; i += height / 20) {
    line(0, i, width, i);
  }

  // Draw vertical lines
  for (let i = 0; i <= width; i += width / 20) {
    line(i, 0, i, height);
  }

  // Redraw existing points
  for (let pt of points) {
    let px = map(pt.x, -1, 1, 0, width);
    let py = map(pt.y, -1, 1, height, 0); // Invert y-axis
    noStroke();
    fill(pt.label === 1 ? color(255, 0, 0) : color(0, 0, 255));
    ellipse(px, py, 8, 8);
  }

  // Draw the separating line if weights are initialized
  if (weights[0] !== 0 || weights[1] !== 0) {
    drawLine();
  }
}

function drawLine() {
  // Line formula: weights[0]*x + weights[1]*y + bias = 0
  // Solve for y when x is -1 and 1
  let x1 = -1;
  let y1 = (-bias - weights[0] * x1) / weights[1];
  let x2 = 1;
  let y2 = (-bias - weights[0] * x2) / weights[1];

  // Map back to screen coordinates
  let px1 = map(x1, -1, 1, 0, width);
  let py1 = map(y1, -1, 1, height, 0);
  let px2 = map(x2, -1, 1, 0, width);
  let py2 = map(y2, -1, 1, height, 0);

  stroke(0);
  line(px1, py1, px2, py2);
}

function switchClass() {
  if (currentClass === 1) {
    currentClass = -1;
    classButton.html('Switch to Class 1');
  } else {
    currentClass = 1;
    classButton.html('Switch to Class 2');
  }
}
// #### THE DATA SHOULD BE NORMALIZED TO GAURANTEE CONVERGENCE
// function normalizeData() {
//   if (points.length === 0) return;

//   // Calculate mean and standard deviation for x and y
//   let meanX = points.reduce((sum, pt) => sum + pt.x, 0) / points.length;
//   let meanY = points.reduce((sum, pt) => sum + pt.y, 0) / points.length;
  
//   let stdX = Math.sqrt(points.reduce((sum, pt) => sum + (pt.x - meanX) ** 2, 0) / points.length);
//   let stdY = Math.sqrt(points.reduce((sum, pt) => sum + (pt.y - meanY) ** 2, 0) / points.length);

//   // Normalize points
//   points = points.map(pt => ({
//     x: (pt.x - meanX) / (stdX || 1), // Avoid division by zero
//     y: (pt.y - meanY) / (stdY || 1),
//     label: pt.label
//   }));
// }

function startTraining() {
  if (!isTraining && points.length > 0) {
    // normalizeData(); // Normalize the data before training
    isTraining = true;
    trainPerceptron();
  }
}

function trainPerceptron() {
  let totalErrors = 0;
  for (let pt of points) {
    let x = [pt.x, pt.y];
    let y = pt.label;
    // Compute the output
    let weightedSum = weights[0] * x[0] + weights[1] * x[1] + bias;
    let output = weightedSum >= 0 ? 1 : -1;
    // Calculate error
    let error = y - output;
    if (error !== 0) {
      totalErrors++;
      // Update weights and bias
      weights[0] += learningRate * error * x[0];
      weights[1] += learningRate * error * x[1];
      bias += learningRate * error;
    }
  }
  drawGrid();
  if (totalErrors === 0) {
    console.log('Training complete.');
    isTraining = false;
  } else {
    // Continue training
    setTimeout(trainPerceptron, 100); // Adjust delay as needed
  }
}

function clearData() {
  points = [];
  weights = [0, 0];
  bias = 0;
  isTraining = false;
  drawGrid();
}
