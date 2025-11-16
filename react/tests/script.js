const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let snake = [{ x: 10, y: 10 }];
let direction = { x: 0, y: 0 };  
let food = {};  
let score = 0;

function placeFood() {
    food.x = Math.floor(Math.random() * (canvas.width / 10)) * 10;
    food.y = Math.floor(Math.random() * (canvas.height / 10)) * 10;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = 'green';
    snake.forEach(part => {
        ctx.fillRect(part.x, part.y, 10, 10);
    });
    ctx.fillStyle = 'red';
    ctx.fillRect(food.x, food.y, 10, 10);
}

function update() {
    const head = { x: snake[0].x + direction.x, y: snake[0].y + direction.y };

    if (head.x === food.x && head.y === food.y) {
        score++;
        placeFood();
    } else {
        snake.pop();
    }

    snake.unshift(head);
}

function gameLoop() {
    draw();
    update();
    setTimeout(gameLoop, 100);
}

function changeDirection(event) {
    switch (event.key) {
        case 'ArrowUp':
            direction = { x: 0, y: -10 };
            break;
        case 'ArrowDown':
            direction = { x: 0, y: 10 };
            break;
        case 'ArrowLeft':
            direction = { x: -10, y: 0 };
            break;
        case 'ArrowRight':
            direction = { x: 10, y: 0 };
            break;
    }
}

window.addEventListener('keydown', changeDirection);
placeFood();
gameLoop();