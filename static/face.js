const square = document.getElementById('square');
const square2 = document.getElementById('square2');
const square3 = document.getElementById('square3');
const square4 = document.getElementById('square4');
const coordinates = document.getElementById('coordinates');


async function updateFacePosition() {
    // Fetch face coordinates from your Flask app
    const response = await fetch('http://172.16.1.135:8000/face');
    const data = await response.json();
    const faceX = data.x;
    const faceY = data.y;

    // Calculate the center of the screen
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;

    // Calculate the difference between the face position and the center
    const deltaX = faceX - centerX;
    const deltaY = faceY - centerY;

    // Calculate the opposite direction
    const oppositeX = centerX - (deltaX * 0.7);
    const oppositeY = centerY - (deltaY * 0.7);
    const oppositeX2 = centerX - (deltaX * 0.6);
    const oppositeY2 = centerY - (deltaY * 0.6);
    const oppositeX3 = centerX - (deltaX * 0.5);
    const oppositeY3 = centerY - (deltaY * 0.5);
    const oppositeX4 = centerX - (deltaX * 0.4);
    const oppositeY4 = centerY - (deltaY * 0.4);

    // Set the square's position
    square.style.transform = `translate(${oppositeX - square.clientWidth / 2}px, ${oppositeY - square.clientHeight / 2}px)`;
    square2.style.transform = `translate(${oppositeX2 - square2.clientWidth / 2}px, ${oppositeY2 - square2.clientHeight / 2}px)`;
    square3.style.transform = `translate(${oppositeX3 - square3.clientWidth / 2}px, ${oppositeY3 - square3.clientHeight / 2}px)`;
    square4.style.transform = `translate(${oppositeX4 - square4.clientWidth / 2}px, ${oppositeY4 - square4.clientHeight / 2}px)`;

    coordinates.innerText = `X: ${faceX}, Y: ${faceY}`;
}

// Update face position every 100 milliseconds
setInterval(updateFacePosition, 10);
