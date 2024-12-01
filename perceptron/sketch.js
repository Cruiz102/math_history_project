let gridSize = 32; // Initial grid size
// ... [rest of your existing variables]

// Add new variables for the grid size input
let gridSizeInput;
let gridSizeLabel;
let squares = [
  { x: 0, y: 0, size: 0, grid: [], name: "New Data", color: [255, 165, 0], label: null }, // Orange, data to classify
  { x: 0, y: 0, size: 0, grid: [], name: "Class 1", color: [255, 0, 0], label: 1 }, // Red, label +1
  { x: 0, y: 0, size: 0, grid: [], name: "Class 2", color: [0, 255, 0], label: -1 }, // Green, label -1
];
let centerGrid = {
  x: 0,
  y: 0,
  size: 0,
  grid: []
};

let startButton;
let classifyButton;
let classificationResult;
let clearCenterButton;
let fontSize;

// Added input fields and labels for learning rate and bias
let learningRateInput;
let biasInput;
let learningRateLabel;
let biasLabel;

let weights = []; // Perceptron weights
let bias = 0;
let learningRate = 1;
let trainingData = [];
let trainingIndex = 0;
let isTraining = false;

function setup() {
  createCanvas(windowWidth, windowHeight);

  // Initialize grids for each square
  for (let square of squares) {
    square.grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));
  }

  // Initialize the center grid
  centerGrid.grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));

  // Initialize weights
  weights = Array(gridSize * gridSize).fill(0);

  // Create buttons
  startButton = createButton("Start Training");
  startButton.mousePressed(startTraining);

  classifyButton = createButton("Classify New Data");
  classifyButton.mousePressed(classifyNewData);

  // Create clear buttons for each square
  for (let i = 0; i < squares.length; i++) {
    let square = squares[i];
    let clearButton = createButton(`Clear ${square.name}`);
    square.clearButton = clearButton;
    clearButton.mousePressed(() => clearGrid(square));
  }

  // Create a clear button for the center grid
  clearCenterButton = createButton("Clear Center Grid");
  clearCenterButton.mousePressed(clearCenterGrid);

  // Create a text field to show the classification result
  classificationResult = createDiv("Classification Result: ");

  // Create input fields for learning rate and bias
  learningRateInput = createInput(learningRate.toString());
  learningRateInput.attribute('type', 'number');
  learningRateInput.attribute('step', 'any');
  learningRateInput.attribute('min', '0');

  biasInput = createInput(bias.toString());
  biasInput.attribute('type', 'number');
  biasInput.attribute('step', 'any');

  // Create labels for the input fields
  learningRateLabel = createDiv('Learning Rate:');
  biasLabel = createDiv('Initial Bias:');


    // Create input field for grid size
    gridSizeInput = createInput(gridSize.toString());
    gridSizeInput.attribute('type', 'number');
    gridSizeInput.attribute('min', '8');
    gridSizeInput.attribute('max', '32');
    gridSizeInput.attribute('step', '1');
    gridSizeInput.changed(onGridSizeChanged); // Event handler for changes
  
    gridSizeLabel = createDiv('Grid Size (8-32):');

  // Call setupLayout to position elements
  setupLayout();
}

function setupLayout() {
  // Recalculate positions and sizes
  let w = windowWidth;
  let h = windowHeight;

  fontSize = min(w, h) * 0.02; // 2% of the smaller dimension

  // Adjust square sizes
  let squareSize = min(w, h) * 0.3; // 30% of the smaller dimension

  if (w > h) {
    // Landscape orientation
    let spacing = (w - 3 * squareSize) / 4;
    squares[0].x = spacing;
    squares[0].y = h * 0.1;
    squares[1].x = spacing * 2 + squareSize;
    squares[1].y = h * 0.1;
    squares[2].x = spacing * 3 + 2 * squareSize;
    squares[2].y = h * 0.1;

    centerGrid.x = w / 2 - squareSize / 2;
    centerGrid.y = h * 0.5;
    centerGrid.size = squareSize;
  } else {
    // Portrait orientation
    let spacing = (h - 4 * squareSize) / 5;
    squares[0].x = w * 0.1;
    squares[0].y = spacing;
    squares[1].x = w * 0.1;
    squares[1].y = spacing * 2 + squareSize;
    squares[2].x = w * 0.1;
    squares[2].y = spacing * 3 + 2 * squareSize;

    centerGrid.x = w * 0.1;
    centerGrid.y = spacing * 4 + 3 * squareSize;
    centerGrid.size = squareSize;
  }

  // Set sizes
  for (let square of squares) {
    square.size = squareSize;
  }
  centerGrid.size = squareSize;

  // Style buttons
  startButton.style('font-size', fontSize + 'px');
  classifyButton.style('font-size', fontSize + 'px');
  classificationResult.style('font-size', fontSize + 'px');

  // Style input fields and labels
  learningRateInput.style('font-size', fontSize + 'px');
  biasInput.style('font-size', fontSize + 'px');
  learningRateLabel.style('font-size', fontSize + 'px');
  biasLabel.style('font-size', fontSize + 'px');


  gridSizeInput.style('font-size', fontSize + 'px');
  gridSizeLabel.style('font-size', fontSize + 'px');

  // Position buttons and input fields
  if (w > h) {
    // Landscape orientation - place buttons at the bottom with spacing
    let buttonY = h - fontSize * 6;
    let buttonSpacing = w * 0.02;
    let buttonX = w * 0.05;

    startButton.position(buttonX, buttonY);
    buttonX += startButton.size().width + buttonSpacing;
    classifyButton.position(buttonX, buttonY);
    buttonX += classifyButton.size().width + buttonSpacing;
    classificationResult.position(buttonX, buttonY);

    // Position input fields below buttons
    buttonY += startButton.size().height + fontSize;
    buttonX = w * 0.05;

    learningRateLabel.position(buttonX, buttonY);
    learningRateInput.position(buttonX, buttonY + fontSize * 1.5);

    buttonX += learningRateLabel.size().width + buttonSpacing * 2;

    biasLabel.position(buttonX, buttonY);
    biasInput.position(buttonX, buttonY + fontSize * 1.5);

    buttonX += biasInput.size().width + buttonSpacing * 2;

    gridSizeLabel.position(buttonX, buttonY);
    gridSizeInput.position(buttonX, buttonY + fontSize * 1.5);

  } else {
    // Portrait orientation - place buttons on the right in a vertical stack
    let buttonX = squares[0].x + squareSize + w * 0.05;
    let buttonY = squares[0].y;
    let buttonSpacing = fontSize * 2;

    startButton.position(buttonX, buttonY);
    buttonY += startButton.size().height + buttonSpacing;
    classifyButton.position(buttonX, buttonY);
    buttonY += classifyButton.size().height + buttonSpacing;
    classificationResult.position(buttonX, buttonY);

    // Position input fields below buttons
    buttonY += classificationResult.size().height + buttonSpacing;
    learningRateLabel.position(buttonX, buttonY);
    learningRateInput.position(buttonX, buttonY + fontSize * 1.5);

    buttonY += learningRateLabel.size().height + fontSize * 2;

    biasLabel.position(buttonX, buttonY);
    biasInput.position(buttonX, buttonY + fontSize * 1.5);

    buttonY += biasLabel.size().height + fontSize * 2;

    gridSizeLabel.position(buttonX, buttonY);
    gridSizeInput.position(buttonX, buttonY + fontSize * 1.5);
  }

  // Position and style clear buttons for each square
  for (let square of squares) {
    let clearButton = square.clearButton;
    clearButton.position(square.x, square.y + square.size + fontSize);
    clearButton.style('font-size', fontSize + 'px');
  }

  // Position and style clear center grid button
  clearCenterButton.position(
    centerGrid.x,
    centerGrid.y + centerGrid.size + fontSize
  );
  clearCenterButton.style('font-size', fontSize + 'px');
}



function onGridSizeChanged() {
  let newSize = parseInt(gridSizeInput.value());
  if (isNaN(newSize) || newSize < 8 || newSize > 32) {
    alert("Please enter a valid grid size between 8 and 32.");
    gridSizeInput.value(gridSize.toString());
    return;
  }
  gridSize = newSize;

  // Re-initialize grids for each square
  for (let square of squares) {
    square.grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));
  }

  // Re-initialize the center grid
  centerGrid.grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));

  // Re-initialize weights
  weights = Array(gridSize * gridSize).fill(0);

  // Reset bias and training state
  bias = parseFloat(biasInput.value());
  isTraining = false;

  // Update the layout and redraw the canvas
  setupLayout();
  redraw();
}


function draw() {
  background(220);

  // Draw the squares
  for (let square of squares) {
    stroke(0);
    noFill();
    rect(square.x, square.y, square.size, square.size);

    let cellSize = square.size / gridSize; // Size of each grid cell

    // Draw the grid inside the square
    for (let row = 0; row < gridSize; row++) {
      for (let col = 0; col < gridSize; col++) {
        // Fill the cell if it's marked
        if (square.grid[row][col] === 1) {
          fill(square.color);
        } else {
          noFill();
        }
        stroke(200);
        rect(square.x + col * cellSize, square.y + row * cellSize, cellSize, cellSize);
      }
    }

    // Display the name of the drawing next to the clear button
    fill(0);
    noStroke();
    textSize(fontSize);
    textAlign(LEFT, CENTER);
    text(
      square.name || "Untitled",
      square.x,
      square.y + square.size + fontSize * 2
    );
  }

  // Draw the center grid (to visualize weights)
  drawCenterGrid();

  // Perform continuous drawing while the mouse or touch is pressed
  if ((mouseIsPressed || touches.length > 0) && !isTraining) {
    drawOnSquares();
  }
}

function drawCenterGrid() {
  stroke(0);
  noFill();
  rect(centerGrid.x, centerGrid.y, centerGrid.size, centerGrid.size);

  let cellSize = centerGrid.size / gridSize;

  // Visualize the weights
  for (let row = 0; row < gridSize; row++) {
    for (let col = 0; col < gridSize; col++) {
      let weightIndex = row * gridSize + col;
      let w = weights[weightIndex];
      // Map weight to grayscale color
      let c = map(w, -1, 1, 0, 255);
      c = constrain(c, 0, 255);
      fill(c);
      stroke(200);
      rect(centerGrid.x + col * cellSize, centerGrid.y + row * cellSize, cellSize, cellSize);
    }
  }
}

function drawOnSquares() {
  let inputPositions = [{ x: mouseX, y: mouseY }];
  for (let t of touches) {
    inputPositions.push({ x: t.x, y: t.y });
  }
  for (let pos of inputPositions) {
    for (let square of squares) {
      if (
        pos.x > square.x &&
        pos.x < square.x + square.size &&
        pos.y > square.y &&
        pos.y < square.y + square.size
      ) {
        let cellSize = square.size / gridSize;
        let gridX = Math.floor((pos.x - square.x) / cellSize);
        let gridY = Math.floor((pos.y - square.y) / cellSize);

        if (gridX >= 0 && gridX < gridSize && gridY >= 0 && gridY < gridSize) {
          square.grid[gridY][gridX] = 1; // Mark the grid cell as filled
        }
      }
    }
  }
}

function mousePressed() {
  if (!isTraining) {
    drawOnSquares();
  }
}

function touchStarted() {
  if (!isTraining) {
    drawOnSquares();
  }
}

function touchMoved() {
  if (!isTraining) {
    drawOnSquares();
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  setupLayout();
}

function startTraining() {
  if (isTraining) return;

  // Get values from input fields
  learningRate = parseFloat(learningRateInput.value());
  bias = parseFloat(biasInput.value());

  // Prepare training data
  trainingData = [];
  for (let i = 1; i < squares.length; i++) { // Only Class 1 and Class 2 are used for training
    let square = squares[i];
    let flatGrid = square.grid.flat();
    trainingData.push({
      input: flatGrid,
      label: square.label
    });
  }
  trainingIndex = 0;
  isTraining = true;
  trainPerceptron();
}

function trainPerceptron() {
  if (!isTraining) return;

  // One epoch
  let totalErrors = 0;

  function trainStep() {
    if (trainingIndex >= trainingData.length) {
      trainingIndex = 0; // Reset for next epoch
      if (totalErrors === 0) {
        console.log("Training converged.");
        isTraining = false;
        return;
      } else {
        totalErrors = 0;
      }
    }

    let data = trainingData[trainingIndex];
    let x = data.input;
    let y = data.label;

    // Compute weighted sum
    let weightedSum = 0;
    for (let i = 0; i < weights.length; i++) {
      weightedSum += weights[i] * x[i];
    }
    weightedSum += bias;

    // Activation function (sign function)
    let output = weightedSum >= 0 ? 1 : -1;

    // Update weights if there's an error
    let error = y - output;
    if (error !== 0) {
      totalErrors++;
      for (let i = 0; i < weights.length; i++) {
        weights[i] += learningRate * error * x[i];
      }
      bias += learningRate * error;
    }

    // Update visualization
    trainingIndex++;
    redraw(); // Redraw to update the visualization

    // Delay for visualization
    setTimeout(trainStep, 200); // Adjust delay as needed
  }

  trainStep();
}

function classifyNewData() {
  if (isTraining) {
    alert("Training is still in progress. Please wait for it to complete.");
    return;
  }

  // Get the data from the "New Data" square
  let newData = squares[0].grid.flat();

  // Compute the weighted sum for the new data
  let weightedSum = 0;
  for (let i = 0; i < weights.length; i++) {
    weightedSum += weights[i] * newData[i];
  }
  weightedSum += bias;

  // Determine the class based on the weighted sum
  let output = weightedSum >= 0 ? 1 : -1;

  // Update the classification result
  if (output === 1) {
    classificationResult.html("Classification Result: Class 1 (Red)");
  } else {
    classificationResult.html("Classification Result: Class 2 (Green)");
  }
}

function clearGrid(square) {
  square.grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));
  redraw(); // Update the canvas
}

function clearCenterGrid() {
  // Clear the center grid
  centerGrid.grid = Array.from({ length: gridSize }, () => Array(gridSize).fill(0));

  // Reset weights and bias
  weights = Array(gridSize * gridSize).fill(0);
  bias = parseFloat(biasInput.value());
  isTraining = false;

  // Clear classification result
  classificationResult.html("Classification Result: ");

  redraw(); // Update the canvas
}
