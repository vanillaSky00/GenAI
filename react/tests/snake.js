const canvas = document.getElementById("gameCanvas");\
const ctx = canvas.getContext("2d");\
\
let snake = [\
    { x: 10, y: 10 }\
];\
let direction = { x: 0, y: 0 };\
\
function gameLoop() {\
    ctx.clearRect(0, 0, canvas.width, canvas.height);\
    ctx.fillStyle = "lime";\
    snake.forEach(part => {\
        ctx.fillRect(part.x, part.y, 10, 10);\
    });\
    // Move Snake Logic Here\
    requestAnimationFrame(gameLoop);\
}\
\
document.addEventListener("keydown", event => {\
    if (event.key === "ArrowUp") direction = { x: 0, y: -10 };\
    if (event.key === "ArrowDown") direction = { x: 0, y: 10 };\
    if (event.key === "ArrowLeft") direction = { x: -10, y: 0 };\
    if (event.key === "ArrowRight") direction = { x: 10, y: 0 };\
});\
\
gameLoop();
