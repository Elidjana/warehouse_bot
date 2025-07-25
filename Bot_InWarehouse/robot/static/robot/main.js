let robotPos = [0, 0];
let running = false;

function startSim(color) {
    fetch(`/start/?color=${color}`)
        .then(() => {
            running = true;
            robotPos = [0, 0];
            tick();
        });
}

function tick() {
    if (!running) return;

    fetch("/step/")
        .then(res => res.json())
        .then(data => {
            robotPos = data.pos;
            drawGrid(robotPos);
            if (data.state !== "done") {
                setTimeout(tick, 300);
            } else {
                running = false;
                alert("✅ Task complete");
            }
        });
}

function drawGrid(pos) {
    const ctx = document.getElementById("grid").getContext("2d");
    ctx.clearRect(0, 0, 600, 600);

    for (let y = 0; y < 12; y++) {
        for (let x = 0; x < 12; x++) {
            ctx.strokeRect(x * 50, y * 50, 50, 50);
        }
    }

    ctx.fillStyle = "red";
    ctx.beginPath();
    ctx.arc(pos[0] * 50 + 25, pos[1] * 50 + 25, 20, 0, Math.PI * 2);
    ctx.fill();
}