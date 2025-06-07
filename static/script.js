async function cargarEstado() {
    const res = await fetch('/estado');
    const data = await res.json();
    document.getElementById('score').textContent = 'Puntuación: ' + data.score;
    for (const region in data) {
        if (region === 'score') continue;
        const div = document.getElementById(region);
        div.innerHTML = region + ' (' + data[region].terrain + ')';
        const units = data[region].human;
        let offset = 0;
        for (const tipo in units) {
            for (let i = 0; i < units[tipo]; i++) {
                const el = document.createElement('div');
                el.classList.add('unit', tipo);
                el.style.left = offset + 'px';
                el.style.top = offset + 'px';
                offset += 10;
                div.appendChild(el);
            }
        }
    }
}

async function enviarAccion() {
    const accion = document.getElementById('accion').value;
    const origen = document.getElementById('origen').value;
    const destino = document.getElementById('destino').value;
    const tipo = document.getElementById('tipo').value;
    await fetch('/accion_jugador', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({accion, origen, destino, tipo})
    });
    await fetch('/accion_ia', {method: 'POST'});
    cargarEstado();
}

window.onload = cargarEstado;
